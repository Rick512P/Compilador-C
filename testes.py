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
            instrucao = ('store', no[2], no[1])

        elif no[0] == 'return':  # Caso o nó seja um retorno
            # Gera código para a expressão de retorno
            gerar_codigo_intermediario(no[1], codigo_intermediario)
            instrucao = ('return', no[1])  # Gera a instrução de retorno

        elif no[0] == 'increment':  # Caso o nó seja um incremento
            # Adiciona a operação de incremento (n = n + 1)
            instrucao = ('op', '+', no[1], 1)
            #gerar_codigo_intermediario(no, )
            codigo_intermediario.append(instrucao)
            instrucao = ('store', ('+', no[1], 1), no[1])

        elif no[0] == 'decrement':  # Caso o nó seja um decremento
            # Adiciona a operação de decremento (n = n - 1)
            instrucao = ('op', '-', no[1], 1)
            codigo_intermediario.append(instrucao)
            instrucao = ('store', ('-', no[1], 1), no[1])    

        elif no[0] in ('+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '&&', '||'):
            # Caso o nó seja uma operação aritmética ou lógica
            # Gera código para os operandos
            gerar_codigo_intermediario(no[1], codigo_intermediario)
            gerar_codigo_intermediario(no[2], codigo_intermediario)
            # Gera a instrução da operação
            instrucao = ('op', no[0], no[1], no[2])

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
            start_label = f"label_start_{len(codigo_intermediario)}"
            end_label = f"label_end_{len(codigo_intermediario)}"
            
            # Adiciona o rótulo de início do laço
            codigo_intermediario.append(('label', start_label))
            
            # Gera código para a condição
            gerar_codigo_intermediario(no[1], codigo_intermediario)
            
            # Gera a instrução para pular para o fim caso a condição seja falsa
            codigo_intermediario.append(('jump_if_false', end_label))
            
            # Gera código para o corpo do laço
            for comando in no[2][1]:
                gerar_codigo_intermediario(comando, codigo_intermediario)
            
            # Salta de volta para o início do laço
            codigo_intermediario.append(('jump', start_label))
            
            # Adiciona o rótulo de fim do laço
            codigo_intermediario.append(('label', end_label))


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

def verifica_sw(mips_codigo):
    """
    Função que reorganiza o código MIPS para verificar instruções 'sw'
    e utilizar o registrador da linha anterior.
    """
    i = 1  # Começa em 1 para poder acessar a linha anterior
    while i < len(mips_codigo):
        linha_atual = mips_codigo[i]
        linha_anterior = mips_codigo[i - 1]

        # Exemplo: verifica 'sw' na linha atual
        if 'sw' in linha_atual and '(' in linha_atual:
            # Transformar linha_anterior em um vetor (lista) usando split com vírgula
            vetor_linha_atual = linha_atual.split(' (')  # Divide por vírgulas
            vetor_linha_anterior = linha_anterior.replace(" ", "").split('$')  # Divide por vírgulas    
            vetor_linha_anterior[1] = vetor_linha_anterior[1].replace(",", "")
            print(f"Vetor da linha anterior: {vetor_linha_anterior}")
            
            vetor_linha_atual[1] = '$' + vetor_linha_anterior[1]
            linha_atual_modificada = ' '.join(vetor_linha_atual)  # Junta os elementos com vírgula
            
            mips_codigo[i] = linha_atual_modificada
            print(f"Vetor linha atual: {vetor_linha_atual}")
            if len(vetor_linha_anterior) > 1:  # Garante que exista um índice 1
                print(f"Segundo elemento do vetor: {vetor_linha_anterior[1]}")
            else:
                print("A linha anterior não tem um segundo elemento após a vírgula.")
        
        i += 1  # Incrementa o índice para continuar
    return mips_codigo




def traduzir_para_mips(codigo_intermediario):
    """
    Traduz o código intermediário gerado para o assembly do MiniMIPS.
    """
    mips_codigo = []  # Lista para armazenar as instruções em assembly
    registradores = {}  # Mapeia variáveis para registradores
    registrador_atual = 0  # Índice do registrador disponível
    labels = 0  # Contador para etiquetas únicas

    def novo_registrador(x):
        """
        Retorna um novo registrador disponível para uso.
        """

        nonlocal registrador_atual
        reg = f"$t{registrador_atual}"  # Seleciona o registrador atual
        registrador_atual = (registrador_atual + 1) % 10  # Atualiza o índice para o próximo registrador
        printar = (f"sw {reg}, {x}")  # Gera a instrução de store
        return reg, printar
    
    def novo_registrador_resultado():
        """
        Retorna um novo registrador disponível para uso.
        """

        nonlocal registrador_atual
        reg = f"$t{registrador_atual}"  # Seleciona o registrador atual
        registrador_atual = (registrador_atual + 1) % 10  # Atualiza o índice para o próximo registrador
        return reg
    
    def nova_label():
        """Gera um novo rótulo único."""
        nonlocal labels
        lbl = f"label_{labels}"
        labels += 1
        return lbl

    for instrucao in codigo_intermediario:
        #print("Instrucao: ", instrucao)
        if instrucao[0] == 'function':  # Declaração de função
            corpo = instrucao[3]
            # Traduz o corpo da função
            mips_codigo.extend(traduzir_para_mips(corpo))

        elif instrucao[0] == 'store':  # Atribuição
            var = instrucao[1]
            var2 = instrucao[2]
            reg = registradores.get(var, novo_registrador_resultado())
            registradores[var] = reg
            mips_codigo.append(f"sw {reg}, {var} # {var2}")

        elif instrucao[0] == 'return':  # Instrução de retorno
            valor = instrucao[1]
            reg, load_instrucao = novo_registrador(valor)
            mips_codigo.append(load_instrucao)  # Gera instrução para carregar o valor
            mips_codigo.append(f"move $v0, {reg}")  # Move o valor para $v0 (registrador de retorno)
            mips_codigo.append("jr $ra")  # Retorna ao chamador
    
        elif instrucao[0] == 'op':  # Operação aritmética ou lógica
            operador = instrucao[1]
            mips_operadores = {
                '+': 'add', '-': 'sub', '*': 'mul', '/': 'div',
                '==': 'seq', '!=': 'sne', '<': 'slt', '>': 'sgt',
                '<=': 'sle', '>=': 'sge'
            }
            print("Instrucao: ", instrucao)
            print("Operador: ", mips_operadores.get(operador))
            operacao = mips_operadores.get(operador)
            if operacao:
                op1 = novo_registrador(instrucao[2])
                op2 = novo_registrador(instrucao[3])
                resultado = novo_registrador_resultado()
                mips_codigo.append(f"{op1[1]}")
                mips_codigo.append(f"{op2[1]}")
                mips_codigo.append(f"{operacao} {resultado}, {op1[0]}, {op2[0]}")

        elif instrucao[0] == 'for':  # Laço "for"
            bloco_for = instrucao[1]  # Bloco "for"
            start_label = nova_label()
            end_label = nova_label()

            # Adiciona o rótulo de início do laço
            mips_codigo.append(f"{start_label}:")
            # Gera código para as operações do corpo do laço
            bloco_for_traduzido = traduzir_para_mips(bloco_for)
            mips_codigo.extend(bloco_for_traduzido)
            # Salta de volta para o início
            mips_codigo.append(f"j {start_label}")
            # Adiciona o rótulo de fim do laço
            mips_codigo.append(f"{end_label}:")
            
        elif instrucao[0] == 'declare':  # Declaração de variáveis
            var = instrucao[2]
        elif instrucao[0] == 'if':  # Bloco condicional
            bloco_if = instrucao[1]   # Bloco "if"

            # Criação dos labels
            label_if = nova_label()  # Label para o bloco "if"
            label_end = nova_label() # Label para o final do "if"

            # Adiciona instrução para pular para o bloco "end" se a condição for falsa
            mips_codigo.append(f"beq $t0, $zero, {label_if}")
            # Adiciona o salto para o final, para evitar execução do código subsequente
            mips_codigo.append(f"j {label_end}")

            # Adiciona o bloco "if" associado ao rótulo
            mips_codigo.append(f"{label_if}:")
            bloco_if_traduzido = traduzir_para_mips(bloco_if)
            for i in range(len(bloco_if_traduzido)):
                mips_codigo.append(f"    {bloco_if_traduzido[i]}")


            # Adiciona o rótulo do final do bloco "if"
            mips_codigo.append(f"{label_end}:")


        elif instrucao[0] == 'while':  # Laço "while"
            start_label = nova_label()
            end_label = nova_label()
            # Adiciona o rótulo de início do laço
            mips_codigo.append(f"{start_label}:")
            # Gera código para a condição
            mips_codigo.extend(traduzir_para_mips([instrucao[1]]))
            # Salta para o fim se a condição for falsa
            mips_codigo.append(f"beq $t0, $zero, {end_label}")
            # Gera código para o corpo do laço
            for cmd in instrucao[1]:
                mips_codigo.extend(traduzir_para_mips([cmd]))
            # Salta de volta para o início
            mips_codigo.append(f"j {start_label}")
            # Adiciona o rótulo de fim do laço
            mips_codigo.append(f"{end_label}:")

        elif instrucao[0] == 'label':  # Rótulos
            mips_codigo.append(f"{instrucao[1]}:")
        
        elif instrucao[0] == 'jump':  # Salto incondicional
            destino = instrucao[1]
            mips_codigo.append(f"j {destino}")
        
        


    # Adiciona jumps aos blocos de código conforme necessário
    mips_codigo = adiciona_jump(mips_codigo)
    mips_codigo = verifica_sw(mips_codigo)
    

    return mips_codigo

def adiciona_jump(mips_codigo):
    """
    Ajusta o código MIPS para garantir que, em blocos apontados por `beq`,
    seja inserido um único `j END` dentro do label correspondente, apenas se o bloco tiver código.
    """
    i = 0
    while i < len(mips_codigo):
        if mips_codigo[i].startswith("beq"):
            # Extrai o label para onde o `beq` pula
            partes = mips_codigo[i+1].split()
            destino = partes[-1]  # O label de destino do `jump`
            linha_destino = None

            # Localiza o rótulo apontado pelo `jump`
            for j, instrucao in enumerate(mips_codigo):
                if instrucao.startswith(f"{destino}:"):
                    linha_destino = j
                    break

            if linha_destino is not None:
                # Verifica se há instruções associadas ao label
                bloco = mips_codigo[linha_destino - 1:]
                bloco_valido = any(
                    not instrucao.strip().startswith(("j", "END:", destino)) and instrucao.strip()
                    for instrucao in bloco
                )

                if bloco_valido:
                    # Verifica se já existe um `j END` dentro do bloco
                    jump_existe = any(instrucao.strip() == "j END" for instrucao in bloco)

                    if not jump_existe:
                        # Adiciona `END:` ao final do código, se necessário
                        if "END:" not in mips_codigo:
                            mips_codigo.append("END:")

                        # Insere o `j END` dentro do bloco
                        mips_codigo.insert(linha_destino, "    j END")
        i += 1
    return mips_codigo




def main():
    """
    Função principal que lê o arquivo C, gera a árvore sintática
    e traduz para assembly MIPS, salvando o resultado em um arquivo .asm.
    """
    entrada_c = 'teste2.c'
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
