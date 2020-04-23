import numpy


#Função para transferir os dados do arquivo para a estrutura do algoritmo,
#cada linha possui um valor para cada atributo de entrada e um valor para saída
#A função recebe um conjunto de dados "f" e quantas linhas "numExamples" serão utilizadas
def InitExamples(f, numExamples):
    l = f.readlines()
    a = []    
    
    for x in range(len(l)):
        newLine = []
        rChar = ""
        
        for y in range(len(l[x])):
            if l[x][y] == ',':
                aux1 = float(rChar)
                newLine.append(aux1)
                rChar = ""

            elif l[x][y] == '\n':
                newLine.append(rChar)
                rChar = ""

            elif x == len(l)-1 and y == len(l[x])-1:
                rChar += l[x][y]
                newLine.append(rChar)

            else:
                rChar += l[x][y]
                
        if len(a) < numExamples:
            a.append(newLine)

    #print("tam f: ", len(a))
    return a

#Cálculo da informação obtida utilizando um determinado atributo
#A função recebe um conjunto de exemplos e o atributo escolhido
#Para comparar cada valor possivel do atributo, a função divide os valores em dois conjuntos:
#conjunto de valores menor do que a média, e conjunto de valores maior/igual a média
#
def Remainder(examples, atribbute):

    remainder = 0
    out = {""}
    output = []

    meanCount = 0    
    for x in range(len(examples)):
        #print("ex ", examples[x])
        out.add(examples[x][-1])
        meanCount += examples[x][atribbute]

    
    meanVal = meanCount/(len(examples))
    #meanVal = round(meanVal, 3)
    #print("mean remainder: ", meanVal)
    
    for x in out:
        output.append(x)

    #print("all outputs: ", out)
    del output[0]

    #Every possible value of A
    #Divide all values comparing to the mean 

    exValuesLess = []
    exValuesGreater = []

    for j in range(len(examples)):
        if examples[j][atribbute] < meanVal:
            aux = []
            aux.append(examples[j][atribbute])
            aux.append(examples[j][-1])
            exValuesLess.append(aux)
            
        else:            
            aux = []
            aux.append(examples[j][atribbute])
            aux.append(examples[j][-1])
            exValuesGreater.append(aux)

    outProbLess = []
    outProbGreater = []
    
    countTL = 0
    countTG = 0
    for j in range(len(output)):
        countL = 0
        countG = 0

        for k in range(len(exValuesLess)):
            if output[j] == exValuesLess[k][-1]:
                countL+=1

        outProbLess.append(countL)
        countTL += countL

        for k in range(len(exValuesGreater)):
            if output[j] == exValuesGreater[k][-1]:
                countG+=1

        outProbGreater.append(countG)
        countTG += countG

    outProbLess[:] = [x / countTL for x in outProbLess]
    outProbGreater[:] = [x / countTG for x in outProbGreater]

    #Information on values less than mean

    r1 = 0
    c = 0
    for j in outProbLess:
        if j != 0:
            c += (-1)*j*numpy.log2(j)

    r1 = (countTL/(countTL+countTG))*c

    #Information on values greater than mean

    r2 = 0
    c = 0
    for j in outProbGreater:
        if j != 0:
            c += (-1)*j*numpy.log2(j)

    r2 = (countTG/(countTL+countTG))*c
    
    remainder = r1 + r2

    #print("remainder A = ", remainder)
    return remainder

#Cálculo da informação contida no conjunto de exemplos
#A função recebe o conjunto de exemplos, com os valores das entradas e saída

def InfoGlobal(examples):

    #Find all target outputs
    targets = {""}

    for i in examples:
        targets.add(i[-1])

    target = []
    for x in targets:
        target.append(x)

    del target[0]
    probTarget = []

    for x in target:
        count = 0
        
        for y in examples:
            if x == y[-1]:
                count+=1

        probTarget.append(count)

    probTarget[:] = [x / len(examples) for x in probTarget]

    #Information

    ig1 = 0
    for x in probTarget:
        ig1 += x*numpy.log2(x)*(-1)

    return ig1

#Classe auxiliar para representar um nó na árvore de decisão
#Variável "mode" possui o valor 0 para representar um nó com valor da saída,
#e possui o valor 1 para um nó atributo
#Variável "atribbute" armazena o valor da saída ou um atributo (o índice do atributo)
#Variável "branches" representa o valor da média dos valores de um atributo, que divide um conjunto em dois
#Variável "nextNodes[]" armazena os nós adjacentes. Usando a média, existem apenas 2 nós adjacentes.
class Node:
    
    def __init__(self, mode, atribbute):
        self.mode = mode
        self.atribbute = atribbute
        self.branches = -1
        self.nextNodes = []
        

#Algoritmo ID3
#Constrói uma árvore de decisão, usando a heurística de escolher o atributo com maior
#maior ganho de informação        
def ID3(examples, validAtr):

    targets = {""}
    for i in examples:
        targets.add(i[-1])

    target = []
    for x in targets:
        target.append(x)

    del target[0]
    
    countOutput = 0
    commonOutput = 0
    for i in range(len(target)):
        x = examples.count(target[i])
        if x > countOutput:
            x = countOutput[i]
            commonOutput = i
            
    #print("targets: ", target, "\n")
    
    if len(target) < 2:
        n = Node(0, target[-1])
        
    elif validAtr.count(1) == 0:
        n = Node(0, target[commonOutput])
        
    else:
        #Choose best Atribbute
        bestAtr = -1
        bestIGL = -1
        for i in range(len(validAtr)):
            if validAtr[i] == 1:
                a = InfoGlobal(examples)
                b = Remainder(examples, i)
                c = a-b

                if c > bestIGL:
                    bestIGL = c
                    bestAtr = i                

        n = Node(1, bestAtr)
        validAtr1 = validAtr.copy()
        validAtr2 = validAtr.copy()

        validAtr1[bestAtr] = 0
        validAtr2[bestAtr] = 0

        print("best atr: ", bestAtr,"\n")
        #print(validAtr1)
        #print(validAtr2)

        #Every possible value of A
        #Divide all values comparing to the mean
        
        meanCount = 0
        for i in range(len(examples)):
            meanCount += examples[i][bestAtr]

        #Calculate the mean value
        meanVal = meanCount/(len(examples))

        #print("mean id3: ", meanVal, "\n")
        
        newExamples1 = []
        newExamples2 = []

        n.branches = meanVal
        
        n.nextNodes.append(Node(0, commonOutput))
        n.nextNodes.append(Node(0, commonOutput))
        
        for j in range(len(examples)):
            if examples[j][bestAtr] < meanVal:
                newExamples1.append(examples[j])
            else:
                newExamples2.append(examples[j])

        if len(newExamples1) >= 0:
            newNode1 = ID3(newExamples1, validAtr1)
            n.nextNodes[0] = newNode1

        if len(newExamples2) >= 0:
            newNode2 = ID3(newExamples2, validAtr2)
            n.nextNodes[1] = newNode2

        #print(n.atribbute)
        #print(n.nextNodes[0].atribbute, " and ", n.nextNodes[1].atribbute)

        if n.nextNodes[0].mode == n.nextNodes[1].mode and n.nextNodes[0].atribbute == n.nextNodes[1].atribbute and n.nextNodes[0].mode == 0: 
            n.mode = n.nextNodes[0].mode
            n.atribbute = n.nextNodes[0].atribbute

    return n

#Função para validar a árvore de decisão
#A função recebe o conjunto de testes e a árvore de decisão.
#Cada exemplo de teste é avaliado usando os nós da árvore e comparado com o valor de saída alvo.
#Ao final do teste, a precisão dos resultados é apresentada
def Validate(test, node):
    count = 0
    for i in range(len(test)):
        print("teste ", i)
        s = node
        while s.mode != 0:
            if s.mode == 1:
                if test[i][s.atribbute] < s.branches:
                    s = s.nextNodes[0]
                else:
                    s = s.nextNodes[1]

        print(s.atribbute)
        if s.atribbute == test[i][-1]:
            print("---------right")
            count += 1
        else:
            print("---------wrong")
    print("precision: ", count/len(test))

#Exibir a árvore de decisão encontrada pelo algoritmo ID3, usando uma busca BFS
#para visitar os nós
def ShowTree(s, atrNames):

    queue =[s]
    print("\nfinal tree\n")
    while len(queue) > 0:
        n = queue[0]
        del queue[0]
        #print("queue length: ", len(queue))
        print("n = ", n.atribbute, " = ", atrNames[n.atribbute])
        print("branch(mean) = ", n.branches)
        print("nodes adj = ", len(n.nextNodes))

            
        for i in range(len(n.nextNodes)):
                
            #print("node adj: ", n.nextNodes[i].atribbute)
                
            if n.nextNodes[i].mode != 0:
                queue.append(n.nextNodes[i])
                print("node (", n.nextNodes[i].atribbute,") adj: ", atrNames[n.nextNodes[i].atribbute])
            else:
                print("node adj: ", n.nextNodes[i].atribbute)
        print()

#Instruções para leitura de um arquivo de dados para treino e outro para testes
f=open("iris3.data", "r")
g=open("irisTest.data", "r")


#Função principal para adaptar o programa para os dados do "Iris Data Set"
if f.mode == 'r':
        l = InitExamples(f, 130)

        numAtr = len(l[0]) - 1

        validAtr = []
        for x in range(numAtr):
            validAtr.append(1)


        atrNames = ["Sepal Length", "Sepal Width", "Petal Length", "Petal Width",]

        s = ID3(l, validAtr)
        
        ShowTree(s, atrNames)

        test = InitExamples(g, 20)
        Validate(test, s)
