import ply.lex as lex
import ply.yacc as yacc

# Definição dos tokens
tokens = (
    'ID',                 # Identificadores (nomes de variáveis)
    'NUM',                # Números
    'MAIS',               # Operador soma
    'MENOS',              # Operador subtração
    'MULT',               # Operador multiplicação
    'DIV',                # Operador divisão
    'PONTO_VIRGULA',      # Ponto e vírgula
    'IGUAL',              # Operador de atribuição
)

# Expressões regulares para os tokens
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'  # Identificadores
t_NUM = r'\d+'  # Números
t_MAIS = r'\+'
t_MENOS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_IGUAL = r'='
t_PONTO_VIRGULA = r';'

# Ignorar espaços e tabulações
t_ignore = ' \t'

# Função de erro para caracteres inválidos
def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

# Criar o analisador léxico
analisador_lexico = lex.lex()

# Regras de precedência para operadores
precedencia = (
    ('left', 'MAIS', 'MENOS'),
    ('left', 'MULT', 'DIV'),
)

# Regras de produção (gramática)
def p_atribuicao(p):
    '''atribuicao : ID IGUAL expressao PONTO_VIRGULA'''
    p[0] = ('atribuicao', p[1], p[3])  # ('atribuicao', nome_da_variavel, valor)

def p_expressao(p):
    '''expressao : expressao MAIS expressao
                 | expressao MENOS expressao
                 | expressao MULT expressao
                 | expressao DIV expressao'''
    p[0] = (p[2], p[1], p[3])  # ('operador', lado_esquerdo, lado_direito)

def p_expressao_numero(p):
    'expressao : NUM'
    p[0] = ('numero', int(p[1]))  # ('numero', valor)

def p_expressao_id(p):
    'expressao : ID'
    p[0] = ('id', p[1])  # ('id', nome_da_variavel)

# Função para capturar erros de sintaxe
def p_error(p):
    if p:
        print(f"Erro de sintaxe no token '{p.value}'")
    else:
        print("Erro de sintaxe! Fim da entrada inesperado.")

# Criar o analisador sintático
analisador_sintatico = yacc.yacc()

# Receber entrada do usuário
entrada = input("Digite uma expressão para análise: ")

# Limpeza adicional na entrada
entrada = entrada.strip()
print(f"\nEntrada limpa: {entrada}")

# Usar o lexer diretamente para ver a sequência de tokens
analisador_lexico.input(entrada)
print("\nTokens identificados:")
for token in analisador_lexico:
    print(token)

# Analisar a entrada e gerar a árvore de sintaxe abstrata
resultado = analisador_sintatico.parse(entrada)
print("\nResultado da análise sintática:")
print(resultado)

