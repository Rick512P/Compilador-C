import ply.yacc as yacc
from lexico import tokens, lexer


# Regras da gramática

# Programa inicial - ponto de entrada

def p_programa(p):
    """programa : lista_declaracoes"""
    p[0] = p[1]

# Lista de declarações
def p_lista_declaracoes(p):
    """lista_declaracoes : lista_declaracoes declaracao
                          | declaracao"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# Declarações gerais, incluindo funções e variáveis
def p_declaracao(p):
    """declaracao : declaracao_variaveis
                  | declaracao_funcao
                  | declaracao_preprocessador
                  | atribuicao"""
    p[0] = p[1]

# Declarações de variáveis
def p_declaracao_variaveis(p):
    """declaracao_variaveis : tipo lista_variaveis ';'"""
    p[0] = ('var_declaration', p[1], p[2])

# Declarações de função
def p_declaracao_funcao(p):
    """declaracao_funcao : tipo ID '(' parametros ')' bloco"""
    p[0] = ('func_declaration', p[1], p[2], p[4], p[6])

# Declarações de diretivas de pré-processador (como #include, #define)
def p_declaracao_preprocessador(p):
    """declaracao_preprocessador : LIBIMPORT ID OPL ID DELIMITADOR ID OPL
                                  | DEFINE ID NUMERO"""
    if len(p) == 6:
        p[0] = ('include', p[3], p[5])
    else:
        p[0] = ('define', p[2], p[3])

# Tipo de dados - int, void, etc.
def p_tipo(p):
    """tipo : TIPO"""
    p[0] = p[1]

# Lista de variáveis a serem declaradas
def p_lista_variaveis(p):
    """lista_variaveis : lista_variaveis ',' ID
                        | ID"""
    if len(p) == 4:
        p[0] = ('array', p[1], p[3])
    elif len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + [p[3]]

# Lista de parâmetros para funções
def p_parametros(p):
    """parametros : lista_parametros
                   | vazio"""
    p[0] = p[1]

def p_lista_parametros(p):
    """lista_parametros : lista_parametros ',' tipo ID
                         | tipo ID"""
    if len(p) == 5:
        p[0] = p[1] + [(p[3], p[4])]
    else:
        p[0] = [(p[1], p[2])]

# Bloco de comandos - definido por chaves ({})
def p_bloco(p):
    """bloco : '{' lista_comandos '}'"""
    if len(p) == 3:
        p[0] = []
    else:
        p[0] = p[2]

# Lista de comandos
def p_lista_comandos(p):
    """lista_comandos : lista_comandos comando
                      | comando"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# Definição de comandos - inclui estruturas de controle, atribuição, etc.
def p_comando(p):
    """comando : atribuicao
               | comando_condicional
               | comando_loop
               | bloco"""
    p[0] = p[1]

# Atribuições, exemplo: a = b + 1
def p_atribuicao(p):
    """atribuicao : ID ATR expressao DELIMITADOR"""
    p[0] = ('assign', p[1], p[3])

# Comando condicional - if (expressao) { comando }
def p_comando_condicional(p):
    """comando_condicional : IF '(' expressao ')' bloco"""
    if len(p) == 6:
        p[0] = ('if', p[3], p[5])
    else:
        p[0] = ('if_else', p[3], p[5], p[7])

# Comando de loop - for, while
def p_comando_loop(p):
    """comando_loop : FOR '(' atribuicao expressao ';' atribuicao ')' bloco
                    | WHILE '(' expressao ')' bloco"""
    if p[1] == 'for':
        p[0] = ('for', p[3], p[4], p[6], p[8])
    elif p[1] == 'while':
        p[0] = ('while', p[3], p[5])
    else:
        p[0] = ('do_while', p[2], p[5])

# Definição de expressões
def p_expressao(p):
    """expressao : expressao OPL expressao
                 | expressao OPA expressao
                 | ID
                 | NUMERO
                 | '(' expressao ')'"""
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    elif len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

# Regra de vazio - para produção de árvores vazias
def p_vazio(p):
    """vazio : """
    p[0] = []

# Tratamento de erro
def p_error(p):
    if p:
        print(f"Erro de sintaxe no token '{p.value}', linha {p.lineno}")
    else:
        print("Erro de sintaxe: EOF inesperado")

# Criar o analisador sintático
analisador_sintatico = yacc.yacc()

# Função para analisar a entrada e gerar a árvore de sintaxe abstrata
def analisar_entrada(entrada):
    # Exibir tokens identificados (usando o lexer do lexico.py)
    print("\nTokens identificados:")
    lexer.input(entrada)
    
    # Analisar o arquivo completo
    tok = lexer.token()  # Obter o primeiro token
    while tok:
        print(tok)  # Exibir token
        tok = lexer.token()  # Obter o próximo token

    # Analisar a entrada e gerar a árvore de sintaxe abstrata
    print("\nAnálise sintática:")
    resultado = analisador_sintatico.parse(entrada, lexer=lexer)
    print("\nResultado da análise sintática:")
    print(resultado)

# Função principal
def main():
    # Perguntar se o usuário deseja fornecer uma expressão ou um arquivo
    opcao = input("Deseja fornecer uma expressão (E) ou um arquivo (A)? ").strip().upper()

    if opcao == 'E':  # Análise de uma expressão fornecida pelo usuário
        entrada = input("Digite uma expressão para análise: ").strip()
        analisar_entrada(entrada)
    
    elif opcao == 'A':  # Análise de um arquivo fornecido pelo usuário
        arquivo = input("Digite o caminho do arquivo: ").strip()
        
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