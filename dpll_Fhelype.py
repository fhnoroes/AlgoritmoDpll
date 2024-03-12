
import json

def add_json(lista, nome_arquivo):
    try:
        # Tentar carregar o arquivo JSON existente
        with open(nome_arquivo, 'r') as arquivo_json:
            dados = json.load(arquivo_json)
    except FileNotFoundError:
        # Se o arquivo não existir, criar uma lista vazia
        dados = []

    dados.append(lista)

    # Escrever de volta no arquivo JSON
    with open(nome_arquivo, 'w') as arquivo_json:
        json.dump(dados, arquivo_json)


def excluir_ultimo_elemento(nome_arquivo):
    try:
        # Carregar os dados existentes do arquivo JSON
        with open(nome_arquivo, 'r') as arquivo_json:
            dados = json.load(arquivo_json)
    except FileNotFoundError:
        # Se o arquivo não existir, não há nada para excluir
        print("Arquivo não encontrado.")
        return

    # Verificar se há elementos para excluir
    if dados:
        # Excluir o último elemento
        dados.pop()

        # Reescrever os dados no arquivo JSON
        with open(nome_arquivo, 'w') as arquivo_json:
            json.dump(dados, arquivo_json, indent=2)  # indent=2 para uma saída mais legível

    else:
        print("A lista está vazia. Não há elementos para excluir.")

    # Escrever de volta no arquivo JSON
    with open(nome_arquivo, 'w') as arquivo_json:
        json.dump(dados, arquivo_json)

def limpar_json(nomearquivo):
#limpa arquivo JSON
    with open(nomearquivo, 'r') as arquivo:
        dados = json.load(arquivo)

    if dados:
        dados.clear()

    with open(nomearquivo, 'w') as arquivo:
        json.dump(dados, arquivo)


def ler_doc(nomearquivo):
#ler documento em cnf
    list = []
    listclausula = []
    with open(nomearquivo, 'r') as arquivo:
        for linha in arquivo:
            if (linha[0]=='c' or linha[0]=="%"):
                continue
            elif(linha[0]=='p'):
                list = linha.split()
                totvar = int(list[2])
                totclausula = int(list[3])
            else:
                list = linha.split()[:-1]
                if list != []:
                    listclausula.append(list)
#printa o total de cláusulas e variáveis
    print(f"O total de variáveis é {totvar}")
    print(f"O total de cláusulas é {totclausula}")
    return listclausula
       

def dpll(lista,var = []):
    continuar = False
    resultado = lista
    variaveis = var
    while continuar != True:
#sai do laço se não tiver nenhuma cláusula unitária para simplificar
        resultado,variaveis = unitária(resultado,variaveis)
        resultado,variaveis, continuar = pura(resultado,variaveis)
#fora do laço faz o terceiro passo do dpll, atribui um valor a variavel (verdade ou falso) e faz chamada recursiva para os passos anteriores
    resultado, variaveis = atribui(resultado,variaveis)
    if resultado == "É satisfazível":
        return "É satisfazível", variaveis
    elif resultado == "É insatisfazível":
        return "É insatisfazível", variaveis
    else:
        return "ERRO", variaveis
       

def unitária(listclausula, variaveis):
    cont = 0
    while(cont<len(listclausula)):
            #verificando para clausúla unitária
        if(len(listclausula[cont])==1):
            elemento = int(listclausula[cont][0])
            contr= 0
            if str(elemento) not in variaveis:
                variaveis.append(str(elemento))
            while(contr<len(listclausula)):
                if (str(elemento) in listclausula[contr]):
                    listclausula[contr] = "apaga"          
                elif(str(elemento*-1) in listclausula[contr]):
                        #removendo o elemento da cláusula quando tem valor contrário
                    listclausula[contr].remove(str(elemento*-1))
                contr+=1
            contr = 0
        cont+=1

#apagando a clásula quando tem o elemento unitário
    elemento = "apaga"
    while elemento in listclausula:
        listclausula.remove("apaga")

    return listclausula, variaveis
   


   


def pura(listclausula,variaveis):
#verificando elemento puro
    lista_aux = []
    lista_verif = []
    cont_adic =0
    
    for clausula in listclausula:
        for e in clausula:
            if e not in lista_verif:
                lista_verif.append(e)
        
    for e in lista_verif:
        if str(int(e)*-1) not in lista_verif:
            lista_aux.append(e)
            if e not in variaveis:
            #adiciona na lista de vars quando tomá-la como verdade
                variaveis.append(e)
            listclausula.append(lista_aux)
            cont_adic +=1
            lista_aux = []
    if cont_adic == 0:
        return listclausula,variaveis, True
    return listclausula,variaveis, False

def atribui(listclausula,variaveis):
#verifica se o que veio antes é satisfazível ou não
    if listclausula == []:
        return "É satisfazível", variaveis
    else:
        for c in listclausula:
            if c == []:
                return "É insatisfazível", variaveis

    lista = []

    for clausula in listclausula:
        for e in clausula:
                #adiciona o histórico de cláusula no json
                add_json(listclausula,'hist.json')
                #adiciona o histórico de variáveis tomadas como verdade no json
                add_json(variaveis,'histvar.json')
                if e not in variaveis:
                    variaveis.append(e)
                lista.append(e)
                listclausula.append(lista)
                #recursão tomando a variável como verdade
                recur_atribui, variaveis = dpll(listclausula,variaveis)

                if recur_atribui == "É satisfazível":
                    return "É satisfazível", variaveis
                elif recur_atribui == "É insatisfazível":
                    #caso haja um retorno insatisfazível da recursão ele exclui o elemento e adiciona o seu oposto
                    excluir_ultimo_elemento('histvar.json')
                    #carregando o último elemento registrado no json
                    with open('hist.json', 'r') as arquivo_json:
                        lista_json = arquivo_json.read()
                        lista_recuperadahist = json.loads(lista_json)
                    #carregando o ultimo elemento registrado no json
                    with open('histvar.json', 'r') as arquivo_json:
                        lista2_json = arquivo_json.read()
                        lista_varrecuperada = json.loads(lista2_json)
                    lista = []
                    lista.append(str(int(e)*-1))
                    listclausula = lista_recuperadahist[len(lista_recuperadahist)-1]
                    variaveis = lista_varrecuperada[len(lista_recuperadahist)-1]
                    variaveis.append(str(int(e)*-1))
                    listclausula.append(lista)
                    #caso o retorno seja insatisfazível ele exclui o histórico salvo e tenta com a var negativa
                    excluir_ultimo_elemento('hist.json')
                    recur_atribui, variaveis = dpll(listclausula,variaveis)
                    if recur_atribui == "É satisfazível":
                        return "É satisfazível", variaveis
                    elif recur_atribui == "É insatisfazível":
                        with open('histvar.json', 'r') as arquivo_json:
                            lista2_json = arquivo_json.read()
                            lista_varrecuperada = json.loads(lista2_json)
                        variaveis = lista_varrecuperada[len(lista_recuperadahist)-1]

                        return "É insatisfazível", variaveis
                    else:
                        return "ERRO", variaveis
                else:
                    return "ERRO", variaveis

    return "É insatisfazível", variaveis
    
r1, r2 = dpll(ler_doc('Teste2.cnf'))
#chamada da função com dois retornos, r1= satisfazível ou não, r2= variáveis que fazem eles ser satisfeito
print(f"RESULTADO: {r1}")
if r2 == []:
    print("Não há nenhuma valoração que satisfaça")
else:
    print("A valoração que satisfaz é:")
    for e in r2:
        print(e,end=' ')

limpar_json('hist.json')
limpar_json('histvar.json')

