import ply.yacc as yacc
from lexico import tokens, lexer  # Importa tokens e o lexer do lexico.py

# Regras de precedência para operadores
precedencia = (
    ('left', 'OPA'),  # Operadores aritméticos + e -
    ('left', 'OPL'),  # Operadores lógicos ou relacionais
)

# Regras de produção (gramática)

# Programa (sequência de declarações e atribuições)
def p_programa(p):
    '''programa : programa declaracao
               | programa atribuicao
               | declaracao
               | atribuicao'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]  # Adiciona a instrução no programa
    else:
        p[0] = [p[1]]  # Primeira instrução no programa

# Atribuição: ID = expressao;
def p_atribuicao(p):
    '''atribuicao : ID ATR expressao DELIMITADOR'''
    p[0] = ('atribuicao', p[1], p[3])  # ('atribuicao', variável, valor)

# Declaração de variáveis: tipo ID (, ID)* DELIMITADOR
def p_declaracao(p):
    '''declaracao : TIPO lista_ids DELIMITADOR
                  | BOOLEAN lista_ids DELIMITADOR'''
    p[0] = ('declaracao', p[1], p[2])  # ('declaracao', tipo, lista de IDs)

# Lista de identificadores: ID (, ID)*
def p_lista_ids(p):
    '''lista_ids : ID
                 | lista_ids DELIMITADOR ID'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# Expressões aritméticas
def p_expressao(p):
    '''expressao : expressao OPA expressao
                 | NUMERO
                 | ID'''
    if len(p) == 4:  # Caso tenha um operador
        p[0] = (p[2], p[1], p[3])  # ('operador', lado_esquerdo, lado_direito)
    else:  # Caso seja um número ou identificador
        p[0] = p[1]

# Expressões lógicas (relacionais ou lógicas)
def p_expressao_logica(p):
    '''expressao : expressao OPL expressao'''
    p[0] = (p[2], p[1], p[3])  # ('operador lógico', lado_esquerdo, lado_direito)

# Atribuição com booleano
def p_atribuicao_boolean(p):
    '''atribuicao : ID ATR BOOLEAN DELIMITADOR'''
    p[0] = ('atribuicao', p[1], p[3])  # Atribuição de valor booleano

# Estrutura de laços: for
def p_for(p):
    '''for : FOR DELIMITADOR '(' declaracao expressao DELIMITADOR expressao DELIMITADOR ')' LDELIMITADOR programa RDELIMITADOR'''
    p[0] = ('for', p[4], p[5], p[6], p[8])  # ('for', declaração, condição, incremento, bloco de código)

# Função para capturar erros de sintaxe
def p_error(p):
    if p:
        print(f"Erro de sintaxe no token '{p.value}', linha {p.lineno}")
    else:
        print("Erro de sintaxe! Fim inesperado.")

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
