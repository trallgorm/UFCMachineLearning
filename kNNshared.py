import math

def readTopStatsFromFile():
    i=0
    with open("top_stats.txt", "r") as topStatsFile:
        topStats = []
        for line in topStatsFile:
            if i<1000:
                i+=1
                if line !='\n' or line!='':
                    statArray=line.strip().split(',')[1:]
                    if '' in statArray:
                        statArray.remove('')
                    topStats.append(statArray)
            else:
                break
    topStatsFile.close()
    return topStats

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
