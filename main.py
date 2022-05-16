import random
import select

size = 100
matrix = []

inputTable = []

def readFromFile(fileName):
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

def generator(size, saturation):
    howManyEdges = int((size * size - size) / 2)
    print(howManyEdges)

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

#WRITE TO FILE

# with open('data5.txt', 'w') as f:
#     f.write(str(size) + '\n')
#     for i in range(size):
#         for j in range(i, size):
#             if (matrix[i][j] == 1):
#                 f.write(str(i + 1) + " " + str(j + 1) + '\n')

#WRITE TO FILE END



#GREEDY ALGO
# for i in matrix:
#     print(i)

def greedySearch():
    colorTable = []
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

        # print(colorTable[i])

    return max(colorTable)

#GREEDY ALGO END

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
        for j in range(len(graph)):
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

    specs = []
    for p in population:
        specs.append([curRank, p])
        rankSum += curRank
        curRank += 1

    thresholdList = []
    treshold = 0.0
    for s in specs:
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
    for p in population:
        for i in range(len(p.coloredVerticles)):
            if random.uniform(0, 1) < mutationProb:
                p.coloredVerticles[i] = random.randrange(1, numberOfColors)

    return population

def checkIfSolutionExists(population):
    for p in population:
        if p.errors == 0:
            print(p.coloredVerticles)
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

def main():
    # readFromFile('miles250.txt')
    generator(100, 40)
    maxGreedy = greedySearch()
    print(maxGreedy)
    population = generatePopulation(150, maxGreedy - 1, len(matrix))
    population = evaluatePopulation(population, matrix)

    # 0.8 0.005
    for i in range(1000000):
        population = selection(population)
        population = crossover(population, 0.8)
        population = mutation(population, 0.008, maxGreedy)
        population = evaluatePopulation(population, matrix)
        population = selection(population)


        errors = []
        for p in population:
            errors.append(p.errors)

        print(str(i) + ": " + str(min(errors) // 2) + ", maxGreedy: " + str(maxGreedy))

        if (checkIfSolutionExists(population)):
            maxGreedy -= 1
            population = generatePopulation(80, maxGreedy - 1, len(matrix))

main()
