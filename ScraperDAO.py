import xml.etree.ElementTree

#Where the output of the scraper is located
XML_FILE_LOCATION="../UFCScraper/fighters.xml"
STAT_NOT_FOUND_CODE = -1

#This is a class to make storing the record of a fighter at the time of a specific fight easier
class recordAtTimeOfFight:
    def __init__(self, wins, losses):
        self.wins = wins
        self.losses = losses

#Returns the contents of the given node
def textof(node):
    if node is None or node.text==None:
        return ''
    else:
        return node.text

#Returns the amount of wins a fighter has on his record
def findFightersAmountOfWins(fighterNode):
    record = textof(fighterNode.find('fighterRecord')).replace(",", "-").replace("(", "-").split("-")
    if len(record) > 2:
        return(int(record[0]))
    else:
        return(STAT_NOT_FOUND_CODE)

# Returns the amount of losses a fighter has on his record
def findFightersAmountOfLosses(fighterNode):
    record = textof(fighterNode.find('fighterRecord')).replace(",", "-").replace("(", "-").split("-")
    if len(record) > 2:
        return (int(record[1]))
    else:
        return (STAT_NOT_FOUND_CODE)

# Returns the amount of losses a fighter has on his record
def findFightersAmountOfDraws(fighterNode):
    record = textof(fighterNode.find('fighterRecord')).replace(",", "-").replace("(", "-").split("-")
    if len(record) > 2:
        return (int(record[2]))
    else:
        return (STAT_NOT_FOUND_CODE)


#Returns the reach of a fighter in inches
def findFightersReach(fighterNode):
    reach = textof(fighterNode.find('fighterReach'))
    if len(reach) > 0:
        return(int(reach.split('"', 1)[0]))
    else:
        return(STAT_NOT_FOUND_CODE)

def findFightersLegReach(fighterNode):
    reach = textof(fighterNode.find('fighterLegReach'))
    if len(reach) > 0:
        return (int(reach.split('"', 1)[0]))
    else:
        return (STAT_NOT_FOUND_CODE)

#Returns the height of the fighter in centimentres
#Height must be formatted like this: 5' 8" ( 172 cm )
def findFightersHeight(fighterNode):
    height = textof(fighterNode.find('fighterHeight'))
    if(len(height)>0):
        return(int(height.split(' ')[3]))
    else:
        return(STAT_NOT_FOUND_CODE)

def findFightersWeight(fighterNode):
    weight = textof(fighterNode.find('fighterWeight'))
    if(len(weight)>0):
        return(int(weight.split(' ')[0]))
    else:
        return(STAT_NOT_FOUND_CODE)

def findFightersAge(fighterNode):
    age = textof(fighterNode.find('fighterAge'))
    if (len(age) > 0):
        return (int(age))
    else:
        return (STAT_NOT_FOUND_CODE)

def findFightersTotalStrikes(fighterNode):
    totalStrikes = textof(fighterNode.find('fighterTotalStrikes'))
    if (len(totalStrikes) > 0):
        return (int(totalStrikes))
    else:
        return (STAT_NOT_FOUND_CODE)

def findFightersSuccessfulStrikesPercentage(fighterNode):
    strikesPercent = textof(fighterNode.find('fighterSuccessfulStrikesPercentage'))
    if (strikesPercent.__contains__('%')):
        return (int(strikesPercent.split('%')[0]))
    else:
        return (STAT_NOT_FOUND_CODE)

def findFightersTotalTakedowns(fighterNode):
    totalTakedowns = textof(fighterNode.find('fighterTakedowns'))
    if (len(totalTakedowns) > 0):
        return (int(totalTakedowns))
    else:
        return (STAT_NOT_FOUND_CODE)

def findFightersSuccessfulTakedownsPercentage(fighterNode):
    takedownsPercent = textof(fighterNode.find('fighterSuccessfulTakedownsPercentage'))
    if (takedownsPercent.__contains__('%')):
        return (int(takedownsPercent.split('%')[0]))
    else:
        return (STAT_NOT_FOUND_CODE)

def findFightersSuccessfulStrikes(fighterNode):
    sucStrikes = textof(fighterNode.find('fighterSuccessfulStrikes'))
    if (len(sucStrikes) > 0):
        return (int(sucStrikes))
    else:
        return (STAT_NOT_FOUND_CODE)

def findFighterSuccessfulStandingStrikes(fighterNode):
    sucStrikes = textof(fighterNode.find('fighterSuccessfulStrikes').find('fighterSuccessfulStandingStrikes'))
    if (len(sucStrikes) > 0):
        return (int(sucStrikes))
    else:
        return (STAT_NOT_FOUND_CODE)

def findFighterSuccessfulGroundStrikes(fighterNode):
    sucStrikes = textof(fighterNode.find('fighterSuccessfulStrikes').find('fighterSuccessfulGroundStrikes'))
    if (len(sucStrikes) > 0):
        return (int(sucStrikes))
    else:
        return (STAT_NOT_FOUND_CODE)

def findFighterSuccessfulClinchStrikes(fighterNode):
    sucStrikes = textof(fighterNode.find('fighterSuccessfulStrikes').find('fighterSuccessfulClinchStrikes'))
    if (len(sucStrikes) > 0):
        return (int(sucStrikes))
    else:
        return (STAT_NOT_FOUND_CODE)

def findFightersSubmissions(fighterNode):
    totalSubmissions = textof(fighterNode.find('fighterSubmissions'))
    if (len(totalSubmissions) > 0):
        return (int(totalSubmissions))
    else:
        return (STAT_NOT_FOUND_CODE)

def findFightersPasses(fighterNode):
    totalPasses = textof(fighterNode.find('fighterPasses'))
    if (len(totalPasses) > 0):
        return (int(totalPasses))
    else:
        return (STAT_NOT_FOUND_CODE)

def findFightersSweeps(fighterNode):
    totalSweeps = textof(fighterNode.find('fighterSweeps'))
    if (len(totalSweeps) > 0):
        return (int(totalSweeps))
    else:
        return (STAT_NOT_FOUND_CODE)

def findFightersStrikesAvoidedPercentage(fighterNode):
    percent = textof(fighterNode.find('fighterStrikesAvoidedPercentage'))
    if (percent.__contains__('%')):
        return (int(percent.split('%')[0]))
    else:
        return (STAT_NOT_FOUND_CODE)

def findFightersTakedownsAvoidedPercentage(fighterNode):
    percent = textof(fighterNode.find('fighterTakedownsAvoidedPercentage'))
    if (percent.__contains__('%')):
        return (int(percent.split('%')[0]))
    else:
        return (STAT_NOT_FOUND_CODE)

def findAmountOfUFCOpponents(fighterNode):
    i=0
    for opponent in fighterNode.find('fighterOpponents').findall('opponentName'):
        i+=1
    return i

def findFightersFights(fighterNode):
    fights = {}
    for opponent in fighterNode.find('fighterOpponents').findall('opponentName'):
        wins = int(textof(opponent.find('fighterWinsPriorToFight'))) if textof(opponent.find('fighterWinsPriorToFight'))!='' else 0
        losses = int(textof(opponent.find('fighterLossesPriorToFight'))) if textof(opponent.find('fighterLossesPriorToFight')) != '' else 0
        fights[(textof(opponent).strip(),textof(opponent.find('dateOfFight')))] = recordAtTimeOfFight(wins,losses)
    return fights

#Gets the normalized difference between two stats, but assumes the stats are equal if one of the fighters is missing the stat
def getDifference(a,b):
    if(a == STAT_NOT_FOUND_CODE or b == STAT_NOT_FOUND_CODE or a==b):
        return(0)
    else:
        return((a/(a+b))-(b/(a+b)))

# Allows for xml parsing of the data
tree = xml.etree.ElementTree.parse(XML_FILE_LOCATION).getroot()

#Relates the name of the fighter to the stats of that fighter contained in a dictionary
fightersNameToInfoDict = {}
for fighterNode in tree.findall('fighterName'):

    #Dictionary where the key is the name of the stat and the value is that stat for the fighter
    fighterInfoDict = {}
    fighterInfoDict["Wins"] = findFightersAmountOfWins(fighterNode)
    fighterInfoDict["Reach"] = findFightersReach(fighterNode)
    fighterInfoDict["Height"] = findFightersHeight(fighterNode)
    fighterInfoDict["Losses"] = findFightersAmountOfLosses(fighterNode)
    fighterInfoDict["Draws"] = findFightersAmountOfDraws(fighterNode)
    fighterInfoDict["Age"] = findFightersAge(fighterNode)
    fighterInfoDict["Weight"] = findFightersWeight(fighterNode)
    fighterInfoDict["LegReach"] = findFightersLegReach(fighterNode)
    fighterInfoDict["TotalStrikes"] = findFightersTotalStrikes(fighterNode)
    fighterInfoDict["SuccessfulStrikesPercentage"] = findFightersSuccessfulStrikesPercentage(fighterNode)
    fighterInfoDict["TotalTakedowns"] = findFightersTotalTakedowns(fighterNode)
    fighterInfoDict["SuccessfulTakedownsPercentage"] = findFightersSuccessfulTakedownsPercentage(fighterNode)
    fighterInfoDict["SuccessfulStrikes"] = findFightersSuccessfulStrikes(fighterNode)
    fighterInfoDict["SuccessfulStandingStrikes"] = findFighterSuccessfulStandingStrikes(fighterNode)
    fighterInfoDict["SuccessfulGroundStrikes"] = findFighterSuccessfulGroundStrikes(fighterNode)
    fighterInfoDict["SuccessfulClinchStrikes"] = findFighterSuccessfulClinchStrikes(fighterNode)
    fighterInfoDict["Submissions"] = findFightersSubmissions(fighterNode)
    fighterInfoDict["Passes"] = findFightersPasses(fighterNode)
    fighterInfoDict["Sweeps"] = findFightersSweeps(fighterNode)
    fighterInfoDict["StrikesAvoidedPercentage"] = findFightersStrikesAvoidedPercentage(fighterNode)
    fighterInfoDict["TakedownsAvoidedPercentage"] = findFightersTakedownsAvoidedPercentage(fighterNode)
    fighterInfoDict["UFCFights"] = findAmountOfUFCOpponents(fighterNode)
    fighterInfoDict["Fights"] = findFightersFights(fighterNode)


    fightersNameToInfoDict[textof(fighterNode).strip()] = fighterInfoDict

def getNamesOfStats():
    keys=[]
    for key in fighterDifferencesAndResultsList[0]:
        if key != "Result":
            keys.append(key)
    return (keys)

def getDifferencesBetweenFighters(fighterNameA,fighterNameB):
    differencesDict = {}
    for key in fightersNameToInfoDict[fighterNameA]:
        differencesDict[key + "Difference"] = getDifference(fightersNameToInfoDict[fighterNameA][key],fightersNameToInfoDict[fighterNameB][key])
    return(differencesDict)

#Collect the stat differences and the result of the fight and  put each fight in a list
fighterDifferencesAndResultsList = []

for fighterNode in tree.findall('fighterName'):
    fighterName = textof(fighterNode).strip()

    for opponentNode in fighterNode.find('fighterOpponents').findall('opponentName'):
        opponentName = textof(opponentNode).strip()
        #Only include results where we know the stats of the other fighter and we know the result of the fight was either a win or a loss
        if((textof(opponentNode.find('fightResult'))=='Win' or textof(opponentNode.find('fightResult'))=='Loss') and opponentName in fightersNameToInfoDict):

            #Create a dictionary to avoid the magic numbers prevalent in lists
            #This dictionary contains the (fighter stat - opponent stat) as well as the result of the fight
            differencesAndResultDict = {}

            #Calculates differences that don't rely on time
            for key in fightersNameToInfoDict[fighterName]:
                if key not in ["Fights","Wins","Losses"]:
                    differencesAndResultDict[key + "Difference"] = getDifference(fightersNameToInfoDict[fighterName][key],fightersNameToInfoDict[opponentName][key])

            #Calculates differences that do rely on time

            #Fight tuples are combinations of opponents name as well as the date they fought
            fightTuple = (opponentName,textof(opponentNode.find('dateOfFight')))
            opponentFightTuple =(fighterName,textof(opponentNode.find('dateOfFight')))

            #Finds the differences between the wins and losses at the time of the fight
            if fightTuple in fightersNameToInfoDict[fighterName]["Fights"] and opponentFightTuple in fightersNameToInfoDict[opponentName]["Fights"]:
                differencesAndResultDict["WinsDifference"] = getDifference(fightersNameToInfoDict[fighterName]["Fights"][fightTuple].wins,fightersNameToInfoDict[opponentName]["Fights"][opponentFightTuple].wins)
                differencesAndResultDict["LossesDifference"] = getDifference(fightersNameToInfoDict[fighterName]["Fights"][fightTuple].losses,fightersNameToInfoDict[opponentName]["Fights"][opponentFightTuple].losses)
            else:
                differencesAndResultDict["WinsDifference"] = 0
                differencesAndResultDict["LossesDifference"] = 0

            differencesAndResultDict["Result"] = textof(opponentNode.find('fightResult'))
            fighterDifferencesAndResultsList.append(differencesAndResultDict)






