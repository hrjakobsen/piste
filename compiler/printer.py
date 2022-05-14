from parser.core import AstVisitor, RestrictionProcessNode, InputProcessNode, TrueValueNode, FalseValueNode, \
    StringValueNode, IntegerValueNode, IdentifierValueNode, OutputProcessNode, ParallelProcessNode, InactionProcessNode, \
    ReplicatedInputProcessNode, ConditionalNode, ExternProcessNode, RecordNode, PathNode, BinaryExpressionNode, \
    ListAccessNode, ListCreationNode


class PrinterVisitor(AstVisitor):
    def __init__(self):
        self.indentation = 0

    def visit_true_value_node(self, node: TrueValueNode):
        return "true"

    def visit_false_value_node(self, node: FalseValueNode):
        return "false"

    def visit_string_value_node(self, node: StringValueNode):
        return "\"" + node.value + "\""

    def visit_integer_value_node(self, node: IntegerValueNode):
        return str(node.value)

    def visit_identifier_node(self, node: IdentifierValueNode):
        return str(node.value)

    def visit_input_process_node(self, node: InputProcessNode):
        receiver = node.receiver.accept(self)
        s = self.indent() + receiver + "?" + self.print_list(map(lambda x: x.name + ": " + str(x.type), node.identifiers)) + " = \n"
        self.indentation += 1
        s += node.continuation.accept(self)
        self.indentation -= 1
        return s

    def visit_replicated_input_process_node(self, node: ReplicatedInputProcessNode):
        receiver = node.receiver.accept(self)
        s = self.indent() + receiver + "?*" + self.print_list(map(lambda x: x.name + ": " + str(x.type), node.identifiers)) + " = \n"
        self.indentation += 1
        s += node.continuation.accept(self)
        self.indentation -= 1
        return s

    def visit_output_process_node(self, node: OutputProcessNode):
        receiver = node.receiver.accept(self)
        return self.indent() + receiver + "!" + self.print_list(map(lambda x: x.accept(self), node.values))

    def visit_parallel_process_node(self, node: ParallelProcessNode):
        return "{2}(\n{0} \n{2}|\n{1}\n{2})".format(node.left.accept(self), node.right.accept(self), self.indent())

    def visit_restriction_process_node(self, node: RestrictionProcessNode):
        s = self.indent() + "channel " + node.identifier.name + ": " + str(node.identifier.type) + " in \n"
        self.indentation += 1
        s += node.continuation.accept(self)
        self.indentation -= 1
        return s

    def visit_inaction_process_node(self, node: InactionProcessNode):
        return self.indent() + "skip"

    def visit_conditional_node(self, node: ConditionalNode):
        initial_indent = self.indent()
        self.indentation += 1

        s = "{3}if {0} then\n{1}\n{3}else \n{2} \n{3}".format(node.predicate.accept(self),
                                                                  node.true_branch.accept(self),
                                                                  node.false_branch.accept(self),
                                                                  initial_indent)

        self.indentation -= 1
        return s

    def visit_extern_process_node(self, node: ExternProcessNode):
        self.indentation += 1
        cont = node.continuation.accept(self)
        self.indentation -= 1
        return "{3}extern {1}({0}) in\n{2}".format(
            node.external_name.name,
            node.internal_name.name,
            cont,
            self.indent()
        )

    def visit_record_node(self, node: RecordNode):
        return "{ " + ", ".join(map(lambda x: "."+ x[0] + " = " + x[1].accept(self), node.name)) + " }"

    def visit_path_node(self, node: PathNode):
        return "{}.{}".format(
            node.value.accept(self),
            node.field_name.name
        )

    def visit_binary_expression_node(self, node: BinaryExpressionNode):
        return "({} {} {})".format(
            node.left.accept(self),
            node.operation,
            node.right.accept(self)
        )

    def visit_list_creation_node(self, node: ListCreationNode):
        return "[{}]".format(", ".join(map(lambda e: e.accept(self), node.element_expressions)))

    def visit_list_access_node(self, node: ListAccessNode):
        return "{}[{}]".format(node.target_list.accept(self), node.index_expression.accept(self))

    def print_list(self, lst):
        return "[" + ", ".join(lst) + "]"

    def indent(self):
        return "    " * self.indentation
