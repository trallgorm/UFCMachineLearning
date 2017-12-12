import ScraperDAO
import kNNshared
import math
import sys

k = int(math.sqrt(len(ScraperDAO.fighterDifferencesAndResultsList)))

def testTopStats():
    datalists = kNNshared.splitDataset(0,ScraperDAO.fighterDifferencesAndResultsList)

    correctGuesses = 0
    i=0
    for fight in datalists["TestList"]:
        i+=1
        if fight["Result"] == predictOutcomeTopStats(fight,100)[0]:
            correctGuesses += 1
        print("Tested: " + str(i) + "/" + str(len(datalists["TestList"])) + ", Correct: " + str(round(100*correctGuesses / i,2)) + "%")

    return ((correctGuesses / len(datalists["TestList"])) * 100)

def testWeightedStats():
    datalists = kNNshared.splitDataset(0,ScraperDAO.fighterDifferencesAndResultsList)
    i=0
    correctGuesses = 0
    for fight in datalists["TestList"]:
        i+=1
        if fight["Result"] == predictOutcomeWeighted(fight)[0]:
            correctGuesses += 1
        print("Tested: " +str(i) +"/"+str(len(datalists["TestList"])) + ", Correct: " + str(round(100*correctGuesses/i,2)) +"%" )

    return ((correctGuesses / len(datalists["TestList"])) * 100)


def predictOutcomeTopStatsWrapper(fighterNameA, fighterNameB, amountOfTopStats):
    result = predictOutcomeTopStats(ScraperDAO.getDifferencesBetweenFighters(fighterNameA, fighterNameB), amountOfTopStats)
    if result[0] == "Win":
        print(fighterNameA + " wins with " + result[1] + "% accuracy")
    else:
        print(fighterNameB + " wins with " + result[1] + "% accuracy")

#Gets all the recorded stats and has them predict who's going to win
def predictOutcomeAllStatsWrapper(fighterNameA, fighterNameB):
    return predictOutcomeTopStatsWrapper(fighterNameA, fighterNameB, sys.maxint)

def predictOutcomeWeightedWrapper(fighterNameA, fighterNameB):
    result = predictOutcomeWeighted(ScraperDAO.getDifferencesBetweenFighters(fighterNameA, fighterNameB))
    if result[0] == "Win":
        print(fighterNameA + " wins with " + result[1] + "% accuracy")
    else:
        print(fighterNameB + " wins with " + result[1] + "% accuracy")

#Weighs the importance of a prediction based on how accurate the stats are
def predictOutcomeWeighted(fighterDifferences):
    winTotal = 0.0
    lossTotal = 0.0
    for statArray in kNNshared.readTopStatsFromFile(1000):
        if kNNshared.makePrediction(fighterDifferences,statArray[0],ScraperDAO.fighterDifferencesAndResultsList, k)=="Win":
            winTotal+=(1*(statArray[1]/100))
        else:
            lossTotal+=(1*(statArray[1]/100))
    if winTotal > lossTotal:
        return ("Win", str(winTotal * 100 / (winTotal + lossTotal)))
    else:
        return ("Loss", str(lossTotal * 100 / (winTotal + lossTotal)))

#Predicts the outcome of a fight given two fighters based on the top X stats rated by accuracy
def predictOutcomeTopStats(fighterDifferences,amountOfTopStats):

    win=0
    loss=0
    for statArray in kNNshared.readTopStatsFromFile(amountOfTopStats):
        if kNNshared.makePrediction(fighterDifferences,statArray[0],ScraperDAO.fighterDifferencesAndResultsList, k)=="Win":
            win+=1
        else:
            loss+=1
    if win>loss:
        return("Win",str(win*100/(win+loss)))
    else:
        return("Loss",str(loss*100/(win+loss)))

if sys.argv[1] == "-testWeighted":
    testWeightedStats()
elif sys.argv[1] == "-testTop":
    testTopStats()
else:
    if "-top" in sys.argv:
        predictOutcomeTopStatsWrapper(sys.argv[1],sys.argv[2],int(sys.argv[4]))
    else:
        predictOutcomeWeightedWrapper(sys.argv[1],sys.argv[2])


