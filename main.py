import os
from parser_testes import analisar_entrada

def gerar_codigo_intermediario(no, codigo_intermediario):
    """
    Função recursiva para percorrer a árvore sintática em profundidade
    e gerar o código intermediário.
    """
    if isinstance(no, tuple):
        instrucao = None
        print(f"Processando nó: {no}")
        
        if no[0] == 'program':  # Caso o nó seja o programa principal
            # Itera sobre as instruções do programa
            for comando in no[1]:
                gerar_codigo_intermediario(comando, codigo_intermediario)
        elif no[0] == 'assign':  # Caso o nó seja uma atribuição
            # Gera código para a expressão no lado direito
            gerar_codigo_intermediario(no[2], codigo_intermediario)
            # Gera a instrução para armazenar o resultado na variável
            instrucao = ('store', no[1])

        elif no[0] in ('+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '&&', '||'):
            # Caso o nó seja uma operação aritmética ou lógica
            # Gera código para os operandos
            gerar_codigo_intermediario(no[1], codigo_intermediario)
            gerar_codigo_intermediario(no[2], codigo_intermediario)
            # Gera a instrução da operação
            instrucao = ('op', no[0])

        elif no[0] == 'if':  # Caso o nó seja uma instrução condicional
            # Gera código para a condição
            gerar_codigo_intermediario(no[1], codigo_intermediario)
            bloco_codigo = []
            # Itera sobre as instruções do bloco "if"
            for comando in no[2][1]:
                gerar_codigo_intermediario(comando, bloco_codigo)
            # Gera a instrução do bloco condicional
            instrucao = ('if', bloco_codigo)

        elif no[0] == 'for':  # Caso o nó seja um laço "for"
            # Gera código para a inicialização
            gerar_codigo_intermediario(no[1], codigo_intermediario)
            # Gera código para a condição
            gerar_codigo_intermediario(no[2], codigo_intermediario)
            bloco_codigo = []
            # Itera sobre as instruções do corpo do laço
            for comando in no[4][1]:
                gerar_codigo_intermediario(comando, bloco_codigo)
            # Gera código para o incremento
            gerar_codigo_intermediario(no[3], codigo_intermediario)
            # Gera a instrução do laço "for"
            instrucao = ('for', bloco_codigo)

        elif no[0] == 'while':  # Caso o nó seja um laço "while"
            # Gera código para a condição
            gerar_codigo_intermediario(no[1], codigo_intermediario)
            bloco_codigo = []
            # Itera sobre as instruções do corpo do laço
            for comando in no[2][1]:
                gerar_codigo_intermediario(comando, bloco_codigo)
            # Gera a instrução do laço "while"
            instrucao = ('while', bloco_codigo)

        elif no[0] == 'var_declaration':  # Declaração de variáveis
            # Gera instruções para cada variável declarada
            for var in no[2]:
                instrucao = ('declare', no[1], var)
                codigo_intermediario.append(instrucao)

        elif no[0] == 'func_declaration':  # Declaração de funções
            func_codigo = []
            # Gera código para o corpo da função
            for comando in no[4][1]:
                gerar_codigo_intermediario(comando, func_codigo)
            # Gera a instrução da função
            instrucao = ('function', no[2], no[3], func_codigo)

        # Adiciona a instrução gerada ao código intermediário
        if instrucao:
            codigo_intermediario.append(instrucao)

    elif isinstance(no, list):  # Caso o nó seja uma lista de instruções
        for sub_no in no:
            gerar_codigo_intermediario(sub_no, codigo_intermediario)

def traduzir_para_mips(codigo_intermediario):
    """
    Traduz o código intermediário gerado para o assembly do MiniMIPS.
    """
    mips_codigo = []  # Lista para armazenar as instruções em assembly
    registradores = {}  # Mapeia variáveis para registradores
    registrador_atual = 0  # Índice do registrador disponível
    labels = 0  # Contador para etiquetas únicas

    def novo_registrador():
        """
        Retorna um novo registrador disponível para uso.
        
        - Usa `nonlocal` para acessar e atualizar a variável `registrador_atual`,
        que rastreia qual registrador está sendo usado atualmente.
        - Formata o nome do registrador como `$tN`, onde N é o índice do registrador atual.
        - Incrementa o índice do registrador para o próximo uso e retorna ao início
        (registrador `$t0`) quando atingir `$t9` (usando módulo 10).
         """
        nonlocal registrador_atual
        reg = f"$t{registrador_atual}"  # Nome do registrador atual (ex.: $t0, $t1, ...)
        registrador_atual = (registrador_atual + 1) % 10  # Atualiza o índice do registrador, limitando a 10 registradores
        return reg  # Retorna o nome do registrador disponível
    
    def nova_label():
        """Gera um novo rótulo único."""
        nonlocal labels
        lbl = f"label_{labels}"
        labels += 1
        return lbl

    for instrucao in codigo_intermediario:
        if instrucao[0] == 'function':  # Declaração de função
            nome_funcao = instrucao[1]
            parametros = instrucao[2]
            corpo = instrucao[3]
            # Traduz o corpo da função
            mips_codigo.extend(traduzir_para_mips(corpo))

        elif instrucao[0] == 'store':  # Atribuição
            var = instrucao[1]
            reg = registradores.get(var, novo_registrador())
            registradores[var] = reg
            mips_codigo.append(f"sw {reg}, {var}")
        elif instrucao[0] == 'op':  # Operação aritmética ou lógica
            operador = instrucao[1]
            mips_operadores = {
                '+': 'add', '-': 'sub', '*': 'mul', '/': 'div',
                '==': 'seq', '!=': 'sne', '<': 'slt', '>': 'sgt', #SEQ usado para verificar se dois valores são iguais. Se os valores forem iguais, ele armazena o valor 1 (verdadeiro) no registrador de destino;
                '<=': 'sle', '>=': 'sge'
            }
            operacao = mips_operadores.get(operador)
            if operacao:
                op1 = novo_registrador()
                op2 = novo_registrador()
                resultado = novo_registrador()
                mips_codigo.append(f"{operacao} {resultado}, {op1}, {op2}")
        elif instrucao[0] == 'declare':  # Declaração de variáveis
            var = instrucao[2]
        elif instrucao[0] == 'if':  # Bloco condicional
            condicoes = instrucao[1]
            label_else = nova_label()
            label_end = nova_label()
            # Avalia a condição e pula para o "else" se falsa
            mips_codigo.append(f"beq $t0, $t1, {label_else}")
            # Gera código para o bloco "if"
            mips_codigo.append(f"{label_else}:")
            #for cmd in condicoes:
                #mips_codigo.append(f"# {cmd}")
            mips_codigo.append(f"j {label_end}")
            mips_codigo.append(f"{label_end}:")
    return mips_codigo
def main():
    """
    Função principal que lê o arquivo C, gera a árvore sintática
    e traduz para assembly MIPS, salvando o resultado em um arquivo .asm.
    """
    entrada_c = 'basico.c'
    try:
        with open(entrada_c, 'r') as file:
            entrada = file.read()  # Lê o código-fonte
    except FileNotFoundError:
        print(f"Erro: o arquivo '{entrada_c}' não foi encontrado.")
        return

    # Analisar o código-fonte e gerar a árvore sintática
    arvore = analisar_entrada(entrada)

    if arvore:
        print("\nGerando código intermediário...")
        codigo_intermediario = []
        gerar_codigo_intermediario(arvore, codigo_intermediario)

        # Exibir o código intermediário gerado
        print("\nCódigo intermediário gerado:")
        for instrucao in codigo_intermediario:
            print(instrucao)

        print("\nTraduzindo para assembly MiniMIPS...")
        mips_codigo = traduzir_para_mips(codigo_intermediario)

        # Exibir o código assembly gerado
        print("\nCódigo assembly gerado:")
        for linha in mips_codigo:
            print(linha)

        # Salvar o código assembly em um arquivo
        saida_asm = os.path.splitext(entrada_c)[0] + '.asm'
        with open(saida_asm, 'w') as file:
            file.write("\n".join(mips_codigo))
        print(f"\nCódigo assembly salvo em '{saida_asm}'.")
    else:
        print("Erro: não foi possível gerar o código intermediário.")

if __name__ == "__main__":
    main()
