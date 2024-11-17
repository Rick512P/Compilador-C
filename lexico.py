import ply.lex as lex
import sys

# Lista de tokens reconhecidos
tokens = [
    'OPA', 'OPL', 'DELIMITADOR', 'ATR', 'ID', 'NUMERO', 
    'STRING', 'LIBIMPORT', 'DEFINE', 'COMENTARIO', 'BOOLEAN', 'CHAR', 'TIPO',
    'LPAREN', 'RPAREN', 'LCHAVE', 'RCHAVE', 'LBRACKET', 'RBRACKET'
] + [
    'IF', 'ELSE', 'SWITCH', 'CASE', 'WHILE', 'DO', 'FOR'
]

# Palavras reservadas
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'switch': 'SWITCH',
    'case': 'CASE',
    'while': 'WHILE',
    'do': 'DO',
    'for': 'FOR',
    'int': 'TIPO',
    'float': 'TIPO',
    'double': 'TIPO',
    'char': 'TIPO',
    'void': 'TIPO',
    'boolean': 'BOOLEAN'
}

# Expressões regulares simples
t_OPA = r'(\+|\-|\*|\/|%|\*\*)'  # Operadores aritméticos
t_OPL = r'(==|!=|<=|>=|<|>|\+=|\-=|&&|\|\|)'  # Operadores lógicos ou relacionais
t_DELIMITADOR = r'[;,\.\:]'  # Pontuação e delimitadores sem parênteses, chaves e colchetes
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCHAVE = r'\{'
t_RCHAVE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_STRING = r'(\"[^\"]*\"|\'[^\']*\')'  # Strings (simples ou duplas)
t_LIBIMPORT = r'\#include'  # Diretiva de importação de biblioteca
t_DEFINE = r'\#define'  # Diretiva de definição
t_ATR = r'='  # Atribuição
t_COMENTARIO = r'(\/\/.*|\/\*[\s\S]*?\*\/)'  # Comentários

# Função para identificar identificadores e palavras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Verifica se é uma palavra reservada
    return t

# Função para identificar números inteiros
def t_NUMERO(t):
    r'\d+'  # Números inteiros
    t.value = int(t.value)
    return t

# Função para identificar valores booleanos
def t_BOOLEAN(t):
    r'\b(true|false)\b'  # "true" ou "false"
    t.value = t.value == 'true'
    return t

# Função para identificar caracteres (single character)
def t_CHAR(t):
    r'\'[^\']\''  # Caracter (como 'a', '1', etc.)
    t.value = t.value[1]  # Remover as aspas simples
    return t

# Função para rastrear número de linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar espaços e tabulações
t_ignore = ' \t'

# Função para tratar erros
def t_error(t):
    print(f"Caractere ilegal: {t.value[0]} na linha {t.lineno}")
    t.lexer.skip(1)

# Constrói o analisador léxico
lexer = lex.lex()

# Função para processar o conteúdo de um arquivo
def lexer_analyze(file_content):
    lexer.input(file_content)
    print("Análise léxica iniciada")
    print("| Linha | Token       | Valor                     |")
    print("|-------|-------------|---------------------------|")

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"| {tok.lineno:<5} | {tok.type:<11} | {str(tok.value):<25} |")

    print("|-------|-------------|---------------------------|")

# Esta parte será executada apenas se o lexico.py for executado diretamente, 
# não será executada quando for importado.
if __name__ == "__main__":
    # Verifica se foi passado um argumento (nome do arquivo) na linha de comando
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], "r") as file:
                file_content = file.read()
                lexer_analyze(file_content)  # Passa o conteúdo completo para o lexer
        except FileNotFoundError:
            print("Erro ao abrir o arquivo")
    else:
        print("Por favor, forneça um arquivo de entrada.")