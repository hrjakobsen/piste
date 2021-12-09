from parser.auto.pisteVisitor import pisteVisitor
from parser.auto.pisteParser import *
from parser.core import *


class CoreBuilder(pisteVisitor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.declarations = {}
        self.num = 0

    def visitOutput(self, ctx: pisteParser.OutputContext):
        receiver = ctx.receiver.accept(self)
        messages = []
        for message in ctx.expression()[1:]:
            messages.append(message.accept(self))
        return OutputProcessNode(receiver, messages)

    def visitInput(self, ctx: pisteParser.InputContext):
        receiver = ctx.expression().accept(self)
        identifiers = []
        for identifier in ctx.IDENTIFIER():
            identifiers.append(IdentifierNode(identifier.getText()))
        continuation = ctx.process().accept(self)
        return InputProcessNode(receiver, identifiers, continuation)

    def visitParen(self, ctx: pisteParser.ParenContext):
        return ctx.process().accept(self)

    def visitInaction(self, ctx: pisteParser.InactionContext):
        return InactionProcessNode()

    def visitParallel(self, ctx: pisteParser.ParallelContext):
        return ParallelProcessNode(ctx.left.accept(self), ctx.right.accept(self))

    def visitRestriction(self, ctx: pisteParser.RestrictionContext):
        identifier = IdentifierNode(ctx.IDENTIFIER().getText())
        typ = ctx.type_name().accept(self)
        continuation = ctx.process().accept(self)
        return RestrictionProcessNode(identifier, typ, continuation)

    def visitTrue_val(self, ctx: pisteParser.True_valContext):
        return TrueValueNode(type=Type.BOOL)

    def visitRecord_val(self, ctx: pisteParser.Record_valContext):
        return ctx.record().accept(self)

    def visitString_val(self, ctx: pisteParser.String_valContext):
        return StringValueNode(ctx.STRING().getText()[1:-1], type=Type.STRING)

    def visitInt_val(self, ctx: pisteParser.Int_valContext):
        return IntegerValueNode(ctx.INTEGER().getText(), type=Type.INT)

    def visitFalse_val(self, ctx: pisteParser.False_valContext):
        return FalseValueNode(type=Type.BOOL)

    def visitIdentifier_val(self, ctx: pisteParser.Identifier_valContext):
        return IdentifierNode(ctx.IDENTIFIER().getText())

    # def visitPath_val(self, ctx: pisteParser.Path_valContext):
    #     return PathNode(ctx.expression().accept(self), IdentifierNode(ctx.IDENTIFIER(1).getText()), IdentifierNode(ctx.IDENTIFIER(0)))

    def visitRecord(self, ctx: pisteParser.RecordContext):
        entries = []
        for (name, val_node) in zip(ctx.IDENTIFIER()[:-1], ctx.expression()):
            entries.append((name.getText(), val_node.accept(self)))
        type = IdentifierNode(ctx.IDENTIFIER()[-1].getText())
        return RecordNode(entries, type)

    def visitReplicated_input(self, ctx:pisteParser.Replicated_inputContext):
        receiver = ctx.expression().accept(self)
        identifiers = []
        for identifier in ctx.IDENTIFIER():
            identifiers.append(IdentifierNode(identifier.getText()))
        continuation = ctx.process().accept(self)
        return ReplicatedInputProcessNode(receiver, identifiers, continuation)

    def visitProcess_def(self, ctx: pisteParser.Process_defContext):
        body = ctx.body.accept(self)
        continuation = ctx.continuation.accept(self)
        name = IdentifierNode(ctx.IDENTIFIER(0).getText())
        args = list(map(lambda i: IdentifierNode(i.getText()), ctx.IDENTIFIER()[1:]))
        return RestrictionProcessNode(
            name,
            ParallelProcessNode(
                ReplicatedInputProcessNode(name, args, body),
                continuation)
        )

    def visitConditional(self, ctx: pisteParser.ConditionalContext):
        return ConditionalNode(
            ctx.expression().accept(self),
            ctx.true_branch.accept(self),
            ctx.false_branch.accept(self) if ctx.false_branch else InactionProcessNode()
        )

    def visitExtern_def(self, ctx:pisteParser.Extern_defContext):
        external_name = IdentifierNode(ctx.IDENTIFIER(0).getText())
        internal_name = IdentifierNode(ctx.IDENTIFIER(1).getText())
        types = [typ.accept(self) for typ in ctx.type_name()[:-1]]
        ret_type = ctx.type_name()[-1]
        continuation = ctx.continuation.accept(self)
        return ExternProcessNode(
            external_name,
            types,
            ret_type,
            internal_name,
            continuation
        )

    def visitLet_binding(self, ctx: pisteParser.Let_bindingContext):
        bindings = []
        for binding in ctx.value_binding():
            bindings.append(binding.accept(self))

        continuation = ctx.process().accept(self)

        next_process = continuation
        for decl in reversed(bindings):
            next_process = self.generate_binding(
                decl["type"],
                decl["variable"],
                decl["function"],
                decl["args"],
                next_process
            )

        return next_process

    def visitCall_binding(self, ctx: pisteParser.Call_bindingContext):
        return {
            "type": "FUNCTION",
            "variable": IdentifierNode(ctx.IDENTIFIER().getText()) if ctx.IDENTIFIER() else IdentifierNode("_"),
            "function": ctx.expression(0).accept(self),
            "args": [arg.accept(self) for arg in ctx.expression()[1:]]
        }


    def visitSimple_value_binding(self, ctx: pisteParser.Simple_value_bindingContext):
        # let x = 4
        return {
            "type": "SIMPLE",
            "variable": IdentifierNode(ctx.IDENTIFIER().getText()),
            "function": None,
            "args": [ctx.expression().accept(self)]
        }

    def generate_binding(self, type, variable, channel, args, continuation):
        channel_name = IdentifierNode("fresh_" + str(self.num))
        self.num += 1
        if type == "FUNCTION":
            return RestrictionProcessNode(
                channel_name,
                args[0].type,
                ParallelProcessNode(
                    OutputProcessNode(channel, args + [channel_name]),
                    InputProcessNode(channel_name, [variable], continuation)
                )
            )
        elif type == "SIMPLE":
            return RestrictionProcessNode(
                channel_name,
                args[0].type,
                ParallelProcessNode(
                    OutputProcessNode(channel_name, args),
                    InputProcessNode(channel_name, [variable], continuation)
                )
            )

    def visitReturn(self, ctx: pisteParser.ReturnContext):
        args = [ctx.expression().accept(self)]
        return OutputProcessNode(IdentifierNode("return_chn"), args)

    def visitFunction_def(self, ctx: pisteParser.Function_defContext):
        name = IdentifierNode(ctx.IDENTIFIER(0).getText())
        args = [IdentifierNode(arg.getText()) for arg in ctx.IDENTIFIER()[1:]]
        arg_types = [typ.accept(self) for typ in ctx.type_name()[:-1]]
        ret_type = ChannelType(MessageType([ctx.type_name()[-1].accept(self)]))
        body = ctx.body.accept(self)
        continuation = ctx.continuation.accept(self)
        return RestrictionProcessNode(
            name,
            ChannelType(MessageType(arg_types + [ret_type])),
            ParallelProcessNode(
                ReplicatedInputProcessNode(name, args + [IdentifierNode("return_chn")], body),
                continuation)
        )

    def visitParen_expr(self, ctx: pisteParser.Paren_exprContext):
        return ctx.expression().accept(self)

    def visitOperator_pow_expr(self, ctx: pisteParser.Operator_pow_exprContext):
        return BinaryExpressionNode(
            ctx.expression(0).accept(self),
            ctx.expression(1).accept(self),
            BinaryExpressionNode.POWER
        )

    def visitOperator_as_expr(self, ctx: pisteParser.Operator_as_exprContext):
        return BinaryExpressionNode(
            ctx.expression(0).accept(self),
            ctx.expression(1).accept(self),
            BinaryExpressionNode.ADDITION if ctx.ADD() else BinaryExpressionNode.SUBTRACTION
        )

    def visitOperator_md_expr(self, ctx: pisteParser.Operator_md_exprContext):
        return BinaryExpressionNode(
            ctx.expression(0).accept(self),
            ctx.expression(1).accept(self),
            BinaryExpressionNode.MULTIPLICATION if ctx.MULT() else BinaryExpressionNode.DIVISION
        )

    def visitLiteral(self, ctx: pisteParser.LiteralContext):
        return ctx.value().accept(self)

    def visitProgram(self, ctx: pisteParser.ProgramContext):
        declarations = [decl.accept(self) for decl in ctx.declaration()]
        process = ctx.process().accept(self)
        return (declarations, process)

    def visitDeclaration(self, ctx: pisteParser.DeclarationContext):
        # visit the singular child
        return super().visitDeclaration(ctx)

    def visitRecord_declaration(self, ctx: pisteParser.Record_declarationContext):
        record_name = ctx.IDENTIFIER(0)
        record_entries = []
        for (identifier_node, type_node) in zip(ctx.IDENTIFIER()[1:], ctx.type_name()):
            record_entries.append((identifier_node.getText(), type_node.accept(self)))
        typ = RecordType(record_name, record_entries)
        self.declarations[record_name] = typ
        return typ

    def visitType_int(self, ctx: pisteParser.Type_intContext):
        return Type.INT

    def visitType_bool(self, ctx: pisteParser.Type_boolContext):
        return Type.BOOL

    def visitType_string(self, ctx: pisteParser.Type_stringContext):
        return Type.STRING

    def visitType_channel(self, ctx: pisteParser.Type_channelContext):
        return ChannelType(ctx.message_type().accept(self))

    def visitType_identifier(self, ctx: pisteParser.Type_identifierContext):
        return self.get_declared_type(ctx.IDENTIFIER().getText())

    def visitMessage_type(self, ctx: pisteParser.Message_typeContext):
        return MessageType([typ.accept(self) for typ in ctx.type_name()])

    def get_declared_type(self, type_name):
        assert type_name in self.declarations
        return self.declarations[type_name]



