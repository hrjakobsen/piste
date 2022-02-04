from parser.auto.pisteVisitor import pisteVisitor
from parser.auto.pisteParser import *
from parser.core import *
from typechecker import TypeReference


def get_node_pos(ctx: ParserRuleContext):
    return (ctx.start.line, ctx.start.column), (ctx.stop.line, ctx.stop.column)


class CoreBuilder(pisteVisitor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.declarations = {}

    def visitOutput(self, ctx: pisteParser.OutputContext):
        receiver = ctx.receiver.accept(self)
        messages = []
        for message in ctx.expression()[1:]:
            messages.append(message.accept(self))
        return OutputProcessNode(receiver, messages, code_position=get_node_pos(ctx))

    def visitInput(self, ctx: pisteParser.InputContext):
        receiver = ctx.expression().accept(self)
        identifiers = []
        for identifier in ctx.identifier_with_type():
            identifiers.append(identifier.accept(self))
        continuation = ctx.process().accept(self)
        return InputProcessNode(receiver, identifiers, continuation, code_position=get_node_pos(ctx))

    def visitParen(self, ctx: pisteParser.ParenContext):
        return ctx.process().accept(self)

    def visitInaction(self, ctx: pisteParser.InactionContext):
        return InactionProcessNode(code_position=get_node_pos(ctx))

    def visitParallel(self, ctx: pisteParser.ParallelContext):
        return ParallelProcessNode(ctx.left.accept(self), ctx.right.accept(self), code_position=get_node_pos(ctx))

    def visitRestriction(self, ctx: pisteParser.RestrictionContext):
        identifier = Identifier(ctx.IDENTIFIER().getText())
        typ = ctx.type_name().accept(self)
        identifier.type = typ
        continuation = ctx.process().accept(self)
        return RestrictionProcessNode(identifier, typ, continuation, code_position=get_node_pos(ctx))

    def visitTrue_val(self, ctx: pisteParser.True_valContext):
        return TrueValueNode(type=Type.BOOL, code_position=get_node_pos(ctx))

    def visitRecord_val(self, ctx: pisteParser.Record_valContext):
        return ctx.record().accept(self)

    def visitString_val(self, ctx: pisteParser.String_valContext):
        return StringValueNode(ctx.STRING().getText()[1:-1], type=Type.STRING, code_position=get_node_pos(ctx))

    def visitInt_val(self, ctx: pisteParser.Int_valContext):
        a = ctx.getSourceInterval()
        return IntegerValueNode(ctx.INTEGER().getText(), type=Type.INT, code_position=get_node_pos(ctx))

    def visitFalse_val(self, ctx: pisteParser.False_valContext):
        return FalseValueNode(type=Type.BOOL, code_position=get_node_pos(ctx))

    def visitIdentifier_val(self, ctx: pisteParser.Identifier_valContext):
        return IdentifierValueNode(ctx.IDENTIFIER().getText(), code_position=get_node_pos(ctx))

    # def visitPath_val(self, ctx: pisteParser.Path_valContext):
    #     return PathNode(ctx.expression().accept(self), IdentifierNode(ctx.IDENTIFIER(1).getText()), IdentifierNode(ctx.IDENTIFIER(0)))

    def visitRecord(self, ctx: pisteParser.RecordContext):
        entries = []
        for (name, val_node) in zip(ctx.IDENTIFIER()[:-1], ctx.expression()):
            entries.append((name.getText(), val_node.accept(self)))
        type = TypeReference((ctx.IDENTIFIER()[-1].getText()))
        return RecordNode(entries, type, code_position=get_node_pos(ctx))

    def visitReplicated_input(self, ctx:pisteParser.Replicated_inputContext):
        receiver = ctx.expression().accept(self)
        identifiers = []
        for identifier in ctx.identifier_with_type():
            identifiers.append(identifier.accept(self))
        continuation = ctx.process().accept(self)
        return ReplicatedInputProcessNode(receiver, identifiers, continuation, code_position=get_node_pos(ctx))

    def visitProcess_def(self, ctx: pisteParser.Process_defContext):
        body = ctx.body.accept(self)
        continuation = ctx.continuation.accept(self)
        name = Identifier(ctx.IDENTIFIER().getText())
        args = [i.accept(self) for i in ctx.identifier_with_type()]
        arg_types = list(map(lambda x: x.type, args))
        return RestrictionProcessNode(
            name,
            ChannelType(MessageType(arg_types)),
            ParallelProcessNode(
                ReplicatedInputProcessNode(IdentifierValueNode(name.name, code_position=get_node_pos(ctx)), args, body),
                continuation,
                code_position=get_node_pos(ctx))
        )

    def visitConditional(self, ctx: pisteParser.ConditionalContext):
        return ConditionalNode(
            ctx.expression().accept(self),
            ctx.true_branch.accept(self),
            ctx.false_branch.accept(self) if ctx.false_branch else InactionProcessNode(),
            code_position=get_node_pos(ctx)
        )

    def visitExtern_declaration(self, ctx: pisteParser.Extern_declarationContext):
        external_name = Identifier(ctx.IDENTIFIER(0).getText())
        internal_name = Identifier(ctx.IDENTIFIER(1).getText())
        types = [typ.accept(self) for typ in ctx.type_name()[:-1]]
        ret_type = ctx.type_name()[-1].accept(self)
        decl = ExternalDeclaration(
            external_name,
            ChannelType(MessageType(types + [ChannelType(MessageType(ret_type))])),
            ChannelType(MessageType(ret_type)),
            internal_name
        )
        self.declarations[internal_name] = decl
        return decl

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
                decl["arg_type"],
                decl["function"],
                decl["args"],
                next_process,
                ctx
            )

        return next_process

    def visitCall_binding(self, ctx: pisteParser.Call_bindingContext):
        identifier = ctx.identifier_with_type().accept(self) if ctx.identifier_with_type() else Identifier("_")
        return {
            "type": "FUNCTION",
            "variable": identifier,
            "arg_type": identifier.type,
            "function": ctx.expression(0).accept(self),
            "args": [arg.accept(self) for arg in ctx.expression()[1:]]
        }


    def visitSimple_value_binding(self, ctx: pisteParser.Simple_value_bindingContext):
        # let x = 4
        identifier = ctx.identifier_with_type().accept(self) if ctx.identifier_with_type() else Identifier("_")
        return {
            "type": "SIMPLE",
            "variable": identifier,
            "arg_type": identifier.type,
            "function": None,
            "args": [ctx.expression().accept(self)]
        }

    def generate_binding(self, type, variable, arg_type, channel, args, continuation, ctx):
        channel_name = "fresh"
        if type == "FUNCTION":
            return RestrictionProcessNode(
                Identifier(channel_name, typ=ChannelType(MessageType(variable.type)) if variable.type else None),
                ChannelType(MessageType(arg_type)),
                ParallelProcessNode(
                    OutputProcessNode(channel, args + [IdentifierValueNode(channel_name, code_position=get_node_pos(ctx))], code_position=get_node_pos(ctx)),
                    InputProcessNode(IdentifierValueNode(channel_name, code_position=get_node_pos(ctx)), [variable], continuation, code_position=get_node_pos(ctx))
                )
            )
        elif type == "SIMPLE":
            return RestrictionProcessNode(
                Identifier(channel_name),
                args[0].type,
                ParallelProcessNode(
                    OutputProcessNode(IdentifierValueNode(channel_name), args),
                    InputProcessNode(IdentifierValueNode(channel_name, code_position=get_node_pos(ctx)), [variable], continuation)
                )
            )

    def visitReturn(self, ctx: pisteParser.ReturnContext):
        args = [ctx.expression().accept(self)]
        return OutputProcessNode(IdentifierValueNode("return_chn"), args, code_position=get_node_pos(ctx))

    def visitFunction_def(self, ctx: pisteParser.Function_defContext):
        name = Identifier(ctx.IDENTIFIER(0).getText())
        arg_types = [typ.accept(self) for typ in ctx.type_name()[:-1]]
        args = [Identifier(arg.getText(), typ=arg_types[i]) for i, arg in enumerate(ctx.IDENTIFIER()[1:])]
        ret_type = ChannelType(MessageType([ctx.type_name()[-1].accept(self)]))
        name.type = ChannelType(MessageType(arg_types + [ret_type]))
        body = ctx.body.accept(self)
        continuation = ctx.continuation.accept(self)
        return RestrictionProcessNode(
            name,
            ChannelType(MessageType(arg_types + [ret_type])),
            ParallelProcessNode(
                ReplicatedInputProcessNode(IdentifierValueNode(name.name), args + [Identifier("return_chn", typ=ret_type)], body),
                continuation),
            code_position=get_node_pos(ctx)
        )

    def visitParen_expr(self, ctx: pisteParser.Paren_exprContext):
        return ctx.expression().accept(self)

    def visitOperator_pow_expr(self, ctx: pisteParser.Operator_pow_exprContext):
        return BinaryExpressionNode(
            ctx.expression(0).accept(self),
            ctx.expression(1).accept(self),
            BinaryExpressionNode.POWER,
            get_node_pos(ctx)
        )

    def visitOperator_as_expr(self, ctx: pisteParser.Operator_as_exprContext):
        return BinaryExpressionNode(
            ctx.expression(0).accept(self),
            ctx.expression(1).accept(self),
            BinaryExpressionNode.ADDITION if ctx.ADD() else BinaryExpressionNode.SUBTRACTION,
            code_position=get_node_pos(ctx)
        )

    def visitOperator_md_expr(self, ctx: pisteParser.Operator_md_exprContext):
        return BinaryExpressionNode(
            ctx.expression(0).accept(self),
            ctx.expression(1).accept(self),
            BinaryExpressionNode.MULTIPLICATION if ctx.MULT() else BinaryExpressionNode.DIVISION,
            code_position=get_node_pos(ctx)
        )

    def visitLiteral(self, ctx: pisteParser.LiteralContext):
        return ctx.value().accept(self)

    def visitImport_statement(self, ctx: pisteParser.Import_statementContext):
        return ctx.STRING().getText()[1:-1]

    def visitProgram(self, ctx: pisteParser.ProgramContext):
        imports = [import_entry.accept(self) for import_entry in ctx.import_statement()]
        declarations = [decl.accept(self) for decl in ctx.declaration()]
        if ctx.process():
            process = ctx.process().accept(self)
        else:
            process = None
        return process, declarations, imports

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

    def visitType_void(self, ctx: pisteParser.Type_voidContext):
        return Type.VOID

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

    def visitIdentifier_with_type(self, ctx: pisteParser.Identifier_with_typeContext):
        id = Identifier(ctx.IDENTIFIER().getText())
        if ctx.type_name():
            id.type = ctx.type_name().accept(self)
        return id





