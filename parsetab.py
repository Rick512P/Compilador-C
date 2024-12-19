
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "ASPAS ATR BOOLEAN BOOLEAN CASE CASE CHAR COMENTARIO DEFINE DELIMITADOR DO DO ELSE ELSE FOR FOR ID IF IF LBRACKET LCHAVE LIBIMPORT LPAREN MATRIX NUMERO OPA OPL PRINT PRINT RBRACKET RCHAVE RPAREN STRING SWITCH SWITCH TIPO TIPO TIPO TIPO TIPO TIPO VECTOR WHILE WHILEprograma : lista_declaracoescomentario : COMENTARIOlista_declaracoes : lista_declaracoes declaracao\n| declaracaodeclaracao : declaracao_funcao\n| declaracao_variaveis\n| declaracao_preprocessador\n| atribuicaodeclaracao_variaveis : comentario\n| tipo lista_variaveis DELIMITADOR\n| tipo ID VECTOR DELIMITADOR\n| tipo ID MATRIX DELIMITADOR\n| tipo ID VECTOR ATR expressao DELIMITADOR\n| tipo ID MATRIX ATR expressao DELIMITADOR\n| tipo ID CHAR ATR expressao DELIMITADORdeclaracao_funcao : tipo ID LPAREN parametros RPAREN bloco\n| tipo ID LPAREN expressao RPAREN blocodeclaracao_preprocessador : LIBIMPORTtipo : TIPOlista_variaveis : lista_variaveis ',' ID\n| IDparametros : lista_parametros\n| vaziolista_parametros : lista_parametros DELIMITADOR tipo ID\n| lista_parametros DELIMITADOR tipo ID VECTOR\n| lista_parametros DELIMITADOR tipo ID MATRIX\n| tipo ID\n| tipo ID VECTOR\n| tipo ID MATRIXbloco : LCHAVE lista_comandos RCHAVElista_comandos : lista_comandos comando\n| comandocomando :  atribuicao\n| comando_condicional\n| comando_loop\n| bloco\n| declaracao_variaveis\n| printaratribuicao : ID ATR expressao DELIMITADOR\n| ID VECTOR ATR expressao DELIMITADOR\n| ID MATRIX ATR expressao DELIMITADOR\n| ID OPA OPA DELIMITADOR\n| ID CHAR ATR ASPAS ID ASPAScomando_condicional : IF LPAREN expressao RPAREN blococomando_loop : DO bloco WHILE LPAREN expressao RPAREN DELIMITADOR\n| WHILE LPAREN expressao RPAREN bloco\n| FOR LPAREN TIPO atribuicao expressao DELIMITADOR atribuicao RPAREN bloco\n| FOR LPAREN atribuicao expressao DELIMITADOR atribuicao RPAREN blocoprintar : PRINT LPAREN expressao RPAREN DELIMITADORexpressao : expressao OPL expressao\n| expressao OPA expressao\n| STRING\n| NUMERO\n| ID\n| ID LPAREN expressao RPAREN\n| ID LBRACKET expressao RBRACKET\n| LBRACKET expressao RBRACKET\n| ID LBRACKET expressao RBRACKET LBRACKET expressao RBRACKET\n| LBRACKET expressao RBRACKET LBRACKET expressao RBRACKET\n| DELIMITADOR\n| bloco\n| LPAREN expressao RPARENvazio : "
    
_lr_action_items = {'LIBIMPORT':([0,2,3,4,5,6,7,10,11,13,14,26,46,48,54,75,90,98,99,103,104,106,107,108,118,],[11,11,-4,-5,-6,-7,-8,-9,-18,-2,-3,-10,-11,-12,-39,-42,-30,-40,-41,-16,-17,-13,-14,-15,-43,]),'ID':([0,2,3,4,5,6,7,8,10,11,12,13,14,17,22,26,27,33,34,36,37,38,41,46,47,48,49,50,52,53,54,55,56,59,60,61,62,63,64,65,66,71,75,76,90,91,92,94,95,97,98,99,103,104,105,106,107,108,111,115,116,118,120,123,125,132,134,136,137,140,142,146,147,],[9,9,-4,-5,-6,-7,-8,15,-9,-18,-19,-2,-3,28,28,-10,51,28,28,9,28,28,77,-11,28,-12,28,28,28,28,-39,28,28,9,-32,-33,-34,-35,-36,-37,-38,96,-42,100,-30,-31,28,28,9,28,-40,-41,-16,-17,119,-13,-14,-15,28,9,28,-43,28,28,28,-44,-46,9,-49,9,-45,-48,-47,]),'TIPO':([0,2,3,4,5,6,7,10,11,13,14,22,26,36,46,48,54,59,60,61,62,63,64,65,66,75,80,90,91,95,98,99,103,104,106,107,108,118,132,134,137,142,146,147,],[12,12,-4,-5,-6,-7,-8,-9,-18,-2,-3,12,-10,12,-11,-12,-39,12,-32,-33,-34,-35,-36,-37,-38,-42,12,-30,-31,115,-40,-41,-16,-17,-13,-14,-15,-43,-44,-46,-49,-45,-48,-47,]),'COMENTARIO':([0,2,3,4,5,6,7,10,11,13,14,26,36,46,48,54,59,60,61,62,63,64,65,66,75,90,91,98,99,103,104,106,107,108,118,132,134,137,142,146,147,],[13,13,-4,-5,-6,-7,-8,-9,-18,-2,-3,-10,13,-11,-12,-39,13,-32,-33,-34,-35,-36,-37,-38,-42,-30,-31,-40,-41,-16,-17,-13,-14,-15,-43,-44,-46,-49,-45,-48,-47,]),'$end':([1,2,3,4,5,6,7,10,11,13,14,26,46,48,54,75,90,98,99,103,104,106,107,108,118,],[0,-1,-4,-5,-6,-7,-8,-9,-18,-2,-3,-10,-11,-12,-39,-42,-30,-40,-41,-16,-17,-13,-14,-15,-43,]),'ATR':([9,18,19,21,23,24,25,],[17,37,38,40,47,49,50,]),'VECTOR':([9,15,77,96,119,],[18,23,101,23,128,]),'MATRIX':([9,15,77,96,119,],[19,24,102,24,129,]),'OPA':([9,20,28,29,30,31,32,35,43,57,58,73,74,81,82,83,84,85,86,87,88,89,90,109,110,112,114,117,121,126,130,131,133,135,138,],[20,39,-54,56,-60,-52,-53,-61,56,56,56,56,56,56,56,56,56,56,56,56,-62,-57,-30,-55,-56,56,56,56,56,56,56,-59,56,56,-58,]),'CHAR':([9,15,96,],[21,25,25,]),'RCHAVE':([10,13,26,46,48,54,59,60,61,62,63,64,65,66,75,90,91,98,99,106,107,108,118,132,134,137,142,146,147,],[-9,-2,-10,-11,-12,-39,90,-32,-33,-34,-35,-36,-37,-38,-42,-30,-31,-40,-41,-13,-14,-15,-43,-44,-46,-49,-45,-48,-47,]),'IF':([10,13,26,36,46,48,54,59,60,61,62,63,64,65,66,75,90,91,98,99,106,107,108,118,132,134,137,142,146,147,],[-9,-2,-10,67,-11,-12,-39,67,-32,-33,-34,-35,-36,-37,-38,-42,-30,-31,-40,-41,-13,-14,-15,-43,-44,-46,-49,-45,-48,-47,]),'DO':([10,13,26,36,46,48,54,59,60,61,62,63,64,65,66,75,90,91,98,99,106,107,108,118,132,134,137,142,146,147,],[-9,-2,-10,68,-11,-12,-39,68,-32,-33,-34,-35,-36,-37,-38,-42,-30,-31,-40,-41,-13,-14,-15,-43,-44,-46,-49,-45,-48,-47,]),'WHILE':([10,13,26,36,46,48,54,59,60,61,62,63,64,65,66,75,90,91,93,98,99,106,107,108,118,132,134,137,142,146,147,],[-9,-2,-10,69,-11,-12,-39,69,-32,-33,-34,-35,-36,-37,-38,-42,-30,-31,113,-40,-41,-13,-14,-15,-43,-44,-46,-49,-45,-48,-47,]),'FOR':([10,13,26,36,46,48,54,59,60,61,62,63,64,65,66,75,90,91,98,99,106,107,108,118,132,134,137,142,146,147,],[-9,-2,-10,70,-11,-12,-39,70,-32,-33,-34,-35,-36,-37,-38,-42,-30,-31,-40,-41,-13,-14,-15,-43,-44,-46,-49,-45,-48,-47,]),'LCHAVE':([10,13,17,22,26,33,34,36,37,38,46,47,48,49,50,52,53,54,55,56,59,60,61,62,63,64,65,66,68,75,78,79,90,91,92,94,97,98,99,106,107,108,111,116,118,120,122,123,124,125,132,134,137,142,144,145,146,147,],[-9,-2,36,36,-10,36,36,36,36,36,-11,36,-12,36,36,36,36,-39,36,36,36,-32,-33,-34,-35,-36,-37,-38,36,-42,36,36,-30,-31,36,36,36,-40,-41,-13,-14,-15,36,36,-43,36,36,36,36,36,-44,-46,-49,-45,36,36,-48,-47,]),'PRINT':([10,13,26,36,46,48,54,59,60,61,62,63,64,65,66,75,90,91,98,99,106,107,108,118,132,134,137,142,146,147,],[-9,-2,-10,72,-11,-12,-39,72,-32,-33,-34,-35,-36,-37,-38,-42,-30,-31,-40,-41,-13,-14,-15,-43,-44,-46,-49,-45,-48,-47,]),'LPAREN':([15,17,22,28,33,34,37,38,47,49,50,52,53,54,55,56,67,69,70,72,75,92,94,97,98,99,111,113,116,118,120,123,125,],[22,33,33,52,33,33,33,33,33,33,33,33,33,-39,33,33,92,94,95,97,-42,33,33,33,-40,-41,33,123,33,-43,33,33,33,]),'DELIMITADOR':([15,16,17,22,23,24,28,29,30,31,32,33,34,35,37,38,39,44,47,49,50,51,52,53,54,55,56,73,74,75,77,81,82,83,86,87,88,89,90,92,94,96,97,98,99,101,102,109,110,111,116,118,119,120,123,125,126,127,128,129,131,135,138,139,],[-21,26,30,30,46,48,-54,54,-60,-52,-53,30,30,-61,30,30,75,80,30,30,30,-20,30,30,-39,30,30,98,99,-42,-27,106,107,108,-50,-51,-62,-57,-30,30,30,-21,30,-40,-41,-28,-29,-55,-56,30,30,-43,-24,30,30,30,136,137,-25,-26,-59,140,-58,142,]),',':([15,16,51,96,],[-21,27,-20,-21,]),'STRING':([17,22,33,34,37,38,47,49,50,52,53,54,55,56,75,92,94,97,98,99,111,116,118,120,123,125,],[31,31,31,31,31,31,31,31,31,31,31,-39,31,31,-42,31,31,31,-40,-41,31,31,-43,31,31,31,]),'NUMERO':([17,22,33,34,37,38,47,49,50,52,53,54,55,56,75,92,94,97,98,99,111,116,118,120,123,125,],[32,32,32,32,32,32,32,32,32,32,32,-39,32,32,-42,32,32,32,-40,-41,32,32,-43,32,32,32,]),'LBRACKET':([17,22,28,33,34,37,38,47,49,50,52,53,54,55,56,75,89,92,94,97,98,99,110,111,116,118,120,123,125,],[34,34,53,34,34,34,34,34,34,34,34,34,-39,34,34,-42,111,34,34,34,-40,-41,120,34,34,-43,34,34,34,]),'RPAREN':([22,28,30,31,32,35,42,43,44,45,54,57,75,77,84,86,87,88,89,90,98,99,101,102,109,110,112,114,117,118,119,128,129,131,133,138,141,143,],[-63,-54,-60,-52,-53,-61,78,79,-22,-23,-39,88,-42,-27,109,-50,-51,-62,-57,-30,-40,-41,-28,-29,-55,-56,122,124,127,-43,-24,-25,-26,-59,139,-58,144,145,]),'OPL':([28,29,30,31,32,35,43,57,58,73,74,81,82,83,84,85,86,87,88,89,90,109,110,112,114,117,121,126,130,131,133,135,138,],[-54,55,-60,-52,-53,-61,55,55,55,55,55,55,55,55,55,55,55,55,-62,-57,-30,-55,-56,55,55,55,55,55,55,-59,55,55,-58,]),'RBRACKET':([28,30,31,32,35,58,85,86,87,88,89,90,109,110,121,130,131,138,],[-54,-60,-52,-53,-61,89,110,-50,-51,-62,-57,-30,-55,-56,131,138,-59,-58,]),'ASPAS':([40,100,],[76,118,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'programa':([0,],[1,]),'lista_declaracoes':([0,],[2,]),'declaracao':([0,2,],[3,14,]),'declaracao_funcao':([0,2,],[4,4,]),'declaracao_variaveis':([0,2,36,59,],[5,5,65,65,]),'declaracao_preprocessador':([0,2,],[6,6,]),'atribuicao':([0,2,36,59,95,115,136,140,],[7,7,61,61,116,125,141,143,]),'tipo':([0,2,22,36,59,80,],[8,8,41,71,71,105,]),'comentario':([0,2,36,59,],[10,10,10,10,]),'lista_variaveis':([8,71,],[16,16,]),'expressao':([17,22,33,34,37,38,47,49,50,52,53,55,56,92,94,97,111,116,120,123,125,],[29,43,57,58,73,74,81,82,83,84,85,86,87,112,114,117,121,126,130,133,135,]),'bloco':([17,22,33,34,36,37,38,47,49,50,52,53,55,56,59,68,78,79,92,94,97,111,116,120,122,123,124,125,144,145,],[35,35,35,35,64,35,35,35,35,35,35,35,35,35,64,93,103,104,35,35,35,35,35,35,132,35,134,35,146,147,]),'parametros':([22,],[42,]),'lista_parametros':([22,],[44,]),'vazio':([22,],[45,]),'lista_comandos':([36,],[59,]),'comando':([36,59,],[60,91,]),'comando_condicional':([36,59,],[62,62,]),'comando_loop':([36,59,],[63,63,]),'printar':([36,59,],[66,66,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programa","S'",1,None,None,None),
  ('programa -> lista_declaracoes','programa',1,'p_programa','parser_testes.py',86),
  ('comentario -> COMENTARIO','comentario',1,'p_comentario','parser_testes.py',94),
  ('lista_declaracoes -> lista_declaracoes declaracao','lista_declaracoes',2,'p_lista_declaracoes','parser_testes.py',98),
  ('lista_declaracoes -> declaracao','lista_declaracoes',1,'p_lista_declaracoes','parser_testes.py',99),
  ('declaracao -> declaracao_funcao','declaracao',1,'p_declaracao','parser_testes.py',104),
  ('declaracao -> declaracao_variaveis','declaracao',1,'p_declaracao','parser_testes.py',105),
  ('declaracao -> declaracao_preprocessador','declaracao',1,'p_declaracao','parser_testes.py',106),
  ('declaracao -> atribuicao','declaracao',1,'p_declaracao','parser_testes.py',107),
  ('declaracao_variaveis -> comentario','declaracao_variaveis',1,'p_declaracao_variaveis','parser_testes.py',112),
  ('declaracao_variaveis -> tipo lista_variaveis DELIMITADOR','declaracao_variaveis',3,'p_declaracao_variaveis','parser_testes.py',113),
  ('declaracao_variaveis -> tipo ID VECTOR DELIMITADOR','declaracao_variaveis',4,'p_declaracao_variaveis','parser_testes.py',114),
  ('declaracao_variaveis -> tipo ID MATRIX DELIMITADOR','declaracao_variaveis',4,'p_declaracao_variaveis','parser_testes.py',115),
  ('declaracao_variaveis -> tipo ID VECTOR ATR expressao DELIMITADOR','declaracao_variaveis',6,'p_declaracao_variaveis','parser_testes.py',116),
  ('declaracao_variaveis -> tipo ID MATRIX ATR expressao DELIMITADOR','declaracao_variaveis',6,'p_declaracao_variaveis','parser_testes.py',117),
  ('declaracao_variaveis -> tipo ID CHAR ATR expressao DELIMITADOR','declaracao_variaveis',6,'p_declaracao_variaveis','parser_testes.py',118),
  ('declaracao_funcao -> tipo ID LPAREN parametros RPAREN bloco','declaracao_funcao',6,'p_declaracao_funcao','parser_testes.py',128),
  ('declaracao_funcao -> tipo ID LPAREN expressao RPAREN bloco','declaracao_funcao',6,'p_declaracao_funcao','parser_testes.py',129),
  ('declaracao_preprocessador -> LIBIMPORT','declaracao_preprocessador',1,'p_declaracao_preprocessador','parser_testes.py',135),
  ('tipo -> TIPO','tipo',1,'p_tipo','parser_testes.py',144),
  ('lista_variaveis -> lista_variaveis , ID','lista_variaveis',3,'p_lista_variaveis','parser_testes.py',149),
  ('lista_variaveis -> ID','lista_variaveis',1,'p_lista_variaveis','parser_testes.py',150),
  ('parametros -> lista_parametros','parametros',1,'p_parametros','parser_testes.py',155),
  ('parametros -> vazio','parametros',1,'p_parametros','parser_testes.py',156),
  ('lista_parametros -> lista_parametros DELIMITADOR tipo ID','lista_parametros',4,'p_lista_parametros','parser_testes.py',161),
  ('lista_parametros -> lista_parametros DELIMITADOR tipo ID VECTOR','lista_parametros',5,'p_lista_parametros','parser_testes.py',162),
  ('lista_parametros -> lista_parametros DELIMITADOR tipo ID MATRIX','lista_parametros',5,'p_lista_parametros','parser_testes.py',163),
  ('lista_parametros -> tipo ID','lista_parametros',2,'p_lista_parametros','parser_testes.py',164),
  ('lista_parametros -> tipo ID VECTOR','lista_parametros',3,'p_lista_parametros','parser_testes.py',165),
  ('lista_parametros -> tipo ID MATRIX','lista_parametros',3,'p_lista_parametros','parser_testes.py',166),
  ('bloco -> LCHAVE lista_comandos RCHAVE','bloco',3,'p_bloco','parser_testes.py',171),
  ('lista_comandos -> lista_comandos comando','lista_comandos',2,'p_lista_comandos','parser_testes.py',176),
  ('lista_comandos -> comando','lista_comandos',1,'p_lista_comandos','parser_testes.py',177),
  ('comando -> atribuicao','comando',1,'p_comando','parser_testes.py',182),
  ('comando -> comando_condicional','comando',1,'p_comando','parser_testes.py',183),
  ('comando -> comando_loop','comando',1,'p_comando','parser_testes.py',184),
  ('comando -> bloco','comando',1,'p_comando','parser_testes.py',185),
  ('comando -> declaracao_variaveis','comando',1,'p_comando','parser_testes.py',186),
  ('comando -> printar','comando',1,'p_comando','parser_testes.py',187),
  ('atribuicao -> ID ATR expressao DELIMITADOR','atribuicao',4,'p_atribuicao','parser_testes.py',192),
  ('atribuicao -> ID VECTOR ATR expressao DELIMITADOR','atribuicao',5,'p_atribuicao','parser_testes.py',193),
  ('atribuicao -> ID MATRIX ATR expressao DELIMITADOR','atribuicao',5,'p_atribuicao','parser_testes.py',194),
  ('atribuicao -> ID OPA OPA DELIMITADOR','atribuicao',4,'p_atribuicao','parser_testes.py',195),
  ('atribuicao -> ID CHAR ATR ASPAS ID ASPAS','atribuicao',6,'p_atribuicao','parser_testes.py',196),
  ('comando_condicional -> IF LPAREN expressao RPAREN bloco','comando_condicional',5,'p_comando_condicional','parser_testes.py',207),
  ('comando_loop -> DO bloco WHILE LPAREN expressao RPAREN DELIMITADOR','comando_loop',7,'p_comando_loop','parser_testes.py',214),
  ('comando_loop -> WHILE LPAREN expressao RPAREN bloco','comando_loop',5,'p_comando_loop','parser_testes.py',215),
  ('comando_loop -> FOR LPAREN TIPO atribuicao expressao DELIMITADOR atribuicao RPAREN bloco','comando_loop',9,'p_comando_loop','parser_testes.py',216),
  ('comando_loop -> FOR LPAREN atribuicao expressao DELIMITADOR atribuicao RPAREN bloco','comando_loop',8,'p_comando_loop','parser_testes.py',217),
  ('printar -> PRINT LPAREN expressao RPAREN DELIMITADOR','printar',5,'p_printar','parser_testes.py',234),
  ('expressao -> expressao OPL expressao','expressao',3,'p_expressao','parser_testes.py',240),
  ('expressao -> expressao OPA expressao','expressao',3,'p_expressao','parser_testes.py',241),
  ('expressao -> STRING','expressao',1,'p_expressao','parser_testes.py',242),
  ('expressao -> NUMERO','expressao',1,'p_expressao','parser_testes.py',243),
  ('expressao -> ID','expressao',1,'p_expressao','parser_testes.py',244),
  ('expressao -> ID LPAREN expressao RPAREN','expressao',4,'p_expressao','parser_testes.py',245),
  ('expressao -> ID LBRACKET expressao RBRACKET','expressao',4,'p_expressao','parser_testes.py',246),
  ('expressao -> LBRACKET expressao RBRACKET','expressao',3,'p_expressao','parser_testes.py',247),
  ('expressao -> ID LBRACKET expressao RBRACKET LBRACKET expressao RBRACKET','expressao',7,'p_expressao','parser_testes.py',248),
  ('expressao -> LBRACKET expressao RBRACKET LBRACKET expressao RBRACKET','expressao',6,'p_expressao','parser_testes.py',249),
  ('expressao -> DELIMITADOR','expressao',1,'p_expressao','parser_testes.py',250),
  ('expressao -> bloco','expressao',1,'p_expressao','parser_testes.py',251),
  ('expressao -> LPAREN expressao RPAREN','expressao',3,'p_expressao','parser_testes.py',252),
  ('vazio -> <empty>','vazio',0,'p_vazio','parser_testes.py',265),
]
