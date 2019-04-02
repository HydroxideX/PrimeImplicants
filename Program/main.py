def calculate_prime_implicants(numberofVariables, mainTerms, dontCare):
    allCalculated = False
    primeImplicants = []
    reducedElements = makegroups(numberofVariables, mainTerms, dontCare)
    while not allCalculated:
        primeImplicants, reducedElements, allCalculated = addPrimeImplicants( primeImplicants, reducedElements, allCalculated)
    primeImplicants = destroyRepetition(primeImplicants)
    primeImplicants = changeRepresentation(primeImplicants, numberOfVariables)
    primeImplicants = rowAndColumnDominance(primeImplicants)
    return primeImplicants


def makegroups(numberofVariables, mainTerms, dontCare):
    reducedElements = [[[-1] for i in range(len(mainTerms)+len(dontCare))]for j in range(numberofVariables+1)]
    reducedElements = putELementsIntoGroups(mainTerms, reducedElements)
    reducedElements = putELementsIntoGroups(dontCare, reducedElements)
    reducedElements = destroyNullElements(reducedElements)
    return reducedElements


def putELementsIntoGroups(arrayToDivide, reducedElements):
    for i in arrayToDivide:
        bits = countBits(i, 0)
        for ct in range(len(reducedElements[bits])):
            if reducedElements[bits][ct][0] == -1:
                reducedElements[bits][ct][0] = i
                break
    return reducedElements


def countBits(minterm, bits):
    if not minterm:
        return bits
    bits += minterm % 2 + countBits(minterm // 2, bits)
    return bits


def destroyNullElements(reducedElements):
    for i in reducedElements[:]:
        for j in i[:]:
            if j[0] == -1:
                i.remove(j)
    for i in reducedElements[:]:
        if not len(i):
            reducedElements.remove(i)
    for i in range(len(reducedElements)):
        reducedElements[i] = sorted(reducedElements[i])
    return reducedElements


def addPrimeImplicants(primeImplicants, reducedElements, allCalculated):
    if len(reducedElements) == 1:
        allCalculated = True
        return primeImplicants, reducedElements, allCalculated
    primeImplicants, reducedElements = checkForPrimeImplicants(primeImplicants, reducedElements)
    return primeImplicants, reducedElements, allCalculated


def checkForPrimeImplicants(primeImplicants, reducedElements):
    temprow = []
    temp = []
    for i in range(len(reducedElements)-1):
        for j in range(len(reducedElements[i])):
            temprow, primeImplicants = addIfCouldBeMinimized(temprow, reducedElements[i][j], reducedElements[i + 1], primeImplicants)
        temp.append(temprow[:])
        temprow.clear()
    return primeImplicants, temp


def addIfCouldBeMinimized(temp, firstNumber, secondNumberArray, primeImplicants):
    changedELement = False
    for k in range(len(secondNumberArray)):
        if secondNumberArray[k][0]-firstNumber[0] > 0 and isPowerOfTwo((secondNumberArray[k][0]-firstNumber[0])):
            if len(secondNumberArray[k]) != len(firstNumber):
                continue
            else:
                firstNumber[1:] = sorted(firstNumber[1:])
                secondNumberArray[k][1:] = sorted(secondNumberArray[k][1:])
                for i in range(1, len(secondNumberArray[k])):
                    if secondNumberArray[k][i] != firstNumber[i]:
                        break
                    if i == len(secondNumberArray[k])-1:
                        firstNumber.append(secondNumberArray[k][0]-firstNumber[0])
                        temp.append(firstNumber[:])
                        firstNumber.pop()
                        changedELement = True
                if len(secondNumberArray[k])==1:
                    firstNumber.append(secondNumberArray[k][0] - firstNumber[0])
                    temp.append(firstNumber[:])
                    firstNumber.pop()
                    changedELement = True
    if not changedELement:
        primeImplicants.append(firstNumber)
    return temp, primeImplicants


def destroyRepetition(primeImplicants):
    for i in range(len(primeImplicants)):
        primeImplicants[i][1:] = sorted(primeImplicants[i][1:])
    for i in primeImplicants[:]:
        ct = 0
        for j in primeImplicants[:]:
            if i == j and ct:
                primeImplicants.remove(j)
            elif ct == 0 and i == j:
                ct = 1
    return primeImplicants

def isPowerOfTwo(number):
    x = 1
    while x<number:
        x = x*2
    if x>number:
        return False
    else:
        return True

def changeRepresentation(primeImplicants,numberOfVariables):
    binaryArray = []
    for i in range(len(primeImplicants)):
        binaryArray.append(changeToBinary(primeImplicants[i][0],numberOfVariables))
        binaryArray[i] = swapWithX(primeImplicants[i], binaryArray[i])
    return binaryArray

def changeToBinary(number,numberOfVariables):
    string = ''
    while number != 1:
        string += str(number%2)
        number //=2
    string += str(1)
    string = ''.join(reversed(string))
    while len(string)<numberOfVariables:
        string = '0' + string
    return string

def swapWithX(dontCareBits, string):
    for i in range(1, len(dontCareBits)):
        ct = 0
        while dontCareBits[i] != 0:
            dontCareBits[i] = dontCareBits[i]//2
            ct += 1
        string = string[0:len(string)-ct]+'x'+string[len(string)-ct+1:]
    return string


def rowAndColumnDominance(primeImplicants):
    for i in primeImplicants[:]:
        temp = []
        temp.clear()
        for k in range(len(i)):
            if i[k] == 'x':
                temp.append(k)
        for j in primeImplicants[:]:
            if i == j:
                continue
            for k in range(len(i)):
                if k in temp:
                    pass
                elif i[k] != j[k]:
                    break
                if k == len(i) - 1:
                    primeImplicants.remove(j)
    return primeImplicants


numberOfVariables = int(input())
mainTerms = list(map(int, input().split()))
dontCare = list(map(int, input().split()))
primeImplicants = calculate_prime_implicants(numberOfVariables, mainTerms, dontCare)
print(primeImplicants)
