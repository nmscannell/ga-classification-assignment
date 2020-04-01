from learning import *
from probabilistic_learning import *

zoo1train = DataSet(name='Files/zoo1train', exclude=[0])
zoo2train = DataSet(name='Files/zoo2train', exclude=[0])

zoo1test = DataSet(name='Files/zoo1test', exclude=[0])
zoo2test = DataSet(name='Files/zoo2test', exclude=[0])

DTL = DecisionTreeLearner(zoo1train)
DTL2 = DecisionTreeLearner(zoo2train)
nbd = NaiveBayesLearner(zoo1train, continuous=False)
nbd2 = NaiveBayesLearner(zoo2train, continuous=False)

attributes = ["hair", "feathers", "eggs", "milk", "airborne", "aquatic", "predator", "toothed", "backbone", "breathes", "venomous", "fins", "legs", "tail", "domestic", "catsize"]

write_file = "Files/classification_results.txt"
with open(write_file, 'w') as file:
    file.write("Zoo1 test set: \n\n")
    for i in range(6):
        file.write("\n" + str(zoo1test.examples[i]))
    file.write("\n\nDecision Tree Zoo1 results: \n")
    numCorrect = 0
    for i in range(6):
        file.write("\n" + DTL(zoo1test.examples[i]))
        if zoo1test.examples[i][17] == DTL(zoo1test.examples[i]):
            numCorrect += 1
    file.write("\n\nMaximum Depth of Tree: " + str(DTL.max_depth()))
    file.write("\n\nPredictors: ")
    for i in DTL.get_predictors([]):
        file.write(attributes[i-1] + " ")
    file.write("\n\nPercentage correct: " + str(numCorrect*100/6))

    file.write("\n\nNaive Bayes Zoo1 results: \n")
    numCorrect = 0
    for i in range(6):
        file.write("\n" + nbd(zoo1test.examples[i]))
        if zoo1test.examples[i][17] == nbd(zoo1test.examples[i]):
            numCorrect += 1
    file.write("\n\nPercentage correct: " + str(numCorrect * 100 / 6))

    file.write("\n\nZoo2 test set: \n\n")
    for i in range(6):
        file.write("\n" + str(zoo2test.examples[i]))

    file.write("\n\nDecision Tree Zoo2 results: \n")
    numCorrect = 0
    for i in range(6):
        file.write("\n" + str(DTL2(zoo2test.examples[i])))
        if zoo2test.examples[i][17] == DTL2(zoo2test.examples[i]):
            numCorrect += 1
    file.write("\n\nMaximum Depth of Tree: " + str(DTL2.max_depth()))
    file.write("\n\nPredictors: ")
    for i in DTL2.get_predictors([]):
        file.write(attributes[i - 1] + " ")
    file.write("\n\nPercentage correct: " + str(numCorrect * 100 / 6))

    file.write("\n\nNaive Bayes Zoo2 results: \n")
    numCorrect = 0
    for i in range(6):
        file.write("\n" + str(nbd2(zoo2test.examples[i])))
        if zoo2test.examples[i][17] == nbd2(zoo2test.examples[i]):
            numCorrect += 1
    file.write("\n\nPercentage correct: " + str(numCorrect * 100 / 6))
