grammar piste;

program: declaration* process;

declaration: record_declaration
           | extern_declaration;

extern_declaration:
    EXTERN IDENTIFIER PAREN_LEFT type_name (COMMA type_name)* PAREN_RIGHT COLON type_name BOUND TO IDENTIFIER;


record_declaration: RECORD IDENTIFIER BRACE_LEFT IDENTIFIER COLON type_name (COMMA IDENTIFIER COLON type_name)* BRACE_RIGHT;

type_name: INT_T #type_int
         | BOOL_T #type_bool
         | VOID_T #type_void
         | STRING_T #type_string
         | CARET message_type #type_channel
         | IDENTIFIER #type_identifier;

message_type: SQUARE_LEFT type_name (COMMA type_name)* SQUARE_RIGHT;

process: receiver=expression SEND SQUARE_LEFT expression (COMMA expression)* SQUARE_RIGHT #output
       | expression RECEIVE SQUARE_LEFT identifier_with_type (COMMA identifier_with_type)* SQUARE_RIGHT EQ process #input
       | CHANNEL IDENTIFIER COLON type_name IN process #restriction
       | expression RECEIVE_REPLICATED SQUARE_LEFT  identifier_with_type (COMMA identifier_with_type)* SQUARE_RIGHT  EQ process #replicated_input
       | PAREN_LEFT process PAREN_RIGHT #paren
       | DEF IDENTIFIER SQUARE_LEFT IDENTIFIER (COMMA IDENTIFIER)* SQUARE_RIGHT EQ body=process continuation=process #process_def
       | INACTION #inaction
       | IF expression THEN true_branch=process (ELSE false_branch=process)? #conditional
       | EXTERN IDENTIFIER PAREN_LEFT type_name (COMMA type_name)* PAREN_RIGHT COLON type_name BOUND TO IDENTIFIER IN continuation=process #extern_def
       | LET value_binding (COMMA value_binding)* IN process #let_binding
       | FUN IDENTIFIER PAREN_LEFT IDENTIFIER COLON type_name (COMMA IDENTIFIER COLON type_name)* PAREN_RIGHT COLON type_name EQ body=process continuation=process #function_def
       | RETURN expression #return
       | <assoc=right> left=process PARALLEL right=process #parallel;

value_binding: (identifier_with_type EQ ) ? expression PAREN_LEFT expression (COMMA expression)*  PAREN_RIGHT #call_binding
             | identifier_with_type EQ expression  #simple_value_binding;

identifier_with_type : IDENTIFIER (COLON type_name)?;

expression: PAREN_LEFT expression PAREN_RIGHT #paren_expr
          | value #literal
          | expression POW expression #operator_pow_expr
          | expression (MULT|DIV) expression #operator_md_expr
          | expression (ADD|SUB) expression #operator_as_expr
        //| expression COLON IDENTIFIER DOT IDENTIFIER #path_val
          ;

value: TRUE #true_val
     | FALSE #false_val
     | STRING #string_val
     | IDENTIFIER #identifier_val
     | record #record_val
     | INTEGER #int_val;

record: BRACE_LEFT IDENTIFIER EQ expression (COMMA IDENTIFIER EQ expression)* BRACE_RIGHT AS IDENTIFIER;

CARET: '^';
POW: '**';
MULT: '*';
DIV: '/';
ADD: '+';
SUB: '-';
COLON: ':';
AS : 'as';
RETURN: 'return';
LET: 'let';
BOUND: 'bound';
TO: 'to';
EXTERN: 'extern';
IF: 'if';
ELSE: 'else';
THEN: 'then';
EQ: '=';
DEF: 'def';
FUN: 'fun';
COMMA: ',';
SEND: '!';
RECEIVE_REPLICATED: '?*';
RECEIVE: '?';
CHANNEL: 'channel';
IN: 'in';
DOT: '.';
PAREN_LEFT: '(';
PAREN_RIGHT: ')';
BRACE_LEFT: '{';
BRACE_RIGHT: '}';
SQUARE_LEFT: '[';
SQUARE_RIGHT: ']';
PARALLEL: '|';
TRUE: 'true';
FALSE: 'false';
INACTION: 'skip';
RECORD: 'record';

INT_T : 'int';
BOOL_T: 'bool';
STRING_T : 'string';
VOID_T : 'void';

STRING: '"' (~'"')* '"';
INTEGER: '-'?[1-9][0-9]*;
IDENTIFIER: [a-zA-Z_][a-zA-Z_\-0-9]*;
SYMBOL_IDENTIFIER: [+/\-><=]+;


WS : [ \t\n\r]+ -> skip ;
COMMENT : '#'(~'\n')* -> skip;