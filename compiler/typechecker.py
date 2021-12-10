from parser.core import AstVisitor, BinaryExpressionNode, PathNode, ExternProcessNode, ConditionalNode, \
    ReplicatedInputProcessNode, InactionProcessNode, RestrictionProcessNode, ParallelProcessNode, OutputProcessNode, \
    InputProcessNode, RecordNode, IdentifierValueNode, IntegerValueNode, StringValueNode, FalseValueNode, TrueValueNode, \
    MessageType, ChannelType, Type


class TypesystemException(Exception):
    pass


class TypingException(TypesystemException):
    def __init__(self, error, node=None, *args):
        msg = "Invalid typing"
        if node is not None and node.code_position is not None:
            msg += " at position ({},{})".format(node.code_position[0][0], node.code_position[0][1])
        msg += ": {}".format(error)
        super().__init__(msg)


class WrongTypeException(TypesystemException):
    def __init__(self, expected_type, actual_type, node=None, *args):
        msg = "Expected type {} got type {}".format(expected_type, actual_type)
        if node is not None and node.code_position is not None:
            msg += " at position ({},{})".format(node.code_position[0][0], node.code_position[0][1])
        super().__init__(msg)


class TypeReference:
    def __init__(self, type_name):
        self.type_name = type_name
        self.inferred_channel_types = {}


def compare_messages_to_channel_type(message_type, channel_type, channel_name="Unknown"):
    chn_type = ChannelType(message_type)
    if not chn_type.is_equal_to(channel_type):
        raise TypingException("Failed type checking for channel {}, {} {}".format(channel_name, chn_type, channel_type))


class ChannelTypeInferVisitor(AstVisitor):
    def __init__(self, typechecker):
        self.typechecker = typechecker

    def visit_output_process_node(self, node: OutputProcessNode):
        if node.receiver.type is not None:
            return
        arg_types = []
        for value in node.values:
            if value.type is None:
                value.accept(self.typechecker)
            if value.type is None:
                return
            arg_types.append(value.type)
        typ = ChannelType(MessageType(arg_types))
        node.receiver.type = typ
        if isinstance(node.receiver, IdentifierValueNode):
            node.receiver.identifier_declaration.type = typ


class TypeCheckerVisitor(AstVisitor):
    def __init__(self, record_declarations):
        self.record_declarations = record_declarations
        self.channel_infer_visitor = ChannelTypeInferVisitor(self)

    def visit_identifier_node(self, node: IdentifierValueNode):
        node.type = node.identifier_declaration.type

    def visit_input_process_node(self, node: InputProcessNode):
        node.receiver.accept(self)
        if node.receiver.type is None:
            raise TypingException("Unknown type of input channel", node)
        if not isinstance(node.receiver.type, ChannelType):
            raise TypingException("Input is not a channel type", node)
        if len(node.identifiers) != len(node.receiver.type.message_type.arg_types):
            raise TypingException("Invalid number of messages, expected {} got {}".format(
                    len(node.receiver.type.message_type.arg_types),
                    len(node.identifiers)),
                node)
        for i, identifier in enumerate(node.identifiers):
            identifier.type = node.receiver.type.message_type.arg_types[i]
        node.continuation.accept(self)

    def visit_output_process_node(self, node: OutputProcessNode):
        node.receiver.accept(self)
        arg_types = []
        for x in node.values:
            x.accept(self)
            if x.type is None:
                raise TypingException("Couldn't type expression in output args", x)
            arg_types.append(x.type)
        if node.receiver.type is None:
            node.accept(self.channel_infer_visitor)
        if node.receiver.type is None:
            raise TypingException("Unable to infer channel type", node.receiver)
        compare_messages_to_channel_type(MessageType(arg_types), node.receiver.type)

    def visit_replicated_input_process_node(self, node: ReplicatedInputProcessNode):
        node.receiver.accept(self)
        if node.receiver.type is None:
            raise TypingException("Unknown type of input channel", node)
        if not isinstance(node.receiver.type, ChannelType):
            raise TypingException("Input is not a channel type", node)
        if len(node.identifiers) != len(node.receiver.type.message_type.arg_types):
            raise TypingException("Invalid number of messages, expected {} got {}".format(
                    len(node.receiver.type.message_type.arg_types),
                    len(node.identifiers)),
                node)
        for i, identifier in enumerate(node.identifiers):
            identifier.type = node.receiver.type.message_type.arg_types[i]
        node.continuation.accept(self)

    def visit_conditional_node(self, node: ConditionalNode):
        node.predicate.accept(self)
        if node.predicate.type != Type.BOOL:
            raise WrongTypeException(Type.BOOL, actual_type=node.predicate.type)
        node.true_branch.accept(self)
        node.false_branch.accept(self)

    def visit_extern_process_node(self, node: ExternProcessNode):
        node.internal_name.type = node.arg_types
        return super().visit_extern_process_node(node)

    def visit_binary_expression_node(self, node: BinaryExpressionNode):
        node.left.accept(self)
        node.right.accept(self)
        int_to_int = {
            BinaryExpressionNode.POWER,
            BinaryExpressionNode.MULTIPLICATION,
            BinaryExpressionNode.DIVISION,
            BinaryExpressionNode.SUBTRACTION,
            BinaryExpressionNode.ADDITION
        }
        if node.operation in int_to_int:
            if node.left.type != Type.INT:
                raise WrongTypeException(Type.INT, node.left.type, node.left)
            if node.right.type != Type.INT:
                raise WrongTypeException(Type.INT, node.right.type, node.right)
            node.type = Type.INT
            return
        return super().visit_binary_expression_node(node)

