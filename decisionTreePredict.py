import ScraperDAO
import json
import sys

#Given a node of the decision tree and the differences between the two fighters, predicts who is going to win
def predict(node, differencesDict):
	print(node['stat'])
	print(differencesDict[node['stat']])
	print(node['value'])
	if differencesDict[node['stat']] < node['value']:
		if str(node['lower']) not in ["Win","Loss"]:
			return predict(node['lower'], differencesDict)
		else:
			return node['lower']
	else:
		if str(node['higher']) not in ["Win","Loss"]:
			return predict(node['higher'], differencesDict)
		else:
			return node['higher']

#A wrapper for the predict function, given a decision tree and two names of fighters, predicts who is going to win
def predictWrapper(tree, fighterNameA, fighterNameB):
	result = predict(tree,ScraperDAO.getDifferencesBetweenFighters(fighterNameA,fighterNameB))
	if result == "Win":
		print(fighterNameA + " will win")
	else:
		print(fighterNameB + " will win")

tree={}
with open("decisiontree.json","r") as file:
    tree = json.load(file)

predictWrapper(tree,sys.argv[1],sys.argv[2])
