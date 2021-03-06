from parser.core import AstVisitor, BinaryExpressionNode, PathNode, ExternProcessNode, ConditionalNode, \
    ReplicatedInputProcessNode, InactionProcessNode, RestrictionProcessNode, ParallelProcessNode, OutputProcessNode, \
    InputProcessNode, RecordNode, IdentifierValueNode, IntegerValueNode, StringValueNode, FalseValueNode, TrueValueNode, \
    MessageType, ChannelType, Type, ListAccessNode, ListCreationNode, ListType


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
        types = {
            BinaryExpressionNode.POWER: [Type.INT, Type.INT, Type.INT],
            BinaryExpressionNode.MULTIPLICATION: [Type.INT, Type.INT, Type.INT],
            BinaryExpressionNode.DIVISION: [Type.INT, Type.INT, Type.INT],
            BinaryExpressionNode.SUBTRACTION: [Type.INT, Type.INT, Type.INT],
            BinaryExpressionNode.ADDITION: [Type.INT, Type.INT, Type.INT],
            BinaryExpressionNode.EQ: [Type.INT, Type.INT, Type.BOOL],
            BinaryExpressionNode.NEQ: [Type.INT, Type.INT, Type.BOOL],
            BinaryExpressionNode.AND: [Type.BOOL, Type.BOOL, Type.BOOL],
            BinaryExpressionNode.OR: [Type.BOOL, Type.BOOL, Type.BOOL],
        }

        if node.operation in types:
            typ = types[node.operation]
            if node.left.type != typ[0]:
                raise WrongTypeException(typ[0], node.left.type, node.left)
            if node.right.type != typ[1]:
                raise WrongTypeException(typ[1], node.right.type, node.right)
            node.type = typ[2]
            return
        elif node.operation == BinaryExpressionNode.APPEND:
            if not isinstance(node.left.type, ListType):
                raise TypingException("Left operand of ++ must be a list", node.left)
            if not node.left.type.is_equal_to(node.right.type):
                raise WrongTypeException(node.left.type, node.right.type, node)
            node.type = node.left.type
            return
        raise Exception("Invalid binary operation {}".format(node.operation))

    def visit_restriction_process_node(self, node: RestrictionProcessNode):
        node.identifier.type = node.channel_type
        super().visit_restriction_process_node(node)

    def visit_list_creation_node(self, node: ListCreationNode):
        if len(node.element_expressions) == 0:
            node.type = Type.EMPTY_LIST
            return Type.EMPTY_LIST
        element_types = []
        for element_expression in node.element_expressions:
            element_expression.accept(self)
            element_types.append(element_expression.type)
            if not element_types[0].is_equal_to(element_expression.type):
                raise TypingException("Values in a list must be of the same type")
        node.type = ListType(element_types[0])
        return node.type

    def visit_list_access_node(self, node: ListAccessNode):
        node.target_list.accept(self)
        list_type = node.target_list.type
        if not isinstance(list_type, ListType):
            raise TypingException("Accessing element in non-list type", node)
        node.index_expression.accept(self)
        index_type = node.index_expression.type
        if index_type != Type.INT:
            raise TypingException("Index must be a number", node)
        if list_type == Type.EMPTY_LIST:
            raise TypingException("Can't dereference empty list", node)
        node.type = list_type.element_type
        return list_type.element_type

