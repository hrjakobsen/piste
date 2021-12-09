from parser.core import *


class RenamerVisitor(AstVisitor):
    def __init__(self):
        self.counter = 0

    def next_name(self):
        name = "proc" + str(self.counter)
        self.counter += 1
        return name

    def visit_input_process_node(self, node: InputProcessNode):
        node.name = self.next_name()
        return super().visit_input_process_node(node)

    def visit_replicated_input_process_node(self, node: InputProcessNode):
        node.name = self.next_name()
        return super().visit_input_process_node(node)

    def visit_extern_process_node(self, node: ExternProcessNode):
        node.name = self.next_name()
        return super().visit_extern_process_node(node)

    def visit_record_node(self, node: RecordNode):
        node.name = self.next_name()


class FreeVariableVisitor(AstVisitor):
    def visit_true_value_node(self, node: TrueValueNode):
        node.free_variables = []
        return node.free_variables

    def visit_false_value_node(self, node: FalseValueNode):
        node.free_variables = []
        return node.free_variables

    def visit_string_value_node(self, node: StringValueNode):
        node.free_variables = []
        return node.free_variables

    def visit_integer_value_node(self, node: IntegerValueNode):
        node.free_variables = []
        return node.free_variables

    def visit_identifier_node(self, node: IdentifierNode):
        node.free_variables = [node.value]
        return node.free_variables

    def visit_record_node(self, node: RecordNode):
        node.free_variables = []
        return node.free_variables

    def visit_input_process_node(self, node: InputProcessNode):
        free_vars = set(node.receiver.accept(self))
        free_vars = set(free_vars) | set(node.continuation.accept(self))
        for identifier in node.identifiers:
            identifier.accept(self)
            free_vars -= set(identifier.free_variables)
        node.free_variables = self.sort(free_vars)
        return node.free_variables

    def visit_replicated_input_process_node(self, node: ReplicatedInputProcessNode):
        free_vars = set(node.receiver.accept(self))
        free_vars |= set(node.continuation.accept(self))
        for identifier in node.identifiers:
            identifier.accept(self)
            free_vars -= set(identifier.free_variables)
        node.free_variables = self.sort(free_vars)
        return node.free_variables

    def visit_output_process_node(self, node: OutputProcessNode):
        frees = set(node.receiver.accept(self))
        for value in node.values:
            free_vars = value.accept(self)
            frees |= set(free_vars)
        node.free_variables = self.sort(list(frees))
        return node.free_variables

    def visit_parallel_process_node(self, node: ParallelProcessNode):
        node.free_variables = self.sort(set(node.left.accept(self)) | set(node.right.accept(self)))
        return node.free_variables

    def visit_restriction_process_node(self, node: RestrictionProcessNode):
        node.free_variables = self.sort(set(node.continuation.accept(self)) - {node.identifier.value})
        return node.free_variables

    def visit_inaction_process_node(self, node: InactionProcessNode):
        node.free_variables = []
        return node.free_variables

    def visit_conditional_node(self, node: ConditionalNode):
        node.free_variables = self.sort(set(node.predicate.accept(self)) |
                                        set(node.true_branch.accept(self)) |
                                        set(node.false_branch.accept(self)))
        return node.free_variables

    def visit_extern_process_node(self, node: ExternProcessNode):
        node.external_name.accept(self)
        node.free_variables = self.sort(set(node.continuation.accept(self)) - set(node.external_name.free_variables))
        return node.free_variables

    def visit_path_node(self, node: PathNode):
        node.free_variables = node.value.accept(self)
        return node.free_variables

    def visit_binary_expression_node(self, node: BinaryExpressionNode):
        node.free_variables = self.sort(set(node.left.accept(self)) | set(node.right.accept(self)))
        return node.free_variables

    def sort(self, set_of_fv):
        return list(sorted(set_of_fv))


def pass_one(ast):
    renamer = RenamerVisitor()
    ast.accept(renamer)
    ast.accept(FreeVariableVisitor())
    return ast