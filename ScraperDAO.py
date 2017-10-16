import xml.etree.ElementTree

#Where the output of the scraper is located
XML_FILE_LOCATION="../UFCScraper/fighters.xml"
STAT_NOT_FOUND_CODE = -1

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

#Gets the difference between two stats, but assumes the stats are equal if one of the fighters is missing the stat
def getDifference(a,b):
    if(a == STAT_NOT_FOUND_CODE or b == STAT_NOT_FOUND_CODE):
        return(0)
    else:
        return(a-b)

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

    fightersNameToInfoDict[textof(fighterNode).strip()] = fighterInfoDict

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
            differencesAndResultDict["Result"] = textof(opponentNode.find('fightResult'))
            differencesAndResultDict["WinsDifference"] = getDifference(fightersNameToInfoDict[fighterName]["Wins"],fightersNameToInfoDict[opponentName]["Wins"])
            differencesAndResultDict["ReachDifference"] = getDifference(fightersNameToInfoDict[fighterName]["Reach"],fightersNameToInfoDict[opponentName]["Reach"])
            differencesAndResultDict["HeightDifference"] = getDifference(fightersNameToInfoDict[fighterName]["Height"],fightersNameToInfoDict[opponentName]["Height"])
            differencesAndResultDict["LossesDifference"] = getDifference(fightersNameToInfoDict[fighterName]["Losses"],fightersNameToInfoDict[opponentName]["Losses"])
            differencesAndResultDict["DrawsDifference"] = getDifference(fightersNameToInfoDict[fighterName]["Draws"],fightersNameToInfoDict[opponentName]["Draws"])
            differencesAndResultDict["AgeDifference"] = getDifference(fightersNameToInfoDict[fighterName]["Age"],fightersNameToInfoDict[opponentName]["Age"])
            differencesAndResultDict["LegReachDifference"] = getDifference(fightersNameToInfoDict[fighterName]["Weight"],fightersNameToInfoDict[opponentName]["Weight"])
            differencesAndResultDict["WeightDifference"] = getDifference(fightersNameToInfoDict[fighterName]["LegReach"],fightersNameToInfoDict[opponentName]["LegReach"])

            fighterDifferencesAndResultsList.append(differencesAndResultDict)


