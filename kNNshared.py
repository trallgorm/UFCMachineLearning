import math
import random

#Fills the training list and the test list with the amount in the training list specified by split percentage
def splitDataset(splitPercentage, data):
    trainingInstancesList = []
    testInstancesList = []
    for i in range(len(data)-1):
        if random.random() < splitPercentage:
            trainingInstancesList.append(data[i])
        else:
            testInstancesList.append(data[i])

    return({"TestList" : testInstancesList, "TrainingList": trainingInstancesList})

#Reads the result file and returns a sorted array of tuple which contain the stat name array and the accuracy percentage
def readPreviousSession():
    allStats = []
    try:
        with open("top_stats.txt", "r") as topStatsFile:
            for line in topStatsFile:
                if line !='\n' or line!='':
                    lineArray=line.strip().split(',')
                    statArray=lineArray[1:]
                    if '' in statArray:
                        statArray.remove('')
                    accuracy = lineArray[0]
                    allStats.append((statArray,float(accuracy)))
        topStatsFile.close()
    except FileNotFoundError:
        allStats=[]
    return sorted(allStats, key=lambda tup: tup[1], reverse=True)

#Reads the top x stats
def readTopStatsFromFile(amountOfTopStats):
    topStats = readPreviousSession()
    if(len(topStats)<amountOfTopStats):
        return topStats[:len(topStats)]
    return topStats[:amountOfTopStats]

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
def makePrediction(newFight, statsToJudgeBy, trainingInstancesList, k):
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


