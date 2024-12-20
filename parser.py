import re
import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens reconhecidos
tokens = [
    'OPA', 'OPL', 'DELIMITADOR', 'ATR', 'ID', 'NUMERO', 
    'STRING', 'LIBIMPORT', 'DEFINE', 'COMENTARIO', 'BOOLEAN', 'CHAR', 'TIPO',
    'LPAREN', 'RPAREN', 'LCHAVE', 'RCHAVE', 'LBRACKET', 'ASPAS', 'RBRACKET', 'VECTOR', 'MATRIX'
] + list({
    'IF', 'ELSE', 'SWITCH', 'CASE', 'WHILE', 'DO', 'FOR', 'PRINT', 'RETURN'
})

# Palavras reservadas
reserved = {
    'printf': 'PRINT',
    'return': 'RETURN',
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
t_ASPAS = r"\'|\""
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCHAVE = r'\{'
t_RCHAVE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_VECTOR = r'\[\d*\]'
t_MATRIX = r'\[\d+\]\[\d+\]'  # Reconhece formatos como [3][4]
t_STRING = r'"(\\.|[^"\\])*"|\'(\\.|[^\'\\])*\''  # Strings (simples ou duplas)
t_LIBIMPORT = r'\#(include|import)\s*<[^>]+>'  # Diretiva de importação de biblioteca
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



# Ignorar comentários de bloco
def p_comentario(t):
    """comentario : COMENTARIO"""
    pass  # Ignora o comentário de bloco    

def p_lista_declaracoes(p):
    """lista_declaracoes : lista_declaracoes declaracao
                          | declaracao"""
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_declaracao(p):
    """declaracao : declaracao_funcao
                  | declaracao_variaveis
                  | declaracao_preprocessador
                  | atribuicao"""
    p[0] = p[1]

def p_declaracao_variaveis(p):
    """declaracao_variaveis : comentario
                            | tipo lista_variaveis DELIMITADOR
                            | tipo lista_variaveis ATR expressao DELIMITADOR
                            | tipo ID VECTOR DELIMITADOR
                            | tipo ID MATRIX DELIMITADOR
                            | tipo ID VECTOR ATR expressao DELIMITADOR
                            | tipo ID MATRIX ATR expressao DELIMITADOR
                            | tipo ID CHAR ATR expressao DELIMITADOR"""
    if len(p) == 4:  # Declaração de variáveis simples
        p[0] = ('var_declaration', p[1], p[2])
    elif len(p) == 5 and '[' in p[3]:  # Declaração de vetor
        p[0] = ('vector_declaration', p[1], p[2], p[3])
    elif len(p) == 5 and '][' in p[3]:  # Declaração de matriz
        p[0] = ('matrix_declaration', p[1], p[2], p[3])

def p_declaracao_funcao(p):
    """declaracao_funcao : tipo ID LPAREN parametros RPAREN bloco
                         | tipo ID LPAREN expressao RPAREN bloco"""
    p[0] = ('func_declaration', p[1], p[2], p[4], p[6])
    

def p_declaracao_preprocessador(p):
    """declaracao_preprocessador : LIBIMPORT"""
    # Aqui, p[1] conterá algo como "#include <stdio.h>", então podemos extrair
    # o nome do arquivo que está dentro dos sinais de menor e maior.
    biblioteca = p[1].split('<')[1].split('>')[0]  # Extrai o nome do arquivo entre '<' e '>'
    p[0] = ('include', biblioteca)


def p_tipo(p):
    """tipo : TIPO '*'
            | TIPO"""
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
    """lista_parametros : lista_parametros DELIMITADOR tipo ID
                         | lista_parametros DELIMITADOR tipo ID VECTOR
                         | lista_parametros DELIMITADOR tipo ID MATRIX
                         | tipo ID
                         | tipo ID VECTOR
                         | tipo ID MATRIX
                         | lista_parametros DELIMITADOR tipo '*' ID
                         | lista_parametros DELIMITADOR tipo '*' ID VECTOR
                         | lista_parametros DELIMITADOR tipo '*' ID MATRIX
                         | tipo '*' ID
                         | tipo '*' ID VECTOR
                         | tipo '*' ID MATRIX"""
    p[0] = p[1] + [(p[3], p[4])] if len(p) == 5 else [(p[1], p[2])]

def p_bloco(p):
    """bloco : LCHAVE lista_comandos RCHAVE"""
    p[0] = ('block', p[2])

def p_lista_comandos(p):
    """lista_comandos : lista_comandos comando
                      | comando"""
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_comando(p):
    """comando :  atribuicao
                | comando_condicional
                | comando_loop
                | bloco
                | declaracao_variaveis
                | printar
                | retorno"""
    p[0] = p[1]

def p_retorno(p):
    """retorno  : RETURN expressao DELIMITADOR
                | RETURN expressao OPA ID LPAREN expressao RPAREN DELIMITADOR"""
    if len(p) == 4:  # Caso simples: return expressao;
        p[0] = ('return', p[2])
    elif len(p) == 8:  # Caso com chamada de função dentro de uma operação
        func_call = ('call', p[4], p[6])  # ('call', nome, argumento)
        p[0] = ('return', (p[3], p[2], func_call))  # operador, lado esquerdo, função

def p_atribuicao(p):
    """atribuicao : ID ATR expressao DELIMITADOR
                  | ID VECTOR ATR expressao DELIMITADOR
                  | ID MATRIX ATR expressao DELIMITADOR
                  | ID OPA OPA DELIMITADOR
                  | ID CHAR ATR ASPAS ID ASPAS"""
    if(p[2] == p[3] and p[2] == '+'):
        p[0] = ('increment', p[1])  # Nó para incremento
    elif(p[2] == p[3] and p[2] == '-'):
        p[0] = ('decrement', p[1])  # Nó para decremento
    elif len(p) == 5:  # Atribuição simples
        p[0] = ('assign', p[1], p[3])
    elif len(p) == 8:  # Atribuição a vetor
        p[0] = ('vector_assign', p[1], p[3], p[6])
    elif len(p) == 11:  # Atribuição a matriz
        p[0] = ('matrix_assign', p[1], p[3], p[6], p[9])


def p_comando_condicional(p):
    """comando_condicional : IF LPAREN expressao RPAREN bloco
                           | IF LPAREN expressao RPAREN bloco ELSE bloco
                           | IF LPAREN expressao RPAREN comando
                           | IF LPAREN expressao RPAREN comando ELSE comando"""
    if len(p) == 6:  # Caso apenas 'if (...) { bloco }'
        p[0] = ('if', p[3], p[5])
    elif len(p) == 8:  # Caso 'if (...) { bloco } else { bloco }'
        p[0] = ('if-else', p[3], p[5], p[7])  # Condição, bloco "if", bloco "else"

def p_comando_loop(p):
    """comando_loop : DO bloco WHILE LPAREN expressao RPAREN DELIMITADOR
                    | WHILE LPAREN expressao RPAREN bloco
                    | WHILE LPAREN expressao RPAREN expressao
                    | FOR LPAREN TIPO atribuicao expressao DELIMITADOR atribuicao RPAREN bloco
                    | FOR LPAREN atribuicao expressao DELIMITADOR atribuicao RPAREN bloco
                    | FOR LPAREN atribuicao expressao DELIMITADOR ID OPA OPA RPAREN bloco
                    | FOR LPAREN atribuicao expressao DELIMITADOR ID OPA OPA RPAREN expressao
                    | FOR LPAREN DELIMITADOR expressao DELIMITADOR ID OPA OPA RPAREN bloco"""
    if p[1] == 'do':
        # Caso 'do ... while'
        p[0] = ('do-while', p[2], p[5])  # Bloco e condição
    elif p[1] == 'while':
        # Caso 'while (...) { bloco }'
        p[0] = ('while', p[3], p[5])  # Condição e bloco
    elif p[1] == 'for':
        
        if len(p) == 10:  # Caso 'for (tipo inicialização; condição; incremento)'
            if p[8] == '++':  # Incremento
                incremento = ('increment', p[7])
            elif p[8] == '--':  # Decremento
                incremento = ('decrement', p[7])
            else:  # Atribuição como incremento
                incremento = p[7]
            p[0] = ('for', p[3], p[5], incremento, p[9])  # Inicialização, condição, incremento, bloco
        elif len(p) == 9:  # Caso 'for (inicialização; condição; incremento)'
            if isinstance(p[6], tuple):  # Incremento como atribuição
                p[0] = ('for', p[3], p[4], p[6], p[8])  # Inicialização, condição, incremento, bloco

def p_printar(p):
    """printar : PRINT LPAREN expressao RPAREN DELIMITADOR"""
    p[0] = ('print', p[3])


def p_expressao(p):
    """expressao : expressao OPL expressao
                 | expressao OPA expressao
                 | STRING
                 | NUMERO
                 | ID
                 | ID LPAREN expressao RPAREN
                 | ID LBRACKET expressao RBRACKET
                 | LBRACKET expressao RBRACKET
                 | ID LBRACKET expressao RBRACKET LBRACKET expressao RBRACKET
                 | LBRACKET expressao RBRACKET LBRACKET expressao RBRACKET
                 | DELIMITADOR
                 | bloco
                 | LPAREN expressao RPAREN"""
    if len(p) == 4:  # Operações aritméticas ou lógicas
        p[0] = (p[2], p[1], p[3])  # operador, lado esquerdo, lado direito
    elif len(p) == 5:  # Acesso a vetor (expressão no índice)
        p[0] = ('vector_access', p[1], p[3])  # nome, índice
    elif len(p) == 8:  # Acesso a matriz (expressões nos índices)
        p[0] = ('matrix_access', p[1], p[3], p[6])  # nome, índice1, índice2
    else:  # Casos simples (ID, NUMERO, CHAR, STRING)
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

def verificar_opl_contexto(tokens):
    """
    Verifica se os operadores '<' e '>' estão sendo usados como comparação ou delimitadores em #include.
    """
    for i, tok in enumerate(tokens):
        if tok.type == 'OPL' and tok.value in ['<', '>']:
            # Caso seja parte de um #include
            if i > 0 and tokens[i - 1].type == 'LIBIMPORT':
                print(f"'{tok.value}' identificado como delimitador de biblioteca (linha {tok.lineno}).")
            # Caso seja usado como operador de comparação
            else:
                print(f"'{tok.value}' identificado como operador de comparação (linha {tok.lineno}).")

def verificar_vetores(tokens):
    """
    Verifica o uso correto de vetores (declaração e acesso).
    """
    for i, tok in enumerate(tokens):
        if tok.type == 'VECTOR':
            # Caso seja uma declaração de vetor
            if i > 0 and tokens[i - 1].type == 'ID':
                print(f"Vetor declarado corretamente: {tokens[i-1].value}{tok.value} (linha {tok.lineno}).")
            # Caso seja acesso a um vetor
            elif i > 0 and tokens[i - 1].type == 'LBRACKET':
                print(f"Acesso ao vetor identificado: índice {tok.value} (linha {tok.lineno}).")
            else:
                print(f"Uso inválido de vetor (linha {tok.lineno}).")

def verificar_matrizes(tokens):
    """
    Verifica o uso correto de matrizes (declaração e acesso).
    """
    for i, tok in enumerate(tokens):
        if tok.type == 'MATRIX':
            # Caso seja uma declaração de matriz
            if i > 0 and tokens[i - 1].type == 'ID':
                print(f"Matriz declarada corretamente: {tokens[i-1].value}{tok.value} (linha {tok.lineno}).")
            # Caso seja acesso à matriz
            elif i > 0 and tokens[i - 1].type == 'LBRACKET':
                print(f"Acesso à matriz identificado: índices {tok.value} (linha {tok.lineno}).")
            else:
                print(f"Uso inválido de matriz (linha {tok.lineno}).")

def analisar_entrada(entrada):
    entrada = preprocess_code(entrada)
    lexer.input(entrada)

    print("\nTokens identificados:")
    tokens = []
    tok = lexer.token()
    while tok:
        tokens.append(tok)
        print(tok)
        tok = lexer.token()

    verificar_vetores(tokens)  # Verificação de vetores
    verificar_matrizes(tokens)  # Verificação de matrizes

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
        arquivo = "teste3.c"
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