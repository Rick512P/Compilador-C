# Importa a biblioteca Ply para criação do analisador léxico
import ply.lex as lex
# Importa a biblioteca sys para manipular argumentos da linha de comando
import sys

# Lista de tokens reconhecidos pelo analisador léxico
tokens = [
    'OPA', 'OPL', 'DELIMITADOR', 'ATR', 'ESPACO', 'TAB', 'NEWLINE', 
    'CARRIAGE_RETURN', 'ID', 'NUMERO', 'TIPO', 'IF', 'ELSE', 'SWITCH', 
    'CASE', 'WHILE', 'DO', 'FOR', 'COMENTARIO', 'STRINGS', 'LIBIMPORT'
]

# Expressões regulares para os tokens
t_OPA = r'(\+|\-|\*|\/|%|\*\*)'
t_OPL = r'(<|>|==|<=|=>|!=|\+=|\-=|&&|\|\|)'
t_DELIMITADOR = r'[;,\.\:\(\)\{\}\[\]]'
t_STRINGS = r'(\"[^\"]*\"|\'[^\']*\')'
t_LIBIMPORT = r'\#'
t_ATR = r'='
t_IF = r'if'
t_ELSE = r'else'
t_SWITCH = r'switch'
t_CASE = r'case'
t_WHILE = r'while'
t_DO = r'do'
t_FOR = r'for'
t_TIPO = r'(int|float|double|char|void)'
t_ESPACO = r'\s+'
t_TAB = r'\t'
t_NEWLINE = r'\n'
t_CARRIAGE_RETURN = r'\r'
t_COMENTARIO = r'(\/\/.*|\/\*[\s\S]*?\*\/)'

# Função que identifica identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

# Função que identifica números inteiros
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Função que rastreia o número de linhas ao encontrar novas linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignora espaços e tabulações
t_ignore = ' \t'

# Função que trata erros léxicos
def t_error(t):
    print(f"Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)

# Constrói o analisador léxico
lexer = lex.lex()

# Função para processar o conteúdo de um arquivo
def lexer_analyze(file_content):
    lexer.input(file_content)
    print("Análise léxica iniciada")
    print("| Linha | Token                            |")
    print("|-------|----------------------------------|")

    while True:
        tok = lexer.token()
        if not tok:
            break
        if tok.type == "NUMERO_INTEIRO" or tok.type == "IDENTIFICADOR":
            print(f"| Linha {tok.lineno} | Token: {tok.type} ({tok.value})")
        else:
            print(f"| Linha {tok.lineno} | Token: {tok.type}")

    print("|-------|----------------------------------|")

# Verifica se foi passado um argumento (nome do arquivo) na linha de comando
if len(sys.argv) > 1:
    try:
        with open(sys.argv[1], "r") as file:
            file_content = file.read()
    except FileNotFoundError:
        print("Erro ao abrir o arquivo")
        sys.exit(1)
else:
    print("Por favor, forneça um arquivo de entrada.")
    sys.exit(1)

# Chama a função de análise léxica com o conteúdo do arquivo
lexer_analyze(file_content)
