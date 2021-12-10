# The core language

class AstNode:
    def __init__(self, code_position = None):
        self.code_position = code_position
        self.free_variables = list()


class ExpressionNode(AstNode):
    def __init__(self, *args, **kwargs):
        if "type" in kwargs:
            self.type = kwargs.pop("type")
        else:
            self.type = None
        super().__init__(*args, **kwargs)


class ValueNode(ExpressionNode):
    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value


class BinaryExpressionNode(ExpressionNode):
    ADDITION = '+'
    SUBTRACTION = '-'
    MULTIPLICATION = '*'
    DIVISION = '/'
    POWER = '**'

    def __init__(self, left, right, operation, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.left = left
        self.right = right
        self.operation = operation

    def accept(self, visitor):
        return visitor.visit_binary_expression_node(self)


class RecordNode(ValueNode):
    def __init__(self, values, type, *args, **kwargs):
        super(RecordNode, self).__init__(values, *args, **kwargs)
        self.name = None
        self.type = type

    def accept(self, visitor):
        return visitor.visit_record_node(self)


class PathNode(ValueNode):
    def __init__(self, value, field_name, type, *args, **kwargs):
        super().__init__(value, *args, **kwargs)
        self.field_name = field_name
        self.type = type

    def accept(self, visitor):
        return visitor.visit_path_node(self)


class TrueValueNode(ValueNode):
    def __init__(self, *args, **kwargs):
        super().__init__(True, *args, **kwargs)

    def accept(self, visitor):
        return visitor.visit_true_value_node(self)


class FalseValueNode(ValueNode):
    def __init__(self, *args, **kwargs):
        super().__init__(False, *args, **kwargs)

    def accept(self, visitor):
        return visitor.visit_false_value_node(self)


class StringValueNode(ValueNode):
    def __init__(self, value, *args, **kwargs):
        super().__init__(value, *args, **kwargs)

    def accept(self, visitor):
        return visitor.visit_string_value_node(self)


class Identifier:
    def __init__(self, name, typ=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.type = typ


class IntegerValueNode(ValueNode):
    def __init__(self, value, *args, **kwargs):
        super().__init__(int(value), *args, **kwargs)

    def accept(self, visitor):
        return visitor.visit_integer_value_node(self)


class IdentifierValueNode(ValueNode):
    def __init__(self, identifier, *args, **kwargs):
        super().__init__(identifier, *args, **kwargs)
        self.identifier_declaration = None

    def accept(self, visitor):
        return visitor.visit_identifier_node(self)


class ConditionalNode(AstNode):
    def __init__(self, predicate, true_branch, false_branch, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.predicate = predicate
        self.true_branch = true_branch
        self.false_branch = false_branch

    def accept(self, visitor):
        return visitor.visit_conditional_node(self)


class ProcessNode(AstNode):
    def __init__(self, name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name


class ExternProcessNode(ProcessNode):
    def __init__(self, external_name, arg_types, ret_type, internal_name, continuation, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.external_name = external_name
        self.arg_types = arg_types
        self.ret_type= ret_type
        self.internal_name = internal_name
        self.continuation = continuation

    def accept(self, visitor):
        return visitor.visit_extern_process_node(self)


class InputProcessNode(ProcessNode):
    def __init__(self, receiver, identifiers, continuation, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.receiver = receiver
        self.identifiers = identifiers
        self.continuation = continuation

    def accept(self, visitor):
        return visitor.visit_input_process_node(self)


class ReplicatedInputProcessNode(ProcessNode):
    def __init__(self, receiver, identifiers, continuation, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.receiver = receiver
        self.identifiers = identifiers
        self.continuation = continuation

    def accept(self, visitor):
        return visitor.visit_replicated_input_process_node(self)


class OutputProcessNode(ProcessNode):
    def __init__(self, receiver, values, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.receiver = receiver
        self.values = values

    def accept(self, visitor):
        return visitor.visit_output_process_node(self)


class ParallelProcessNode(ProcessNode):
    def __init__(self, left, right, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_parallel_process_node(self)


class RestrictionProcessNode(ProcessNode):
    def __init__(self, identifier, channel_type, continuation, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.identifier = identifier
        self.channel_type = channel_type
        self.continuation = continuation

    def accept(self, visitor):
        return visitor.visit_restriction_process_node(self)


class InactionProcessNode(ProcessNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def accept(self, visitor):
        return visitor.visit_inaction_process_node(self)


class Type:
    INT = None
    BOOL = None
    STRING = None

    def is_equal_to(self, other_type):
        return self == other_type

    def __repr__(self):
        return self.__str__()


class IntegerType(Type):
    def __str__(self):
        return "int"


class BoolType(Type):
    def __str__(self):
        return "bool"


class StringType(Type):
    def __str__(self):
        return "string"


class MessageType(Type):
    def __init__(self, arg_types):
        if not isinstance(arg_types, list):
            arg_types = [arg_types]
        self.arg_types = arg_types

    def __str__(self):
        return "[{}]".format(", ".join(map(str, self.arg_types)))

    def is_equal_to(self, other_type):
        # Check pairwise equality with other channel
        is_msg_type = isinstance(other_type, MessageType)
        if not is_msg_type:
            return False
        if not len(other_type.arg_types) == len(self.arg_types):
            return False
        for typ, other_typ in zip(self.arg_types, other_type.arg_types):
            if not typ.is_equal_to(other_typ):
                return False
        return True


class ChannelType(Type):
    def __init__(self, message_type: MessageType):
        self.message_type = message_type

    def is_equal_to(self, other_type):
        # Check pairwise equality with other channel
        is_other_channel = isinstance(other_type, ChannelType)

        if not is_other_channel:
            return False

        return self.message_type.is_equal_to(other_type.message_type)

    def __str__(self):
        return "^{}".format(self.message_type)


class RecordType(Type):
    def __init__(self, name, entries):
        self.name = name
        self.entries = entries

    def __str__(self):
        return "record[{}]".format(self.name)


Type.INT = IntegerType()
Type.BOOL = BoolType()
Type.STRING = StringType()


class AstVisitor:
    def visit_true_value_node(self, node: TrueValueNode):
        return

    def visit_false_value_node(self, node: FalseValueNode):
        return

    def visit_string_value_node(self, node: StringValueNode):
        return

    def visit_integer_value_node(self, node: IntegerValueNode):
        return

    def visit_identifier_node(self, node: IdentifierValueNode):
        return

    def visit_record_node(self, node: RecordNode):
        return

    def visit_input_process_node(self, node: InputProcessNode):
        node.receiver.accept(self)
        return node.continuation.accept(self)

    def visit_output_process_node(self, node: OutputProcessNode):
        res = node.receiver.accept(self)
        for value in node.values:
            res = value.accept(self)
        return res

    def visit_parallel_process_node(self, node: ParallelProcessNode):
        node.left.accept(self)
        return node.right.accept(self)

    def visit_restriction_process_node(self, node: RestrictionProcessNode):
        return node.continuation.accept(self)

    def visit_inaction_process_node(self, node: InactionProcessNode):
        return

    def visit_replicated_input_process_node(self, node: ReplicatedInputProcessNode):
        node.receiver.accept(self)
        return node.continuation.accept(self)

    def visit_conditional_node(self, node: ConditionalNode):
        node.true_branch.accept(self)
        return node.false_branch.accept(self)

    def visit_extern_process_node(self, node: ExternProcessNode):
        return node.continuation.accept(self)

    def visit_path_node(self, node: PathNode):
        node.value.accept(self)
        return node.field_name.accept(self)

    def visit_binary_expression_node(self, node: BinaryExpressionNode):
        node.left.accept(self)
        return node.right.accept(self)