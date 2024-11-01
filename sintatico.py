# Importa a biblioteca Ply para criação do analisador sintático
import ply.yacc as yacc
from lexico import tokens  # Importa os tokens do arquivo lexico.py
import sys

# Programa principal que pode conter múltiplas declarações ou expressões
def p_programa(p):
    'programa : lista_declaracoes'
    p[0] = ("programa", p[1])

# Lista de declarações
def p_lista_declaracoes(p):
    '''lista_declaracoes : lista_declaracoes declaracao
                         | declaracao'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# Declaração que pode ser uma expressão ou uma estrutura de controle
def p_declaracao(p):
    '''declaracao : declaracao_expressao
                  | declaracao_controle'''
    p[0] = p[1]

# Declaração de expressão
def p_declaracao_expressao(p):
    'declaracao_expressao : expressao DELIMITADOR'
    p[0] = ("expressao", p[1])

# Expressões aritméticas com operadores
def p_expressao(p):
    '''expressao : expressao OPA expressao
                 | expressao OPL expressao
                 | NUMERO
                 | ID'''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]

# Estruturas de controle, como if-else
def p_declaracao_controle(p):
    '''declaracao_controle : if_declaracao
                           | while_declaracao'''
    p[0] = p[1]

# Estrutura if-else
def p_if_declaracao(p):
    '''if_declaracao : IF expressao bloco ELSE bloco
                     | IF expressao bloco'''
    if len(p) == 6:
        p[0] = ("if-else", p[2], p[3], p[5])
    else:
        p[0] = ("if", p[2], p[3])

# Estrutura de bloco
def p_bloco(p):
    'bloco : DELIMITADOR declaracao DELIMITADOR'
    p[0] = p[2]

# Estrutura while
def p_while_declaracao(p):
    'while_declaracao : WHILE expressao bloco'
    p[0] = ("while", p[2], p[3])

# Define erro sintático
def p_error(p):
    if p:
        print(f"Erro sintático: {p.value} na linha {p.lineno}")
    else:
        print("Erro sintático: fim inesperado do arquivo")

# Constrói o parser
parser = yacc.yacc()

# Função para analisar sintaticamente o conteúdo de um arquivo
def parser_analyze(file_content):
    result = parser.parse(file_content)
    if result:
        print("Análise sintática completa.")
        print(result)
    else:
        print("Erro na análise sintática.")

# Lê o conteúdo do arquivo, similar ao lexico.py
if len(sys.argv) > 1:
    try:
        with open(sys.argv[1], "r") as file:
            file_content = file.read()
            parser_analyze(file_content)
    except FileNotFoundError:
        print("Erro ao abrir o arquivo")
        sys.exit(1)
else:
    print("Por favor, forneça um arquivo de entrada.")
    sys.exit(1)
