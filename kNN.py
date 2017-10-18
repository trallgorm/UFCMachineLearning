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

def testAllStats():
    statsAndAccuracy =[]

    for size in range(0, len(ScraperDAO.getNamesOfStats()) + 1):
        for statNamesSubset in itertools.combinations(ScraperDAO.getNamesOfStats(), size):
            totalaccuracy=0
            for i in range(10):
                totalaccuracy += getAccuracyOfModel(statNamesSubset)
            statsAndAccuracy.append((statNamesSubset,totalaccuracy/10))
            print(str(statNamesSubset) + " : " + str(totalaccuracy/10))

    print("Done")
    return(sorted(statsAndAccuracy, key=lambda tup: tup[1], reverse=True))

print(testAllStats())








