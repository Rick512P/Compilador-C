import re
import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens reconhecidos
tokens = [
    'OPA', 'OPL', 'DELIMITADOR', 'ATR', 'ID', 'NUMERO', 
    'STRING', 'LIBIMPORT', 'DEFINE', 'COMENTARIO', 'BOOLEAN', 'CHAR', 'TIPO',
    'LPAREN', 'RPAREN', 'LCHAVE', 'RCHAVE', 'LBRACKET', 'RBRACKET'
] + list({
    'IF', 'ELSE', 'SWITCH', 'CASE', 'WHILE', 'DO', 'FOR'
})

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

def merge_dicts(d1, d2):
    return {**d1, **d2}

tokens = list(merge_dicts(reserved, {t: t for t in tokens}).values())

# Expressões regulares simples
t_OPA = r'(\+|\-|\*|\/|%|\*\*)'  # Operadores aritméticos
t_OPL = r'(==|!=|<=|>=|<|>|\+=|\-=|&&|\|\|)'  # Operadores lógicos ou relacionais
t_DELIMITADOR = r'[;,\.:]'  # Pontuação e delimitadores sem parênteses, chaves e colchetes
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCHAVE = r'\{'
t_RCHAVE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_STRING = r'"(\\.|[^"\\])*"|\'(\\.|[^\'\\])*\''  # Strings (simples ou duplas)
t_LIBIMPORT = r'\#include'  # Diretiva de importação de biblioteca
t_DEFINE = r'\#define'  # Diretiva de definição
t_ATR = r'='  # Atribuição
t_COMENTARIO = r'(\/\/.*|\/\*[\s\S]*?\*\/)'  # Comentários

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Verifica se é uma palavra reservada
    return t

def t_NUMERO(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_CHAR(t):
    r"'[^']'"
    t.value = t.value[1]
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print(f"Caractere ilegal: {t.value[0]} na linha {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

# Regras da gramática
def p_programa(p):
    """programa : lista_declaracoes"""
    p[0] = ('program', p[1])

def p_lista_declaracoes(p):
    """lista_declaracoes : lista_declaracoes declaracao
                          | declaracao"""
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_declaracao(p):
    """declaracao : declaracao_variaveis
                  | declaracao_funcao
                  | declaracao_preprocessador
                  | atribuicao"""
    p[0] = p[1]

def p_declaracao_variaveis(p):
    """declaracao_variaveis : tipo lista_variaveis DELIMITADOR"""
    p[0] = ('var_declaration', p[1], p[2])

def p_declaracao_funcao(p):
    """declaracao_funcao : tipo ID LPAREN parametros RPAREN bloco"""
    p[0] = ('func_declaration', p[1], p[2], p[4], p[6])

def p_declaracao_preprocessador(p):
    """declaracao_preprocessador : LIBIMPORT '<' ID '.' ID '>'"""
    p[0] = ('include', f"{p[3]}.{p[5]}")

def p_tipo(p):
    """tipo : TIPO"""
    p[0] = p[1]

def p_lista_variaveis(p):
    """lista_variaveis : lista_variaveis ',' ID
                        | ID"""
    p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]

def p_parametros(p):
    """parametros : lista_parametros
                   | vazio"""
    p[0] = p[1]

def p_lista_parametros(p):
    """lista_parametros : lista_parametros ',' tipo ID
                         | tipo ID"""
    p[0] = p[1] + [(p[3], p[4])] if len(p) == 5 else [(p[1], p[2])]

def p_bloco(p):
    """bloco : LCHAVE lista_comandos RCHAVE"""
    p[0] = ('block', p[2])

def p_lista_comandos(p):
    """lista_comandos : lista_comandos comando
                      | comando"""
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_comando(p):
    """comando : atribuicao
               | comando_condicional
               | comando_loop
               | bloco"""
    p[0] = p[1]

def p_atribuicao(p):
    """atribuicao : ID ATR expressao DELIMITADOR"""
    p[0] = ('assign', p[1], p[3])

def p_comando_condicional(p):
    """comando_condicional : IF LPAREN expressao RPAREN bloco"""
    p[0] = ('if', p[3], p[5])

def p_comando_loop(p):
    """comando_loop : WHILE LPAREN expressao RPAREN bloco"""
    p[0] = ('while', p[3], p[5])

def p_expressao(p):
    """expressao : expressao OPL expressao
                 | expressao OPA expressao
                 | LPAREN expressao RPAREN
                 | ID
                 | NUMERO"""
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_vazio(p):
    """vazio : """
    p[0] = []

def p_error(p):
    if p:
        print(f"Erro de sintaxe no token '{p.value}', linha {p.lineno}")
    else:
        print("Erro de sintaxe: EOF inesperado")

parser = yacc.yacc()

def preprocess_code(code):
    defines = {}
    for line in code.splitlines():
        match = re.match(r'#define\s+(\w+)\s+(\d+)', line)
        if match:
            defines[match.group(1)] = match.group(2)
    for macro, value in defines.items():
        code = re.sub(rf'\b{macro}\b', value, code)
    code = re.sub(r'#define\s+\w+\s+\d+', '', code)
    return code

def analisar_entrada(entrada):
    entrada = preprocess_code(entrada)
    lexer.input(entrada)
    print("\nTokens identificados:")
    tok = lexer.token()
    while tok:
        print(tok)
        tok = lexer.token()

    print("\nAnálise sintática:")
    resultado = parser.parse(entrada, lexer=lexer)
    print("\nEstrutura da árvore sintática:")
    print(resultado)

    if resultado:
        print("\nÁrvore gerada com sucesso!")
        return resultado
    else:
        print("\nErro na geração da árvore.")
        return None

def main():
    #opcao = input("Deseja fornecer uma expressão (E) ou um arquivo (A)? ").strip().upper()
    opcao = "A"
    if opcao == 'E':
        entrada = input("Digite uma expressão para análise: ").strip()
        analisar_entrada(entrada)
    elif opcao == 'A':
        #arquivo = input("Digite o caminho do arquivo: ").strip()
        arquivo = "q.c"
        try:
            with open(arquivo, 'r') as file:
                conteudo = file.read().strip()
                analisar_entrada(conteudo)
        except FileNotFoundError:
            print(f"Erro: O arquivo '{arquivo}' não foi encontrado.")
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
    else:
        print("Opção inválida. Por favor, escolha 'E' para expressão ou 'A' para arquivo.")

if __name__ == "__main__":
    main()