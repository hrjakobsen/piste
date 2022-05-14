from parser.core import *


class RenamerVisitor(AstVisitor):
    def __init__(self, symbols):
        self.counter = 0

        for symbol in symbols:
            symbol.name = self.next_name(symbol.name)

    def next_name(self, initial_name="piste_proc"):
        name = initial_name + "_" + str(self.counter)
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

    def visit_identifier_node(self, node: IdentifierValueNode):
        node.value = node.identifier_declaration.name


class DeclarationAnnotatorVisitor(AstVisitor):
    """
    This class adds references to IdentifierValueNode
    to point to the initial variable declaration
    """
    def __init__(self):
        self.symbols = []
        self.symbol_stack = []

    def visit_identifier_node(self, node: IdentifierValueNode):
        node.identifier_declaration = self.get_symbol(node.value)

    def visit_input_process_node(self, node: InputProcessNode):
        node.receiver.accept(self)

        for arg in node.identifiers:
            self.symbol_stack.append((arg.name, arg))
            self.symbols.append(arg)

        node.continuation.accept(self)

        for _ in node.identifiers:
            self.symbol_stack.pop()

    def visit_restriction_process_node(self, node: RestrictionProcessNode):
        self.symbols.append(node.identifier)
        self.symbol_stack.append((node.identifier.name, node.identifier))
        node.continuation.accept(self)
        self.symbol_stack.pop()

    def visit_replicated_input_process_node(self, node: ReplicatedInputProcessNode):
        node.receiver.accept(self)

        for arg in node.identifiers:
            self.symbol_stack.append((arg.name, arg))
            self.symbols.append(arg)

        node.continuation.accept(self)

        for _ in node.identifiers:
            self.symbol_stack.pop()

    def visit_extern_process_node(self, node: ExternProcessNode):
        self.symbols.append(node.internal_name)
        self.symbol_stack.append((node.internal_name.name, node.internal_name))
        node.continuation.accept(self)
        self.symbol_stack.pop()

    def get_symbol(self, id_name):
        for (name, identifier) in reversed(self.symbol_stack):
            if name == id_name:
                return identifier
        raise Exception("No binder for identifier " + id_name)


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

    def visit_identifier_node(self, node: IdentifierValueNode):
        node.free_variables = [node.value]
        return node.free_variables

    def visit_record_node(self, node: RecordNode):
        node.free_variables = []
        for (ident, val) in node.value:
            node.free_variables += val.accept(self)
        node.free_variables = self.sort(set(node.free_variables))
        return node.free_variables

    def visit_input_process_node(self, node: InputProcessNode):
        free_vars = set(node.receiver.accept(self))
        free_vars = set(free_vars) | set(node.continuation.accept(self))
        for identifier in node.identifiers:
            free_vars -= {identifier.name}
        node.free_variables = self.sort(free_vars)
        return node.free_variables

    def visit_replicated_input_process_node(self, node: ReplicatedInputProcessNode):
        free_vars = set(node.receiver.accept(self))
        free_vars |= set(node.continuation.accept(self))
        for identifier in node.identifiers:
            free_vars -= {identifier.name}
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
        node.free_variables = self.sort(set(node.continuation.accept(self)) - {node.identifier.name})
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
        node.free_variables = self.sort(set(node.continuation.accept(self)) - {node.external_name.name})
        return node.free_variables

    def visit_path_node(self, node: PathNode):
        node.free_variables = node.value.accept(self)
        return node.free_variables

    def visit_binary_expression_node(self, node: BinaryExpressionNode):
        node.free_variables = self.sort(set(node.left.accept(self)) | set(node.right.accept(self)))
        return node.free_variables

    def visit_list_creation_node(self, node: ListCreationNode):
        frees = set()
        for expr in node.element_expressions:
            free_vars = expr.accept(self)
            frees |= set(free_vars)
        node.free_variables = self.sort(list(frees))
        return node.free_variables

    def visit_list_access_node(self, node: ListAccessNode):
        node.free_variables = self.sort(set(node.target_list.accept(self)) | set(node.index_expression.accept(self)))
        return node.free_variables

    def sort(self, set_of_fv):
        return list(sorted(set_of_fv))


def pass_one(ast):
    decl_annotator = DeclarationAnnotatorVisitor()
    ast.accept(decl_annotator)
    renamer = RenamerVisitor(decl_annotator.symbols)
    ast.accept(renamer)
    ast.accept(FreeVariableVisitor())
    return ast