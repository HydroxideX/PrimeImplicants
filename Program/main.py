def calculate_prime_implicants(numberofVariables, mainTerms, dontCare):
    allCalculated = False
    primeImplicants = []
    reducedElements = makegroups(numberofVariables, mainTerms, dontCare)
    while not allCalculated:
        reducedElements = removeEmptySets(reducedElements)
        primeImplicants, reducedElements, allCalculated = addPrimeImplicants(primeImplicants, reducedElements, allCalculated)
    if(len(reducedElements)==1):
        for z in reducedElements[0]:
            primeImplicants.append(z)
    primeImplicants = destroyRepetition(primeImplicants)
    primeImplicants = changeRepresentation(primeImplicants, numberOfVariables)
    primeImplicants = rowAndColumnDominance(primeImplicants, dontCare, numberOfVariables)
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


def removeEmptySets(reducedElements):
    for x in reducedElements:
        if len(x) == 0:
            reducedElements.remove(x)
    return reducedElements


def addPrimeImplicants(primeImplicants, reducedElements, allCalculated):
    if len(reducedElements) == 1 or len(reducedElements) == 0:
        allCalculated = True
        return primeImplicants, reducedElements, allCalculated
    bitMask = bitMask3d(reducedElements)
    primeImplicants, reducedElements = checkForPrimeImplicants(primeImplicants, reducedElements,bitMask)
    return primeImplicants, reducedElements, allCalculated


def bitMask3d(reducedElements):
    bitMask = []
    i = 0;j = 0;k = 0
    bitMask = [[False for j in range(len(reducedElements[i]))]for i in range(len(reducedElements))]
    for i in range(len(reducedElements)):
        for j in range(len(reducedElements[i])):
                bitMask[i][j] = False
    return bitMask


def checkForPrimeImplicants(primeImplicants, reducedElements,bitMask):
    temprow = []
    temp = []
    for i in range(len(reducedElements)-1):
        for j in range(len(reducedElements[i])):
            temprow, primeImplicants = addIfCouldBeMinimized(temprow, reducedElements[i][j], reducedElements[i + 1], primeImplicants,bitMask, i+1)
        temp.append(temprow[:])
        temprow.clear()
    for i in range(len(bitMask)):
        for j in range(len(bitMask[i])):
            if bitMask[i][j] == False:
                primeImplicants.append(reducedElements[i][j])
    return primeImplicants, temp


def addIfCouldBeMinimized(temp, firstNumber, secondNumberArray, primeImplicants, bitMask, index):
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
                        bitMask[index][k] = True
                        firstNumber.append(secondNumberArray[k][0]-firstNumber[0])
                        temp.append(firstNumber[:])
                        firstNumber.pop()
                        changedELement = True
                if len(secondNumberArray[k])==1:
                    bitMask[index][k] = True
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
        binaryArray.append(changeToBinary(primeImplicants[i][0], numberOfVariables))
        binaryArray[i] = swapWithX(primeImplicants[i], binaryArray[i])
    return binaryArray

def changeToBinary(number, numberOfVariables):
    string = ''
    if number == 0:
        return '0'*numberOfVariables
    while number != 1:
        string += str(number%2)
        number //= 2
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


def rowAndColumnDominance(primeImplicants, dontCare,numberOfVariables):
    primeImplicants = removelessers1(primeImplicants)
    primeImplicants = removelessers2(primeImplicants, dontCare,numberOfVariables)
    return primeImplicants

def removelessers1(primeImplicants):
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


def removelessers2(primeImplicants, dontCare, numberOfVariables):
    for i in range(len(dontCare)):
        dontCare[i] = changeToBinary(dontCare[i], numberOfVariables)
    expandedPrimeImplicants = expand(primeImplicants)
    primeImplicants = removeDuplicates(primeImplicants,expandedPrimeImplicants,dontCare)
    return primeImplicants


def expand(primeImplicants):
    if len(primeImplicants) == 0:
        return primeImplicants
    expanded = False
    expandedTerms = []
    i = 0
    while not expanded:
        term = []
        termNotExpanded = True
        term.append(primeImplicants[i])
        j = 0
        while termNotExpanded:
            if 'x' in term[j]:
                Implicant = term[j]
                termNotExpanded = True
                term.append(Implicant.replace('x', '0', 1))
                term.append(Implicant.replace('x', '1', 1))
                term.remove(Implicant)
            else:
                j += 1
            if j == len(term):
                break
        expandedTerms.append(term)
        i += 1
        if i == len(primeImplicants):
            expanded = True
    return expandedTerms



def removeDuplicates(primeImplicants, expandedPrimeImplicants,dontCare):
    binaryMask = defineMask(expandedPrimeImplicants)
    checkForNumber(binaryMask, expandedPrimeImplicants, dontCare,primeImplicants)
    getEssentials(expandedPrimeImplicants, binaryMask, primeImplicants)
    binaryMask = defineMask(expandedPrimeImplicants)
    notDone = True
    while notDone:
        binaryMask = defineMask(expandedPrimeImplicants)
        checkForNumber(binaryMask, expandedPrimeImplicants, dontCare, primeImplicants)
        notDone = checkIfDone(binaryMask)
        primeImplicants, expandedPrimeImplicants = remove(binaryMask, primeImplicants,expandedPrimeImplicants)
    return primeImplicants


def defineMask(expandedPrimeImplicants):
    binaryMask = []
    i = 0;j = 0
    binaryMask = [[False for j in range(len(expandedPrimeImplicants[i]))] for i in range(len(expandedPrimeImplicants))]
    for i in range(len(expandedPrimeImplicants)):
        for j in range(len(expandedPrimeImplicants[i])):
            binaryMask[i][j] = False
    return binaryMask


def checkForNumber(binaryMask, expandedPrimeImplicants, dontCare,primeImplicants):
    for i in range(len(expandedPrimeImplicants)):
        for j in range(len(expandedPrimeImplicants[i])):
            if expandedPrimeImplicants[i][j] in dontCare:
                binaryMask[i][j] = True
                continue
            binaryMask = checkEachNoForRepetition(binaryMask, expandedPrimeImplicants, i, j)



def checkEachNoForRepetition(binaryMask,expandedPrimeImplicants,i,j):
    for k in range(len(expandedPrimeImplicants)):
        for t in range(len(expandedPrimeImplicants[k])):
            if k == i and t == j:
                continue
            elif expandedPrimeImplicants[i][j] == expandedPrimeImplicants[k][t] \
                    and expandedPrimeImplicants[i][j] not in dontCare:
                binaryMask[i][j] = True
                break
        if binaryMask[i][j] == True:
            break
    return binaryMask

def getEssentials(expandedPrimeImplicants,binaryMask,primeImplicants):
    Essentials = set([])
    for i in range(len(expandedPrimeImplicants)):
        for j in range(len(expandedPrimeImplicants[i])):
            if binaryMask[i][j] == False:
                Essentials.add(i)
    print("Essentials Are:", end=' ')
    for x in Essentials:
        print(primeImplicants[x], end=' ')
    print()


def checkIfDone(binaryMask):
    notDone = False
    for i in range(len(binaryMask)):
        for j in range(len(binaryMask[i])):
            if binaryMask[i][j] == False:
                break
            if j == len(binaryMask[i])-1:
                notDone = True
    return notDone


def remove(binaryMask, primeImplicants,expandedPrimeImplicants):
    for i in range(len(binaryMask)):
        for j in range(len(binaryMask[i])):
            if binaryMask[i][j] == False:
                break
            if j == (len(binaryMask[i])-1):
                primeImplicants.remove(primeImplicants[i])
                expandedPrimeImplicants.remove(expandedPrimeImplicants[i])
                return primeImplicants,expandedPrimeImplicants
    return primeImplicants,expandedPrimeImplicants

def getInput(numberOfVariables):
    dontCare = []
    minTerms = []
    minTermsFalse = True
    dontCareFalse = True
    while minTermsFalse:
        print("Enter MinTerms:")
        z = input()
        i = 0
        Continue = False
        for x in z:
            if not x.isdigit() and not x.isspace():
                Continue = True
                continue
        if Continue:
            continue
        while i < len(z):
            if not z[i].isdigit():
                break
            k = i
            while i < len(z) and z[i].isdigit():
                i += 1
            minTerms.append(int(z[k:i]))
            i += 1
            if i >= len(z):
                minTermsFalse = False
    while dontCareFalse:
        print("Enter Dont Care Terms:(-1 if there are none)")
        z = input()
        if len(z) > 1:
            if z[0] == '-' and z[1] == '1':
                dontCare.append(-1)
                break
        i = 0
        Continue = False
        for x in z:
            if not x.isdigit() and not x.isspace():
                Continue = True
                continue
        if Continue:
            continue
        while i < len(z):
            if not z[i].isdigit():
                break
            k = i
            while i < len(z) and z[i].isdigit():
                i += 1
            dontCare.append(int(z[k:i]))
            i += 1
            if i >= len(z):
                dontCareFalse = False
    return minTerms, dontCare


start = True
while start:
    print("Enter Number Of Variables:")
    numberOfVariables = input()
    while not numberOfVariables.isdigit() or int(numberOfVariables) == 0:
        print("Enter Number Of Variables:(ex:1,2,..)")
        numberOfVariables = input()
    numberOfVariables = int(numberOfVariables)
    notCorrect = True
    minTerms = []
    dontCare = []
    while notCorrect:
        notCorrect = False
        minTerms, dontCare = getInput(numberOfVariables)
        for x in minTerms:
            if x < 0 or x >= 2**numberOfVariables:
                notCorrect = True
        for x in dontCare:
            if x < 0 or x >= 2**numberOfVariables:
                notCorrect = True
        if dontCare[0] == -1:
            notCorrect = False

    if dontCare[0] == -1:
        dontCare.clear()
    primeImplicants = calculate_prime_implicants(numberOfVariables, minTerms, dontCare)
    print("Prime Implicants Minimized Are:", end=' ')
    for x in primeImplicants:
        print(x, end=' ')
    print()
    z = 'a'
    while True:
        print()
        print("Do you want to Calculate Another Prime Implicant:[Y/N]")
        z = input()
        if z[0] == 'N':
            start = False
            print("program Ended Successfully :)")
            break
        if z[0] == 'Y':
            break
