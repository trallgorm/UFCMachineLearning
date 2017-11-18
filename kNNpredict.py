import ScraperDAO
import kNNshared
import math
import sys

k = int(math.sqrt(len(ScraperDAO.fighterDifferencesAndResultsList)))

#Predicts the outcome of a fight given two fighters
def predictOutcome(fighterNameA,fighterNameB):
    ScraperDAO.getDifferencesBetweenFighters(fighterNameA,fighterNameB)
    win=0
    loss=0
    for statArray in kNNshared.readTopStatsFromFile():
        if kNNshared.makePrediction(ScraperDAO.getDifferencesBetweenFighters(fighterNameA,fighterNameB),statArray,ScraperDAO.fighterDifferencesAndResultsList, k)=="Win":
            win+=1
        else:
            loss+=1

    if win>loss:
        return (fighterNameA + " wins with " + str(win*100/(win+loss)) + "% accuracy")
    else:
        return (fighterNameB + " wins with " + str(loss*100/(win+loss)) + "% accuracy")

print(predictOutcome(sys.argv[1],sys.argv[2]))