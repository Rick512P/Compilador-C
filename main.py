import os
from parser_testes import analisar_entrada

def gerar_codigo_intermediario(no, codigo_intermediario):
    """
    Função recursiva para percorrer a árvore sintática em profundidade
    e gerar o código intermediário.
    """
    if isinstance(no, tuple):
        instrucao = None
        if no[0] == 'assign':
            gerar_codigo_intermediario(no[2], codigo_intermediario)  # Gera código para a expressão
            instrucao = ('store', no[1])
        elif no[0] in ('+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '&&', '||'):
            gerar_codigo_intermediario(no[1], codigo_intermediario)
            gerar_codigo_intermediario(no[2], codigo_intermediario)
            instrucao = ('op', no[0])
        elif no[0] == 'if':
            gerar_codigo_intermediario(no[1], codigo_intermediario)  # Condição
            bloco_codigo = []
            for comando in no[2][1]:
                gerar_codigo_intermediario(comando, bloco_codigo)
            instrucao = ('if', bloco_codigo)
        elif no[0] == 'for':
            gerar_codigo_intermediario(no[1], codigo_intermediario)  # Atribuição
            gerar_codigo_intermediario(no[2], codigo_intermediario)  # Condição
            bloco_codigo = []
            for comando in no[4][1]:
                gerar_codigo_intermediario(comando, bloco_codigo)
            gerar_codigo_intermediario(no[3], codigo_intermediario)  # Incremento
            instrucao = ('for', bloco_codigo)
        elif no[0] == 'while':
            gerar_codigo_intermediario(no[1], codigo_intermediario)  # Condição
            bloco_codigo = []
            for comando in no[2][1]:
                gerar_codigo_intermediario(comando, bloco_codigo)
            instrucao = ('while', bloco_codigo)
        elif no[0] == 'var_declaration':
            for var in no[2]:
                instrucao = ('declare', no[1], var)
                codigo_intermediario.append(instrucao)
        elif no[0] == 'func_declaration':
            func_codigo = []
            for comando in no[4][1]:
                gerar_codigo_intermediario(comando, func_codigo)
            instrucao = ('function', no[2], no[3], func_codigo)

        if instrucao:
            codigo_intermediario.append(instrucao)
    elif isinstance(no, list):
        for sub_no in no:
            gerar_codigo_intermediario(sub_no, codigo_intermediario)

def traduzir_para_mips(codigo_intermediario):
    """
    Traduz o código intermediário gerado para o assembly do MiniMIPS.
    """
    mips_codigo = []
    registradores = {}
    registrador_atual = 0

    def novo_registrador():
        nonlocal registrador_atual
        reg = f"$t{registrador_atual}"
        registrador_atual = (registrador_atual + 1) % 10
        return reg

    for instrucao in codigo_intermediario:
        if instrucao[0] == 'store':
            var = instrucao[1]
            reg = registradores.get(var, novo_registrador())
            registradores[var] = reg
            mips_codigo.append(f"sw {reg}, {var}")
        elif instrucao[0] == 'op':
            operador = instrucao[1]
            mips_operadores = {
                '+': 'add', '-': 'sub', '*': 'mul', '/': 'div',
                '==': 'seq', '!=': 'sne', '<': 'slt', '>': 'sgt',
                '<=': 'sle', '>=': 'sge'
            }
            operacao = mips_operadores.get(operador, None)
            if operacao:
                op1 = novo_registrador()
                op2 = novo_registrador()
                resultado = novo_registrador()
                mips_codigo.append(f"{operacao} {resultado}, {op1}, {op2}")
        elif instrucao[0] == 'declare':
            mips_codigo.append(f"# Declarando variável {instrucao[2]} do tipo {instrucao[1]}")
        elif instrucao[0] == 'if':
            mips_codigo.append("# Início do bloco condicional")
            for comando in instrucao[1]:
                mips_codigo.append(f"# {comando}")
            mips_codigo.append("# Fim do bloco condicional")

    return mips_codigo

def main():
    """
    Função principal que lê o arquivo C, gera a árvore sintática
    e traduz para assembly MIPS, salvando o resultado em um arquivo .asm.
    """
    entrada_c = 'q.c'
    try:
        with open(entrada_c, 'r') as file:
            entrada = file.read()
    except FileNotFoundError:
        print(f"Erro: o arquivo '{entrada_c}' não foi encontrado.")
        return

    arvore = analisar_entrada(entrada)

    if arvore:
        print("\nGerando código intermediário...")
        codigo_intermediario = []
        gerar_codigo_intermediario(arvore, codigo_intermediario)

        print("\nCódigo intermediário gerado:")
        for instrucao in codigo_intermediario:
            print(instrucao)

        print("\nTraduzindo para assembly MiniMIPS...")
        mips_codigo = traduzir_para_mips(codigo_intermediario)

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
