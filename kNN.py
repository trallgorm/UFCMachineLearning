import ScraperDAO
import random
import math
import itertools

#Set k to the square root of the amount of samples, a good metric
k = int(math.sqrt(len(ScraperDAO.fighterDifferencesAndResultsList)))

#Fills the training list and the test list with the amount in the training list specified by split percentage
def splitDataset(splitPercentage):
    trainingInstancesList = []
    testInstancesList = []
    data = ScraperDAO.fighterDifferencesAndResultsList
    for i in range(len(data)-1):
        if random.random() < splitPercentage:
            trainingInstancesList.append(data[i])
        else:
            testInstancesList.append(data[i])

    return({"TestList" : testInstancesList, "TrainingList": trainingInstancesList})

#Gets the euclidean distance between two matches
#Euclidian distance is the root of the sum of the squared differences between the dimensions
def getEuclideanDistance(a, b , stats):
    distance = 0
    for stat in stats:
        if stat!="Result":
            distance += pow((a[stat] - b[stat]), 2)
    return math.sqrt(distance)

#Guesses whether the fighter will win or lose in a fight
#The input is a set of differences between the fighters stats, eg -10 if the opponent is 10 cm taller
def makePrediction(newFight, statsToJudgeBy, trainingInstancesList):
    winDistancesList=[]
    loseDistancesList=[]

    #Gets the distances between all the matches and places them in the win list or the lose list
    for testInstance in trainingInstancesList:
        distance = getEuclideanDistance(testInstance, newFight, statsToJudgeBy)

        #If you ain't first you're last
        if testInstance["Result"]=="Win":
            winDistancesList.append(distance)
        else:
            loseDistancesList.append(distance)

    winDistancesList.sort()
    loseDistancesList.sort()

    winIndex=0
    loseIndex=0

    #Indeces can be thought of as votes. Eg the index for the winlist only moves if the highest current winning distance is lower than the current losing distance
    for x in range(k):
        if winDistancesList[winIndex]<loseDistancesList[loseIndex]:
            winIndex+=1
        else:
            loseIndex+=1

    if(winIndex>loseIndex):
        return("Win")
    else:
        return("Loss")

#Runs the model and returns its accuracy
def getAccuracyOfModel(statsToJudgeBy):
    datalists = splitDataset(0.66)
    correctGuesses = 0
    for fight in datalists["TestList"]:
        if fight["Result"] == makePrediction(fight, statsToJudgeBy, datalists["TrainingList"]):
            correctGuesses+=1

    return((correctGuesses/len(datalists["TestList"]))*100)

def writeResultsToFile(size, statsAndAccuracy):
    file = open('level' + str(size) + '.txt', 'w+')
    for item in sorted(statsAndAccuracy, key=lambda tup: tup[1], reverse=True):
        file.write(str(item[0]) + " : " + str(item[1]) + '\n')
    file.close()

#Attempts to run the model for a number of stats to see which ones have the most predictive power
def testAllStats():
    statsAndAccuracy =[]

    #Runs for a combination of all the stats, will finish in only around 173 trillion years
    for size in range(1, len(ScraperDAO.getNamesOfStats()) + 1):
        batchSize = 0
        for statNamesSubset in itertools.combinations(ScraperDAO.getNamesOfStats(), size):
            batchSize+=1
            totalaccuracy=0

            #Runs the model 3 times to average out the accuracy
            for i in range(3):
                totalaccuracy += getAccuracyOfModel(statNamesSubset)
            statsAndAccuracy.append((statNamesSubset,totalaccuracy/3))
            print(str(statNamesSubset) + " : " + str(totalaccuracy/3))

            #Writes the results to a file if there are over 100 unwritten results just so theres a result to look at if the level doesn't finish
            if(batchSize>100):
                batchSize=0
                writeResultsToFile(size,statsAndAccuracy)

        print("One level done")
        writeResultsToFile(size, statsAndAccuracy)

    print("Done")
    return(sorted(statsAndAccuracy, key=lambda tup: tup[1], reverse=True))

print(testAllStats())








