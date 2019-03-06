# Code for testing naive-bayes vs decision tree, training/testing generated using bootstrap
import sys
sys.path.insert(0, '../naive_bayes/')
sys.path.insert(0, '../decision_tree/')

from classify import *
from dtree_build import *

TEST = "data/test_set.csv"
TRAIN = "data/train_set.csv"


# Convert csv into a list of lists
def csv_to_data(filename):
    inputCSV = open(filename)
    data = []

    for line in inputCSV:
        arr = line.rstrip().split(",")

        # # Try converting to numeric if possible
        for i in range(len(arr)):
            try:
                arr[i] = float(arr[i])
            except ValueError:
                pass

        data.append(arr)

    inputCSV.close()

    return data


def test_naive_bayes(testData):
    types = get_column_types(TRAIN)
    probs, c_totals = create_counts(types, FILE)
    convert(types, probs, c_totals)

    correct = 0
    total = 0

    for arr in testData:
        # Pass in all data except for class label
        res = classify_entry(arr[:-1], types, probs, c_totals)

        if res == arr[-1]:
            correct += 1

        total += 1

    return float(correct)/total * 100


def test_decision_tree(testData, trainData):
    tree = buildtree(trainData, min_gain=0.002, min_samples=80)

    correct = 0
    total = 0

    for arr in testData:
        # Pass in all data except for class label
        vals = classify(arr[:-1], tree)

        max_key = None
        for k in vals:
            if max_key is None or vals[k] > vals[max_key]:
                max_key = k

        if max_key == arr[-1]:
            correct += 1

        total += 1

    return float(correct)/total * 100


def main():
    trainData = csv_to_data(TRAIN)
    testData = csv_to_data(TEST)

    print("Naive bayes accuracy: " + str(test_naive_bayes(testData)))
    print("Decision tree accuracy: " + str(test_decision_tree(testData, trainData)))


if __name__ == "__main__":
    main()