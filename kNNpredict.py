import ScraperDAO
import kNNshared
import math
import sys

k = int(math.sqrt(len(ScraperDAO.fighterDifferencesAndResultsList)))

def testTopStats():
    datalists = kNNshared.splitDataset(0.66,ScraperDAO.fighterDifferencesAndResultsList)

    correctGuesses = 0
    for fight in datalists["TestList"]:
        if fight["Result"] == predictOutcomeTopStats(fight,1000)[0]:
            correctGuesses += 1
        print(correctGuesses)

    return ((correctGuesses / len(datalists["TestList"])) * 100)


def predictOutcomeTopStatsWrapper(fighterNameA, fighterNameB, amountOfTopStats):
    result = predictOutcomeTopStats(ScraperDAO.getDifferencesBetweenFighters(fighterNameA, fighterNameB), amountOfTopStats)
    if result[0] == "Win":
        print(fighterNameA + " wins with " + result[1] + "% accuracy")
    else:
        print(fighterNameB + " wins with " + result[1] + "% accuracy")


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



#predictOutcomeTopStatsWrapper(sys.argv[1],sys.argv[2],1000)
print(testTopStats())