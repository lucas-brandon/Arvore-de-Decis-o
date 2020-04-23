import numpy


def InitExamples(f, numExamples):
    l = f.readlines()
    a = []

    
    
    for x in l:
        newLine = []
        rChar = ""
        for y in x:
            
            #print("char " + y + "\n")
            if y == ',':
                aux1 = float(rChar)
                newLine.append(aux1)
                rChar = ""

            elif y == x[-1]:
                newLine.append(rChar)
                rChar = ""
                #print("a")

            else:
                rChar += y

        if len(a) < numExamples:
            a.append(newLine)

    print("tam f: ", len(a))
    return a

def Remainder(examples, atribbute):

    remainder = 0

    atVal = {0.0}
    out = {""}
    atValues = []
    output = []

    meanCount = 0    
    for x in range(len(examples)):
        #print(x)
        atVal.add(examples[x][atribbute])
        out.add(examples[x][-1])
        meanCount += examples[x][atribbute]

    
    meanVal = meanCount/(len(examples))

    
    for x in atVal:
        atValues.append(x)
    for x in out:
        output.append(x)

    del atValues[0]
    del output[0]

    #Every possible value of A
    #Divide all values comparing to the mean 

    
    #print("atValues: ", atValues)
    #print("output: ", output)

    #i = 2 vezes (abaixo/acima da média)
    #for i in range(len(atValues)-1):

    exValuesLess = []
    exValuesMore = []
    #print("var: ", atValues[i])
    #filtrar o vetor original para um vetor
    #apenas com o valor da var
    for j in range(len(examples)):

        #print(atValues[i], " = ", examples[j][atribbute])
        if examples[j][atribbute] < meanVal:
        
            aux = []
            aux.append(examples[j][atribbute])
            aux.append(examples[j][-1])
            exValuesLess.append(aux)
        else:            
            aux = []
            aux.append(examples[j][atribbute])
            aux.append(examples[j][-1])
            exValuesMore.append(aux)

    outProbLess = []
    outProbMore = []

    print("example values less: ", len(exValuesLess))
    print("example values less: ", len(exValuesMore))
    
    #print("exValues: ", exValues)
    countTL = 0
    countTM = 0
    for j in range(len(output)):
        countL = 0
        countM = 0
        for k in range(len(exValuesLess)):
            if output[j] == exValuesLess[k][-1]:
                countL+=1

        outProbLess.append(countL)
        countTL += countL

        for k in range(len(exValuesMore)):
            if output[j] == exValuesMore[k][-1]:
                countM+=1

        outProbMore.append(countM)
        countTM += countM
    
    outProbLess[:] = [x / countTL for x in outProbLess]
    outProbMore[:] = [x / countTM for x in outProbMore]

    
    #print("ProbM = ", len(outProbMore))
    #print("ProbL = ", len(outProbLess))
    
            
    #print("prob: ", outProb)
    #print("total: ", countT)

    #Calcular I()

    r1 = 0
    c = 0
    for j in outProbLess:
        if j != 0:
            c += (-1)*j*numpy.log2(j)

    r1 = (countTL/(len(examples)-1))*c

   

    #Calcular I()

    r2 = 0
    c = 0
    for j in outProbMore:
        if j != 0:
            c += (-1)*j*numpy.log2(j)

    r2 = (countTM/(len(examples)-1))*c

   
    
    remainder = r1 + r2

    #print("valor A: ", r)

    #print("remainder A = ", remainder)
    return remainder

        




def InfoGlobal(examples):

    #Mapear as possibilidades de saída

    targets = {""}

    for i in examples:
        targets.add(i[-1])

    #print(targets)

    target = []
    for x in targets:
        target.append(x)

    probTarget = []

    
    
    for x in target:
        count = 0
        for y in examples:
            #print(len(y))
            if x == y[-1]:
                count+=1

        probTarget.append(count)

    #print(probTarget)

    del probTarget[0]

    probTarget[:] = [x / len(examples) for x in probTarget]
    

    #print(probTarget)    

    #Calcular Informação

    ig1 = 0
    for x in probTarget:
        k = numpy.log2(x)
        ig1+=x*k*(-1)

    #print(ig1)
    return ig1


class Node:
    
    def __init__(self, mode, atribbute):
        #self.root = root
        self.mode = mode
        self.atribbute = atribbute
        self.branches = -1
        self.nextNodes = []
        


def ID3(examples, validAtr):

    #Descobrir valor de saída mais comum

    targets = {""}

    for i in examples:
        targets.add(i[-1])
    print("len examples: ", len(examples))
    print("len targets: ", len(targets))

    target = []
    for x in targets:
        target.append(x)

    del target[0]
    
    countOutput = 0
    commonOutput = 0
    for i in range(len(target) - 1):
        x = examples.count(target[i])
        if x > countOutput:
            x = countOutput[i]
            commonOutput = i
            

    if len(target) < 2:
        print("node with only 1 target\n")
        print("target: ", len(target))
        n = Node(0, target[-1])
        
    elif validAtr.count(1) == 0:
        print("node with only 1 atr\n")
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

                print("global info: ", a, " remainder: ", b, " igl: ", c)

                if c > bestIGL:
                    bestIGL = c
                    bestAtr = i
                #print("Atb ", count2," = ", a, " - ", b, " = ", c)
                #count2+=1

        n = Node(1, bestAtr)
        validAtr[bestAtr] = 0
        validAtr2 = validAtr.copy()

        print("best atr: ", bestAtr,"\n")

        #Every possible value of A
        #Divide all values comparing to the mean
        atVal = {0.0}
        atValues = []

        
        meanCount = 0
        for i in range(len(examples)-1):
            #print(len(i))
            atVal.add(examples[i][bestAtr])
            meanCount += examples[i][bestAtr]

        #Calculate the mean value
        meanVal = meanCount/(len(examples))

        print("mean: ", meanVal, "\n")

        #print("atval: ", atVal)
        for i in atVal:
            atValues.append(i)


        #print("mean: ", meanVal)
        newExamples1 = []
        newExamples2 = []

        #branch < mean
        n.branches = meanVal
        
        n.nextNodes.append(Node(0, commonOutput))
        n.nextNodes.append(Node(0, commonOutput))
        
        for j in range(len(examples) - 1):
            if examples[j][bestAtr] < meanVal:
                newExamples1.append(examples[j])
            else:
                newExamples2.append(examples[j])

        #print("valid atr 1: ", validAtr)                
        #print("new examples less: ", len(newExamples1))
        #print("new examples more: ", len(newExamples2))
        print("less\n")
        if len(newExamples1) > 0:
            newNode1 = ID3(newExamples1, validAtr)
            n.nextNodes[0] = newNode1

        #print("valid atr 2: ", validAtr)                
        print("more\n")
        if len(newExamples2) > 0:
            newNode2 = ID3(newExamples2, validAtr2)
            n.nextNodes[1] = newNode2

        #print("n1 : ", newNode1)
        #print("n2 : ", newNode2)
        

        #for i in range(len(atValues) - 1):
            #n.branches.append(atValues[i])
            #n.nextNodes.append(Node(0, commonOutput))

            #for j in range(len(examples) - 1):
                #if examples[j][bestAtr] == atValues[i]:
                    #newExamples.append(examples[j])

            #newNode = ID3(newExamples, validAtr)
            #n.nextNodes[i] = newNode

    return n


def Validate(test, node):
    count = 0
    for i in range(len(test)):
        print("teste ", i)
        s = node
        while s.mode != 0:
            #print(s.atribbute)
            if s.mode == 1:
                if test[i][s.atribbute] < s.branches:
                    s = s.nextNodes[0]
                else:
                    s = s.nextNodes[1]
            else:
                if s.nextNodes[0] != 0:
                    print("res = ", s.nextNodes[0])
                else:
                    print("res = ", s.nextNodes[1])

        print(s.atribbute)
        if s.atribbute == test[i][-1]:
            print("---------right")
            count += 1
        else:
            print("---------wrong")
    print("precision: ", count/len(test))

#f=open("iris.data", "r")

f=open("iris3.data", "r")
g=open("irisTest.data", "r")


if f.mode == 'r':
        l = InitExamples(f, 130)

        numAtr = len(l[0]) - 1

        validAtr = []
        for x in range(numAtr):
            validAtr.append(1)

        count = 0
        count2 = 0

        atrNames = ["Sepal Length", "Sepal Width", "Petal Length", "Petal Width",]

        s = ID3(l, validAtr)

        #input()

        queue =[s]

        while len(queue) > 0:
            n = queue[0]
            del queue[0]
            #print("queue length: ", len(queue))
            print("n = ", n.atribbute, " = ", atrNames[n.atribbute])
            print("branches = ", n.branches)
            print("nodes adj = ", len(n.nextNodes))

            
            for i in range(len(n.nextNodes)):
                
                #print("node adj: ", n.nextNodes[i].atribbute)
                
                if n.nextNodes[i].mode != 0:
                    queue.append(n.nextNodes[i])
                    print("node adj: ", atrNames[n.nextNodes[i].atribbute])
                else:
                    print("node adj: ", n.nextNodes[i].atribbute)

        test = InitExamples(g, 20)
        Validate(test, s)                    
        print("\n")

        #while len(l) != 0:
        #while count2 < numAtr:

            #a = InfoGlobal(l)

            #b = Remainder(l, count2)

            #c = a-b
            #print("Atb ", count2," = ", a, " - ", b, " = ", c)
            #count2+=1

            

        
