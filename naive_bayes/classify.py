# Code to classify entries

from naive_bayes import *
import math

labels = ["TRUE", "FALSE"]


# Probability density function
def pdf(val, mean, sd):
    return (
        (pow(math.e, -pow(val - mean, 2)/(2*pow(sd, 2)))) /
        (sd*math.sqrt(2*math.pi))
    )


def classify_entry(vals, c_types, probs, total_counts):
    scores = [0, 0]

    for i in range(len(labels)):
        scores[i] += math.log(total_counts[i], 2)

        for j in range(len(vals)):
            attr = COLUMN_NAMES[j]

            # Numeric type
            if c_types[j] == "N":
                mean = probs[attr][labels[i]][0]
                sd = probs[attr][labels[i]][1]

                try:
                    scores[i] += math.log(pdf(vals[j], mean, sd), 2)
                except ValueError:
                    pass
            # Discrete type
            else:
                try:
                    scores[i] += math.log(probs[attr][labels[i]][vals[j]])
                except ValueError:
                    pass

    return labels[0 if scores[0] > scores[1] else 1]


if __name__ == "__main__":
    types = get_column_types(FILE)
    probs, c_totals = create_counts(types, FILE)
    convert(types, probs, c_totals)

    test = [1, 100, 150, "FALSE", 0.05, 0, 0, 0.2, 0, 0.2, 0, 0.05, 0, 0, 0, 0, 0, 0, 0.2, "UNVISITED",
            "UNVISITED", "VISITED", "UNVISITED", 0.5, 15, 300, 0, 4, 1.0, 5, 1.0, "N", "FALSE", 3, 0, 0, 80, "C10.0", 0]

    print(classify_entry(test, types, probs, c_totals))
