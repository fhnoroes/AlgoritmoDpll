
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


def ler_doc():
    list = []
    listclausula = []
    with open('teste2.cnf', 'r') as arquivo:
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
    print(f"O total de variáveis é {totvar}")
    print(f"O total de cláusulas é {totclausula}")
    return listclausula
       
def limpar_json(nomearquivo):
    with open(nomearquivo, 'r') as arquivo:
        dados = json.load(arquivo)

    if dados:
        dados.clear()

    with open(nomearquivo, 'w') as arquivo:
        json.dump(dados, arquivo)

def dpll(lista,var = []):
    continuar = False
    resultado = lista
    variaveis = var
    while continuar != True:
        resultado,variaveis = unitária(resultado,variaveis)
        resultado,variaveis, continuar = pura(resultado,variaveis)
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
    #tentar arrumar uma maneira de não precisar verificar todos depois que achei o que eu queria
    for clausula in listclausula:
        for e in clausula:
            if e not in lista_verif:
                lista_verif.append(e)
        
    for e in lista_verif:
        if str(int(e)*-1) not in lista_verif:
            lista_aux.append(e)
            if e not in variaveis:
                variaveis.append(e)
            listclausula.append(lista_aux)
            cont_adic +=1
            lista_aux = []
    if cont_adic == 0:
        return listclausula,variaveis, True
    return listclausula,variaveis, False

def atribui(listclausula,variaveis):
    if listclausula == []:
        return "É satisfazível", variaveis
    else:
        for c in listclausula:
            if c == []:
                return "É insatisfazível", variaveis

    lista = []

    for clausula in listclausula:
        for e in clausula:
                add_json(listclausula,'hist.json')
                add_json(variaveis,'histvar.json')
                if e not in variaveis:
                    variaveis.append(e)
                lista.append(e)
                listclausula.append(lista)
                recur_atribui, variaveis = dpll(listclausula,variaveis)


                if recur_atribui == "É satisfazível":
                    return "É satisfazível", variaveis
                elif recur_atribui == "É insatisfazível":
                    excluir_ultimo_elemento('histvar.json')
                    with open('hist.json', 'r') as arquivo_json:
                        lista_json = arquivo_json.read()
                        lista_recuperadahist = json.loads(lista_json)
                    with open('histvar.json', 'r') as arquivo_json:
                        lista2_json = arquivo_json.read()
                        lista_varrecuperada = json.loads(lista2_json)
                    lista = []
                    lista.append(str(int(e)*-1))
                    listclausula = lista_recuperadahist[len(lista_recuperadahist)-1]
                    variaveis = lista_varrecuperada[len(lista_recuperadahist)-1]
                    variaveis.append(str(int(e)*-1))
                    listclausula.append(lista)
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
                    # Aqui, podemos ajustar a lógica conforme necessário
                    return "ERRO", variaveis

    # Caso chegue ao final do loop sem retornar, retornamos algo como "Não foi possível determinar"
    return "É insatisfazível", variaveis
            






    
r1, r2 = dpll(ler_doc())
print(f"RESULTADO: {r1}")
if r2 == []:
    print("Não há nenhuma valoração que satisfaça")
else:
    print("A valoração que satisfaz é:")
    for e in r2:
        print(e,end=' ')

limpar_json('hist.json')
limpar_json('histvar.json')

