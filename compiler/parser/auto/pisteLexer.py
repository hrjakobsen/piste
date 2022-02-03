# Generated from /home/mathias/gitrepos/piste/compiler/piste.g4 by ANTLR 4.9.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\62")
        buf.write("\u012d\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.")
        buf.write("\t.\4/\t/\4\60\t\60\4\61\t\61\3\2\3\2\3\3\3\3\3\3\3\4")
        buf.write("\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\t\3\n\3")
        buf.write("\n\3\n\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\f\3\f\3\f")
        buf.write("\3\f\3\f\3\f\3\r\3\r\3\r\3\16\3\16\3\16\3\16\3\16\3\16")
        buf.write("\3\16\3\17\3\17\3\17\3\20\3\20\3\20\3\20\3\20\3\21\3\21")
        buf.write("\3\21\3\21\3\21\3\22\3\22\3\23\3\23\3\23\3\23\3\24\3\24")
        buf.write("\3\24\3\24\3\24\3\24\3\24\3\25\3\25\3\25\3\25\3\26\3\26")
        buf.write("\3\27\3\27\3\30\3\30\3\30\3\31\3\31\3\32\3\32\3\32\3\32")
        buf.write("\3\32\3\32\3\32\3\32\3\33\3\33\3\33\3\34\3\34\3\35\3\35")
        buf.write("\3\36\3\36\3\37\3\37\3 \3 \3!\3!\3\"\3\"\3#\3#\3$\3$\3")
        buf.write("$\3$\3$\3%\3%\3%\3%\3%\3%\3&\3&\3&\3&\3&\3\'\3\'\3\'\3")
        buf.write("\'\3\'\3\'\3\'\3(\3(\3(\3(\3)\3)\3)\3)\3)\3*\3*\3*\3*")
        buf.write("\3*\3*\3*\3+\3+\3+\3+\3+\3,\3,\7,\u0101\n,\f,\16,\u0104")
        buf.write("\13,\3,\3,\3-\5-\u0109\n-\3-\3-\7-\u010d\n-\f-\16-\u0110")
        buf.write("\13-\3.\3.\7.\u0114\n.\f.\16.\u0117\13.\3/\6/\u011a\n")
        buf.write("/\r/\16/\u011b\3\60\6\60\u011f\n\60\r\60\16\60\u0120\3")
        buf.write("\60\3\60\3\61\3\61\7\61\u0127\n\61\f\61\16\61\u012a\13")
        buf.write("\61\3\61\3\61\2\2\62\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21")
        buf.write("\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24")
        buf.write("\'\25)\26+\27-\30/\31\61\32\63\33\65\34\67\359\36;\37")
        buf.write("= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W-Y.[/]\60_\61a\62\3\2\n\3")
        buf.write("\2$$\3\2\63;\3\2\62;\5\2C\\aac|\7\2//\62;C\\aac|\6\2-")
        buf.write("-//\61\61>@\5\2\13\f\17\17\"\"\3\2\f\f\2\u0133\2\3\3\2")
        buf.write("\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2")
        buf.write("\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2")
        buf.write("\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35")
        buf.write("\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2")
        buf.write("\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2")
        buf.write("\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2")
        buf.write("\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2")
        buf.write("\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2")
        buf.write("\2\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3")
        buf.write("\2\2\2\2W\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_")
        buf.write("\3\2\2\2\2a\3\2\2\2\3c\3\2\2\2\5e\3\2\2\2\7h\3\2\2\2\t")
        buf.write("j\3\2\2\2\13l\3\2\2\2\rn\3\2\2\2\17p\3\2\2\2\21r\3\2\2")
        buf.write("\2\23u\3\2\2\2\25|\3\2\2\2\27\u0080\3\2\2\2\31\u0086\3")
        buf.write("\2\2\2\33\u0089\3\2\2\2\35\u0090\3\2\2\2\37\u0093\3\2")
        buf.write("\2\2!\u0098\3\2\2\2#\u009d\3\2\2\2%\u009f\3\2\2\2\'\u00a3")
        buf.write("\3\2\2\2)\u00aa\3\2\2\2+\u00ae\3\2\2\2-\u00b0\3\2\2\2")
        buf.write("/\u00b2\3\2\2\2\61\u00b5\3\2\2\2\63\u00b7\3\2\2\2\65\u00bf")
        buf.write("\3\2\2\2\67\u00c2\3\2\2\29\u00c4\3\2\2\2;\u00c6\3\2\2")
        buf.write("\2=\u00c8\3\2\2\2?\u00ca\3\2\2\2A\u00cc\3\2\2\2C\u00ce")
        buf.write("\3\2\2\2E\u00d0\3\2\2\2G\u00d2\3\2\2\2I\u00d7\3\2\2\2")
        buf.write("K\u00dd\3\2\2\2M\u00e2\3\2\2\2O\u00e9\3\2\2\2Q\u00ed\3")
        buf.write("\2\2\2S\u00f2\3\2\2\2U\u00f9\3\2\2\2W\u00fe\3\2\2\2Y\u0108")
        buf.write("\3\2\2\2[\u0111\3\2\2\2]\u0119\3\2\2\2_\u011e\3\2\2\2")
        buf.write("a\u0124\3\2\2\2cd\7`\2\2d\4\3\2\2\2ef\7,\2\2fg\7,\2\2")
        buf.write("g\6\3\2\2\2hi\7,\2\2i\b\3\2\2\2jk\7\61\2\2k\n\3\2\2\2")
        buf.write("lm\7-\2\2m\f\3\2\2\2no\7/\2\2o\16\3\2\2\2pq\7<\2\2q\20")
        buf.write("\3\2\2\2rs\7c\2\2st\7u\2\2t\22\3\2\2\2uv\7t\2\2vw\7g\2")
        buf.write("\2wx\7v\2\2xy\7w\2\2yz\7t\2\2z{\7p\2\2{\24\3\2\2\2|}\7")
        buf.write("n\2\2}~\7g\2\2~\177\7v\2\2\177\26\3\2\2\2\u0080\u0081")
        buf.write("\7d\2\2\u0081\u0082\7q\2\2\u0082\u0083\7w\2\2\u0083\u0084")
        buf.write("\7p\2\2\u0084\u0085\7f\2\2\u0085\30\3\2\2\2\u0086\u0087")
        buf.write("\7v\2\2\u0087\u0088\7q\2\2\u0088\32\3\2\2\2\u0089\u008a")
        buf.write("\7g\2\2\u008a\u008b\7z\2\2\u008b\u008c\7v\2\2\u008c\u008d")
        buf.write("\7g\2\2\u008d\u008e\7t\2\2\u008e\u008f\7p\2\2\u008f\34")
        buf.write("\3\2\2\2\u0090\u0091\7k\2\2\u0091\u0092\7h\2\2\u0092\36")
        buf.write("\3\2\2\2\u0093\u0094\7g\2\2\u0094\u0095\7n\2\2\u0095\u0096")
        buf.write("\7u\2\2\u0096\u0097\7g\2\2\u0097 \3\2\2\2\u0098\u0099")
        buf.write("\7v\2\2\u0099\u009a\7j\2\2\u009a\u009b\7g\2\2\u009b\u009c")
        buf.write("\7p\2\2\u009c\"\3\2\2\2\u009d\u009e\7?\2\2\u009e$\3\2")
        buf.write("\2\2\u009f\u00a0\7f\2\2\u00a0\u00a1\7g\2\2\u00a1\u00a2")
        buf.write("\7h\2\2\u00a2&\3\2\2\2\u00a3\u00a4\7k\2\2\u00a4\u00a5")
        buf.write("\7o\2\2\u00a5\u00a6\7r\2\2\u00a6\u00a7\7q\2\2\u00a7\u00a8")
        buf.write("\7t\2\2\u00a8\u00a9\7v\2\2\u00a9(\3\2\2\2\u00aa\u00ab")
        buf.write("\7h\2\2\u00ab\u00ac\7w\2\2\u00ac\u00ad\7p\2\2\u00ad*\3")
        buf.write("\2\2\2\u00ae\u00af\7.\2\2\u00af,\3\2\2\2\u00b0\u00b1\7")
        buf.write("#\2\2\u00b1.\3\2\2\2\u00b2\u00b3\7A\2\2\u00b3\u00b4\7")
        buf.write(",\2\2\u00b4\60\3\2\2\2\u00b5\u00b6\7A\2\2\u00b6\62\3\2")
        buf.write("\2\2\u00b7\u00b8\7e\2\2\u00b8\u00b9\7j\2\2\u00b9\u00ba")
        buf.write("\7c\2\2\u00ba\u00bb\7p\2\2\u00bb\u00bc\7p\2\2\u00bc\u00bd")
        buf.write("\7g\2\2\u00bd\u00be\7n\2\2\u00be\64\3\2\2\2\u00bf\u00c0")
        buf.write("\7k\2\2\u00c0\u00c1\7p\2\2\u00c1\66\3\2\2\2\u00c2\u00c3")
        buf.write("\7\60\2\2\u00c38\3\2\2\2\u00c4\u00c5\7*\2\2\u00c5:\3\2")
        buf.write("\2\2\u00c6\u00c7\7+\2\2\u00c7<\3\2\2\2\u00c8\u00c9\7}")
        buf.write("\2\2\u00c9>\3\2\2\2\u00ca\u00cb\7\177\2\2\u00cb@\3\2\2")
        buf.write("\2\u00cc\u00cd\7]\2\2\u00cdB\3\2\2\2\u00ce\u00cf\7_\2")
        buf.write("\2\u00cfD\3\2\2\2\u00d0\u00d1\7~\2\2\u00d1F\3\2\2\2\u00d2")
        buf.write("\u00d3\7v\2\2\u00d3\u00d4\7t\2\2\u00d4\u00d5\7w\2\2\u00d5")
        buf.write("\u00d6\7g\2\2\u00d6H\3\2\2\2\u00d7\u00d8\7h\2\2\u00d8")
        buf.write("\u00d9\7c\2\2\u00d9\u00da\7n\2\2\u00da\u00db\7u\2\2\u00db")
        buf.write("\u00dc\7g\2\2\u00dcJ\3\2\2\2\u00dd\u00de\7u\2\2\u00de")
        buf.write("\u00df\7m\2\2\u00df\u00e0\7k\2\2\u00e0\u00e1\7r\2\2\u00e1")
        buf.write("L\3\2\2\2\u00e2\u00e3\7t\2\2\u00e3\u00e4\7g\2\2\u00e4")
        buf.write("\u00e5\7e\2\2\u00e5\u00e6\7q\2\2\u00e6\u00e7\7t\2\2\u00e7")
        buf.write("\u00e8\7f\2\2\u00e8N\3\2\2\2\u00e9\u00ea\7k\2\2\u00ea")
        buf.write("\u00eb\7p\2\2\u00eb\u00ec\7v\2\2\u00ecP\3\2\2\2\u00ed")
        buf.write("\u00ee\7d\2\2\u00ee\u00ef\7q\2\2\u00ef\u00f0\7q\2\2\u00f0")
        buf.write("\u00f1\7n\2\2\u00f1R\3\2\2\2\u00f2\u00f3\7u\2\2\u00f3")
        buf.write("\u00f4\7v\2\2\u00f4\u00f5\7t\2\2\u00f5\u00f6\7k\2\2\u00f6")
        buf.write("\u00f7\7p\2\2\u00f7\u00f8\7i\2\2\u00f8T\3\2\2\2\u00f9")
        buf.write("\u00fa\7x\2\2\u00fa\u00fb\7q\2\2\u00fb\u00fc\7k\2\2\u00fc")
        buf.write("\u00fd\7f\2\2\u00fdV\3\2\2\2\u00fe\u0102\7$\2\2\u00ff")
        buf.write("\u0101\n\2\2\2\u0100\u00ff\3\2\2\2\u0101\u0104\3\2\2\2")
        buf.write("\u0102\u0100\3\2\2\2\u0102\u0103\3\2\2\2\u0103\u0105\3")
        buf.write("\2\2\2\u0104\u0102\3\2\2\2\u0105\u0106\7$\2\2\u0106X\3")
        buf.write("\2\2\2\u0107\u0109\7/\2\2\u0108\u0107\3\2\2\2\u0108\u0109")
        buf.write("\3\2\2\2\u0109\u010a\3\2\2\2\u010a\u010e\t\3\2\2\u010b")
        buf.write("\u010d\t\4\2\2\u010c\u010b\3\2\2\2\u010d\u0110\3\2\2\2")
        buf.write("\u010e\u010c\3\2\2\2\u010e\u010f\3\2\2\2\u010fZ\3\2\2")
        buf.write("\2\u0110\u010e\3\2\2\2\u0111\u0115\t\5\2\2\u0112\u0114")
        buf.write("\t\6\2\2\u0113\u0112\3\2\2\2\u0114\u0117\3\2\2\2\u0115")
        buf.write("\u0113\3\2\2\2\u0115\u0116\3\2\2\2\u0116\\\3\2\2\2\u0117")
        buf.write("\u0115\3\2\2\2\u0118\u011a\t\7\2\2\u0119\u0118\3\2\2\2")
        buf.write("\u011a\u011b\3\2\2\2\u011b\u0119\3\2\2\2\u011b\u011c\3")
        buf.write("\2\2\2\u011c^\3\2\2\2\u011d\u011f\t\b\2\2\u011e\u011d")
        buf.write("\3\2\2\2\u011f\u0120\3\2\2\2\u0120\u011e\3\2\2\2\u0120")
        buf.write("\u0121\3\2\2\2\u0121\u0122\3\2\2\2\u0122\u0123\b\60\2")
        buf.write("\2\u0123`\3\2\2\2\u0124\u0128\7%\2\2\u0125\u0127\n\t\2")
        buf.write("\2\u0126\u0125\3\2\2\2\u0127\u012a\3\2\2\2\u0128\u0126")
        buf.write("\3\2\2\2\u0128\u0129\3\2\2\2\u0129\u012b\3\2\2\2\u012a")
        buf.write("\u0128\3\2\2\2\u012b\u012c\b\61\2\2\u012cb\3\2\2\2\n\2")
        buf.write("\u0102\u0108\u010e\u0115\u011b\u0120\u0128\3\b\2\2")
        return buf.getvalue()


class pisteLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    CARET = 1
    POW = 2
    MULT = 3
    DIV = 4
    ADD = 5
    SUB = 6
    COLON = 7
    AS = 8
    RETURN = 9
    LET = 10
    BOUND = 11
    TO = 12
    EXTERN = 13
    IF = 14
    ELSE = 15
    THEN = 16
    EQ = 17
    DEF = 18
    IMPORT = 19
    FUN = 20
    COMMA = 21
    SEND = 22
    RECEIVE_REPLICATED = 23
    RECEIVE = 24
    CHANNEL = 25
    IN = 26
    DOT = 27
    PAREN_LEFT = 28
    PAREN_RIGHT = 29
    BRACE_LEFT = 30
    BRACE_RIGHT = 31
    SQUARE_LEFT = 32
    SQUARE_RIGHT = 33
    PARALLEL = 34
    TRUE = 35
    FALSE = 36
    INACTION = 37
    RECORD = 38
    INT_T = 39
    BOOL_T = 40
    STRING_T = 41
    VOID_T = 42
    STRING = 43
    INTEGER = 44
    IDENTIFIER = 45
    SYMBOL_IDENTIFIER = 46
    WS = 47
    COMMENT = 48

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'^'", "'**'", "'*'", "'/'", "'+'", "'-'", "':'", "'as'", "'return'", 
            "'let'", "'bound'", "'to'", "'extern'", "'if'", "'else'", "'then'", 
            "'='", "'def'", "'import'", "'fun'", "','", "'!'", "'?*'", "'?'", 
            "'channel'", "'in'", "'.'", "'('", "')'", "'{'", "'}'", "'['", 
            "']'", "'|'", "'true'", "'false'", "'skip'", "'record'", "'int'", 
            "'bool'", "'string'", "'void'" ]

    symbolicNames = [ "<INVALID>",
            "CARET", "POW", "MULT", "DIV", "ADD", "SUB", "COLON", "AS", 
            "RETURN", "LET", "BOUND", "TO", "EXTERN", "IF", "ELSE", "THEN", 
            "EQ", "DEF", "IMPORT", "FUN", "COMMA", "SEND", "RECEIVE_REPLICATED", 
            "RECEIVE", "CHANNEL", "IN", "DOT", "PAREN_LEFT", "PAREN_RIGHT", 
            "BRACE_LEFT", "BRACE_RIGHT", "SQUARE_LEFT", "SQUARE_RIGHT", 
            "PARALLEL", "TRUE", "FALSE", "INACTION", "RECORD", "INT_T", 
            "BOOL_T", "STRING_T", "VOID_T", "STRING", "INTEGER", "IDENTIFIER", 
            "SYMBOL_IDENTIFIER", "WS", "COMMENT" ]

    ruleNames = [ "CARET", "POW", "MULT", "DIV", "ADD", "SUB", "COLON", 
                  "AS", "RETURN", "LET", "BOUND", "TO", "EXTERN", "IF", 
                  "ELSE", "THEN", "EQ", "DEF", "IMPORT", "FUN", "COMMA", 
                  "SEND", "RECEIVE_REPLICATED", "RECEIVE", "CHANNEL", "IN", 
                  "DOT", "PAREN_LEFT", "PAREN_RIGHT", "BRACE_LEFT", "BRACE_RIGHT", 
                  "SQUARE_LEFT", "SQUARE_RIGHT", "PARALLEL", "TRUE", "FALSE", 
                  "INACTION", "RECORD", "INT_T", "BOOL_T", "STRING_T", "VOID_T", 
                  "STRING", "INTEGER", "IDENTIFIER", "SYMBOL_IDENTIFIER", 
                  "WS", "COMMENT" ]

    grammarFileName = "piste.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


