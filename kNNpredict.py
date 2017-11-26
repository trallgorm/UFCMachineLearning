import ScraperDAO
import kNNshared
import math
import sys

k = int(math.sqrt(len(ScraperDAO.fighterDifferencesAndResultsList)))

#Predicts the outcome of a fight given two fighters based on the top X stats rated by accuracy
def predictOutcomeTopStats(fighterNameA,fighterNameB,amountOfTopStats):
    ScraperDAO.getDifferencesBetweenFighters(fighterNameA,fighterNameB)
    win=0
    loss=0
    for statArray in kNNshared.readTopStatsFromFile(amountOfTopStats):
        if kNNshared.makePrediction(ScraperDAO.getDifferencesBetweenFighters(fighterNameA,fighterNameB),statArray[0],ScraperDAO.fighterDifferencesAndResultsList, k)=="Win":
            win+=1
        else:
            loss+=1
    if win>loss:
        return (fighterNameA + " wins with " + str(win*100/(win+loss)) + "% accuracy")
    else:
        return (fighterNameB + " wins with " + str(loss*100/(win+loss)) + "% accuracy")

print(predictOutcomeTopStats(sys.argv[1],sys.argv[2],1000))