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
    EQ = '=='
    NEQ = '!='
    AND = '&&'
    OR = '||'
    SUBTRACTION = '-'
    MULTIPLICATION = '*'
    APPEND = '++'
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


class ListCreationNode(ExpressionNode):
    def __init__(self, element_expressions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.element_expressions = element_expressions

    def __str__(self):
        "[{}]".format(", ".join(map(str, self.element_expressions)))

    def accept(self, visitor):
        return visitor.visit_list_creation_node(self)


class ListAccessNode(ExpressionNode):
    def __init__(self, target_list, index_expression, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_list = target_list
        self.index_expression = index_expression

    def __str__(self):
        "{}[{}]".format(self.target_list, self.index_expression)

    def accept(self, visitor):
        return visitor.visit_list_access_node(self)


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


class ExternalDeclaration:
    def __init__(self, external_name, arg_types, ret_type, internal_name):
        self.external_name = external_name
        self.arg_types = arg_types
        self.ret_type = ret_type
        self.internal_name = internal_name

    def wrap(self, continuation):
        extended = ExternProcessNode(
            self.external_name,
            self.arg_types,
            self.ret_type,
            self.internal_name,
            continuation
        )
        return extended


class ProcessDeclaration:
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body

    def wrap(self, continuation):
        arg_types = list(map(lambda x: x.type, self.args))
        return RestrictionProcessNode(
            self.name,
            ChannelType(MessageType(arg_types)),
            ParallelProcessNode(
                ReplicatedInputProcessNode(IdentifierValueNode(self.name.name), self.args, self.body),
                continuation
            )
        )


class Type:
    INT = None
    BOOL = None
    STRING = None
    VOID = None
    EMPTY_LIST = None

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


class VoidType(Type):
    def __str__(self):
        return "void"


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


class ListType(Type):
    def __init__(self, element_type):
        self.element_type = element_type

    def __str__(self):
        return "{}[]".format(self.element_type)

    def is_equal_to(self, other_type):
        is_other_list = isinstance(other_type, ListType)
        return is_other_list and other_type.element_type.is_equal_to(self.element_type)


Type.INT = IntegerType()
Type.BOOL = BoolType()
Type.STRING = StringType()
Type.VOID = VoidType()
Type.EMPTY_LIST = ListType(None)


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
        node.predicate.accept(self)
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

    def visit_list_creation_node(self, node: ListCreationNode):
        last = None
        for element_expression in node.element_expressions:
            last = element_expression.accept(self)
        return last

    def visit_list_access_node(self, node: ListAccessNode):
        node.target_list.accept(self)
        return node.index_expression.accept(self)
