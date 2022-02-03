# Generated from /home/mathias/gitrepos/piste/compiler/piste.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .pisteParser import pisteParser
else:
    from pisteParser import pisteParser

# This class defines a complete generic visitor for a parse tree produced by pisteParser.

class pisteVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by pisteParser#program.
    def visitProgram(self, ctx:pisteParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#declaration.
    def visitDeclaration(self, ctx:pisteParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#record_declaration.
    def visitRecord_declaration(self, ctx:pisteParser.Record_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#type_int.
    def visitType_int(self, ctx:pisteParser.Type_intContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#type_bool.
    def visitType_bool(self, ctx:pisteParser.Type_boolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#type_void.
    def visitType_void(self, ctx:pisteParser.Type_voidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#type_string.
    def visitType_string(self, ctx:pisteParser.Type_stringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#type_channel.
    def visitType_channel(self, ctx:pisteParser.Type_channelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#type_identifier.
    def visitType_identifier(self, ctx:pisteParser.Type_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#message_type.
    def visitMessage_type(self, ctx:pisteParser.Message_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#process_def.
    def visitProcess_def(self, ctx:pisteParser.Process_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#inaction.
    def visitInaction(self, ctx:pisteParser.InactionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#conditional.
    def visitConditional(self, ctx:pisteParser.ConditionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#extern_def.
    def visitExtern_def(self, ctx:pisteParser.Extern_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#output.
    def visitOutput(self, ctx:pisteParser.OutputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#replicated_input.
    def visitReplicated_input(self, ctx:pisteParser.Replicated_inputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#function_def.
    def visitFunction_def(self, ctx:pisteParser.Function_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#input.
    def visitInput(self, ctx:pisteParser.InputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#paren.
    def visitParen(self, ctx:pisteParser.ParenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#let_binding.
    def visitLet_binding(self, ctx:pisteParser.Let_bindingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#parallel.
    def visitParallel(self, ctx:pisteParser.ParallelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#restriction.
    def visitRestriction(self, ctx:pisteParser.RestrictionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#return.
    def visitReturn(self, ctx:pisteParser.ReturnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#call_binding.
    def visitCall_binding(self, ctx:pisteParser.Call_bindingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#simple_value_binding.
    def visitSimple_value_binding(self, ctx:pisteParser.Simple_value_bindingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#identifier_with_type.
    def visitIdentifier_with_type(self, ctx:pisteParser.Identifier_with_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#paren_expr.
    def visitParen_expr(self, ctx:pisteParser.Paren_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#operator_pow_expr.
    def visitOperator_pow_expr(self, ctx:pisteParser.Operator_pow_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#operator_as_expr.
    def visitOperator_as_expr(self, ctx:pisteParser.Operator_as_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#operator_md_expr.
    def visitOperator_md_expr(self, ctx:pisteParser.Operator_md_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#literal.
    def visitLiteral(self, ctx:pisteParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#true_val.
    def visitTrue_val(self, ctx:pisteParser.True_valContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#false_val.
    def visitFalse_val(self, ctx:pisteParser.False_valContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#string_val.
    def visitString_val(self, ctx:pisteParser.String_valContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#identifier_val.
    def visitIdentifier_val(self, ctx:pisteParser.Identifier_valContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#record_val.
    def visitRecord_val(self, ctx:pisteParser.Record_valContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#int_val.
    def visitInt_val(self, ctx:pisteParser.Int_valContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pisteParser#record.
    def visitRecord(self, ctx:pisteParser.RecordContext):
        return self.visitChildren(ctx)



del pisteParser