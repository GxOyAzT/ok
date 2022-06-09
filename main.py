import random
import time

def readFromFile(fileName):
    matrix = []
    inputTable = []
    with open(fileName) as f:
        size = int(next(f))
        for line in f:
            inputTable.append([int(x) for x in line.split()])

    for i in range(size):
        innerTable = []
        for j in range(size):
            innerTable.append(0)
        matrix.append(innerTable)

    for inputTableLine in inputTable:
        matrix[inputTableLine[0] - 1][inputTableLine[1] - 1] = 1
        matrix[inputTableLine[1] - 1][inputTableLine[0] - 1] = 1

    return matrix

def generator(size, saturation):
    matrix = []
    howManyEdges = int((size * size - size) / 2)

    for i in range(size):
        innerTable = []
        for j in range(size):
            innerTable.append(0)
        matrix.append(innerTable)

    matrix[0][size - 1] = 1
    matrix[size - 1][0] = 1

    for i in range(size - 1):
        matrix[i][i+1] = 1
        matrix[i][i - 1] = 1

    matrix[size - 1][size - 2] = 1

    counter = 0
    while(counter <= howManyEdges * saturation / 100 - size):
        a = random.randint(0, size - 1)
        b = random.randint(0, size - 1)
        if a == b:
            continue

        if matrix[a][b] == 1:
            continue

        matrix[a][b] = 1
        matrix[b][a] = 1

        counter += 1

    return matrix

def writeToFile(fileName, matrix):
    size = len(matrix)
    with open(fileName, 'w') as f:
        f.write(str(size) + '\n')
        for i in range(size):
            for j in range(i, size):
                if (matrix[i][j] == 1):
                    f.write(str(i + 1) + " " + str(j + 1) + '\n')

def greedySearch(matrix):
    colorTable = []
    size = len(matrix)
    for i in range(size):
        colorTable.append(0)

    for i in range(size):
        takenColors = []
        for j in range(size):
            if matrix[i][j] == 1:
                takenColors.append(colorTable[j])
        takenColors.sort()
        # print(takenColors)
        for j in range(1, size):
            if j not in takenColors:
                colorTable[i] = j
                break

    print("Greedy: colors:", max(colorTable), " for: ", colorTable)
    return max(colorTable)

class Specimen:
    def __init__(self, coloredVerticles):
        self.coloredVerticles = coloredVerticles
        self.errors = 0

    def clone(self):
        return Specimen(self.coloredVerticles, self.errors)

def generatePopulation(populationSize, numberOfColors, verticles):
    ret = []
    for populationIndex in range(populationSize):
        population = []

        for verticleIndex in range(verticles):
            population.append(random.randrange(1, numberOfColors))

        ret.append(Specimen(population))

    return ret

def evaluateSpecimen(specimen, graph):
    specimen.errors = 0
    for i in range(len(graph)):
        for j in range(i, len(graph)):
            if graph[i][j] == 1 and specimen.coloredVerticles[i] == specimen.coloredVerticles[j]:
                specimen.errors += 1
    return specimen

def evaluatePopulation(population, graph):
    for s in population:
        s = evaluateSpecimen(s, graph)

    return population

def selection(population):
    population.sort(key = lambda x: x.errors, reverse = True)

    rankSum = 0
    curRank = 0

    specsRank = []
    for s in population:
        specsRank.append([curRank, s])
        rankSum += curRank
        curRank += 1

    thresholdList = []
    treshold = 0.0
    for s in specsRank:
        treshold = treshold + (s[0] / rankSum)
        thresholdList.append([treshold, s[1]])

    newPopulation = []

    for i in range(len(population)):
        selection = random.uniform(0, 1)
        satisfyCond = []
        for j in thresholdList:
            if j[0] >= selection:
                satisfyCond.append(j[1])

        newPopulation.append(satisfyCond[0])

    return newPopulation

def crossover(population, crossoverProb):
    newPopulation = []

    for i in range(len(population)):
        randIndex = random.randrange(i, len(population))
        tmp = population[i]
        population[i] = population[randIndex]
        population[randIndex] = tmp

    helperPopulation = []

    for p in population:
        helperPopulation.append(p)

    while len(helperPopulation) > 1:
        spec1 = helperPopulation.pop()
        spec2 = helperPopulation.pop()

        if (random.uniform(0, 1) < crossoverProb):
            locus = random.randint(1, len(spec1.coloredVerticles))
            newSpec1 = spec1.coloredVerticles[:locus] + spec2.coloredVerticles[locus:]
            newSpec2 = spec1.coloredVerticles[locus:] + spec2.coloredVerticles[:locus]
            newPopulation.append(Specimen(newSpec1))
            newPopulation.append(Specimen(newSpec2))
        else:
            newPopulation.append(spec1)
            newPopulation.append(spec2)

    while len(helperPopulation) > 0:
        newPopulation.append(helperPopulation.pop())

    return newPopulation

def mutation(population, mutationProb, numberOfColors):
    for s in population:
        for i in range(len(s.coloredVerticles)):
            if random.uniform(0, 1) < mutationProb:
                s.coloredVerticles[i] = random.randrange(1, numberOfColors)

    return population

ans = []
def checkIfSolutionExists(population, iteration, maxColors):
    for p in population:
        if p.errors == 0:
            ans.append([maxColors, iteration, p.coloredVerticles])
            print("Found answear for max ", max(p.coloredVerticles), "colors: ",  p.coloredVerticles, " !")
            return True

    return False

def selectBestIndex(population):
    bestIndex = 0
    for i in len(population):
        if population[bestIndex].errors > population[i].errors:
            bestIndex = i

    return bestIndex

def printPopulation(population):
    for s in population:
        print(s.errors, s.coloredVerticles)

def printAns(ans):
    print("----- Answears -----")
    for a in ans:
        print("Looked for max: ", a[0], " in iterations count: ", a[1], " with answear: ", a[2])

def metaheuristicSearch(matrix):
    ans = []
    iteration = []
    maxGreedy = greedySearch(matrix)
    print("START FROM -> " + str(maxGreedy))
    populationSize = 500 # 150
    population = generatePopulation(populationSize, maxGreedy - 1, len(matrix))
    population = evaluatePopulation(population, matrix)
    iteration.append([maxGreedy - 1, 0])
    # 300 0,5 0,0009
    # 0.8 0.005
    startTime = time.time()
    try:
        for i in range(1000000):
            iteration[-1][1] += 1
            # print("STEP ", i, "ERRORS", population[0].errors, "COLORS", population[0].coloredVerticles)
            population = selection(population)
            population = crossover(population, 0.3)
            population = mutation(population, 0.0005, maxGreedy)
            population = evaluatePopulation(population, matrix)

            errors = []
            for p in population:
                errors.append(p.errors)

            print(str(i) + ":   " + str(min(errors)) + " (min)   " + str(
                max(errors)) + "(max)  , looking for max: " + str(maxGreedy - 1))

            if (checkIfSolutionExists(population, iteration[-1][1], maxGreedy - 1)):
                maxGreedy -= 1
                iteration.append([maxGreedy, 0])
                population = generatePopulation(populationSize, maxGreedy, len(matrix))

            # if time.time() - startTime > 60*3:
            #     print("End of time!")
            #     raise Exception("End of time!")
    except:
        printAns(ans)

def main():
    matrix = readFromFile('gc500.txt')
    metaheuristicSearch(matrix)

def analize():
    for j in [20,30,40,50,60,70,80,90]:
        print("----------------------------------------------------------------  number of verticles " + str(j) + "  ----------------------------------------------------------------")
        for i in range(5):
            print(" -----------------------  " + str(i) + "  -----------------------")
            matrix = generator(j, 50)
            metaheuristicSearch(matrix)

def greedyVSmetaheurGenerator():

    writeToFile("greedyVSmetaheur" + str(51) + ".txt")

def greedyVSmetaheur():
    readFromFile('greedyVSmetaheur51.txt')
    main()

main()