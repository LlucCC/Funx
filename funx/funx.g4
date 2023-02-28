grammar funx;
root : func* expr? EOF ;

stat : expr #Expres
      |ID '<-' expr #Assig 
      |'if' boolexpr bloc ('else' bloc )? #Conditional
      |'while' boolexpr bloc #While ;

boolexpr: '(' boolexpr ')' #BoolPar |
          expr ('=='|'!=' |'<' |'>' |'<=' |'>=') expr #Comparison | 
          boolexpr ('and'|'or'|'xor'|'->'| '<->') boolexpr #Comparison | 
          'not' boolexpr #Negation ; 

bloc: '{' stat+ '}' ;

func: FUNCID (ID|FUNCID)* bloc ;

expr : 
    '(' expr ')' #Par
    |<assoc=right> expr '^' expr #Bin
    | expr ('*'|'/'|'%') expr #Bin
    | expr ('+'|'-') expr #Bin
    | '-' expr #Negative 
    | NUM #Valor
    | ID #Variable
    | FUNCID (FUNCID|expr)* #Call
    ;

ID : [a-z][a-zA-Z0-9]* ;
NUM : [0-9]+ ;
FUNCID : [A-Z][a-zA-Z0-9]* ; 
COMENT : '#'~[\n]*[\n]? -> skip ;
WS : [ \n]+ -> skip ;