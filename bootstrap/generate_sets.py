# Code to store training and test sets in .csv files, generated using bootstrap
import random


def main(filename):
    inputCSV = open(filename)

    # Temporarily store csv file in list of strings
    data = []

    for line in inputCSV:
        data.append(line.rstrip())

    inputCSV.close()

    # Create a copy of the list, so sampling with replacement can be done
    testing_set = list(data)
    training_set = []

    for i in range(len(data)):
        index = random.randint(0, len(data) - 1)
        training_set.append(data[index])

        # Placeholder
        testing_set[index] = ""

    # Output testing and training sets to a csv file
    test_out = open("data/test_set.csv", "w")
    train_out = open("data/train_set.csv", "w")

    for s in testing_set:
        if s != "":
            test_out.write(s + "\n")

    for s in training_set:
        train_out.write(s + "\n")

    test_out.close()
    train_out.close()


if __name__ == "__main__":
    main("../data/Preprocessed.csv")