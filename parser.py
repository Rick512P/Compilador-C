import ply.yacc as yacc
from lexico import tokens, lexer

# Definindo a gramática para a análise sintática
def p_comandos(p):
    '''comandos : comando comandos
                | comando'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]  # Adiciona o comando à lista de comandos
    else:
        p[0] = [p[1]]  # Apenas um comando

def p_comando(p):
    '''comando : expr DELIMITADOR'''
    p[0] = ('comando', p[1])

def p_expr_atr(p):
    '''expr : ID ATR expr DELIMITADOR'''
    p[0] = ('atribuicao', p[1], p[3])

def p_expr_binaria(p):
    '''expr : expr OPA expr'''
    p[0] = (p[2], p[1], p[3])

def p_expr_numero(p):
    '''expr : NUMERO'''
    p[0] = p[1]

def p_expr_id(p):
    '''expr : ID'''
    p[0] = p[1]

def p_expr_str(p):
    '''expr : STRINGS'''
    p[0] = p[1]

def p_expr_booleano(p):
    '''expr : BOOLEAN'''
    p[0] = p[1]

def p_expr_parentese(p):
    '''expr : LDELIMITADOR expr RDELIMITADOR'''
    p[0] = p[2]

def p_comando_while(p):
    '''comando : WHILE LDELIMITADOR expr RDELIMITADOR comando'''
    p[0] = ('while', p[3], p[5])

def p_comando_if(p):
    '''comando : IF LDELIMITADOR expr RDELIMITADOR comando'''
    p[0] = ('if', p[3], p[5])

def p_comando_for(p):
    '''comando : FOR LDELIMITADOR expr DELIMITADOR expr DELIMITADOR expr RDELIMITADOR comando'''
    p[0] = ('for', p[3], p[5], p[7], p[9])

def p_error(p):
    if p:
        print(f"Erro sintático no token {p.type} com valor '{p.value}' na linha {p.lineno}")
    else:
        print("Erro sintático de fim de entrada.")

# Criação do analisador sintático
parser = yacc.yacc()

def analisar_entrada(entrada):
    return parser.parse(entrada)

def analisar_arquivo(arquivo):
    with open(arquivo, 'r') as f:
        content = f.read()
        return parser.parse(content)

def menu():
    arquivo = input("Digite o nome do arquivo para análise: ").strip()
    print("\nAnálise léxica e sintática do arquivo:")
    with open(arquivo, 'r') as f:
        conteudo = f.read()
        lexer.input(conteudo)
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok)
        print("\nAnálise sintática:")
        resultado = analisar_arquivo(arquivo)
        print("Resultado da análise sintática:", resultado)

if __name__ == "__main__":
    menu()
