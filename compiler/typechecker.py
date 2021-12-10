from parser.core import AstVisitor, BinaryExpressionNode, PathNode, ExternProcessNode, ConditionalNode, \
    ReplicatedInputProcessNode, InactionProcessNode, RestrictionProcessNode, ParallelProcessNode, OutputProcessNode, \
    InputProcessNode, RecordNode, IdentifierValueNode, IntegerValueNode, StringValueNode, FalseValueNode, TrueValueNode


class TypeReference:
    def __init__(self, type_name):
        self.type_name = type_name


class TypeCheckerVisitor(AstVisitor):
    def __init__(self, record_declarations=None):
        if record_declarations is None:
            record_declarations = {}

    # Literals are already given a type during transformation

    def visit_identifier_node(self, node: IdentifierValueNode):
        super().visit_identifier_node(node)

    def visit_record_node(self, node: RecordNode):
        super().visit_record_node(node)

    def visit_input_process_node(self, node: InputProcessNode):
        return super().visit_input_process_node(node)

    def visit_output_process_node(self, node: OutputProcessNode):
        return super().visit_output_process_node(node)

    def visit_parallel_process_node(self, node: ParallelProcessNode):
        return super().visit_parallel_process_node(node)

    def visit_restriction_process_node(self, node: RestrictionProcessNode):
        return super().visit_restriction_process_node(node)

    def visit_inaction_process_node(self, node: InactionProcessNode):
        super().visit_inaction_process_node(node)

    def visit_replicated_input_process_node(self, node: ReplicatedInputProcessNode):
        return super().visit_replicated_input_process_node(node)

    def visit_conditional_node(self, node: ConditionalNode):
        return super().visit_conditional_node(node)

    def visit_extern_process_node(self, node: ExternProcessNode):
        return super().visit_extern_process_node(node)

    def visit_path_node(self, node: PathNode):
        return super().visit_path_node(node)

    def visit_binary_expression_node(self, node: BinaryExpressionNode):
        return super().visit_binary_expression_node(node)