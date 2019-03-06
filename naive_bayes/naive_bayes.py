# Code to build the classifier
from columns import *
import math

FILE = "../data/Preprocessed.csv"

# Names of attributes
COLUMN_NAMES = ["TOTAL_VISITS", "TOTAL_SPENT", "AVRG_SPENT_PER_VISIT", "HAS_CREDIT_CARD", "PSWEATERS", "PKNIT_TOPS",
                "PKNIT_DRES", "PBLOUSES", "PJACKETS", "PCAR_PNTS", "PCAS_PNTS", "PSHIRTS", "PDRESSES", "PSUITS",
                "POUTERWEAR", "PJEWELRY", "PFASHION", "PLEGWEAR", "PCOLLSPND", "AMSPEND", "PSSPEND", "CCSPEND",
                "AXSPEND", "GMP", "PROMOS_ON_FILE", "FREQ_DAYS", "MARKDOWN", "PRODUCT_CLASSES", "COUPONS", "STYLES",
                "STORES", "VALPHON", "WEB", "MAILED", "RESPONDED", "RESPONSERATE", "LTFREDAY", "CLUSTYPE", "PERCRET",
                "RESP"]


# Create counts of each relevant word being in a category
def create_counts(c_types, data):
    probs = {}
    class_counts = [0, 0]
    inputCSV = open(data)

    for row in inputCSV:
        arr = row.rstrip().split(",")
        c_label = arr[-1]
        class_counts[0 if c_label == "TRUE" else 1] += 1

        # Iterate all attributes, last is class label
        for i in range(len(arr) - 1):
            val = arr[i]
            attr = COLUMN_NAMES[i]

            # Numeric type
            if c_types[i] == "N":
                val = float(val)

                if attr not in probs:
                    # For numeric, store a list of the values, to later estimate mean and SD
                    probs[attr] = {"TRUE": [], "FALSE": []}

                probs[attr][c_label].append(val)
            # Discrete type
            else:
                if attr not in probs:
                    # For discrete, start with an empty dict because we don't know the values of the attribute
                    probs[attr] = {"TRUE": {}, "FALSE": {}}

                if val not in probs[attr][c_label]:
                    probs[attr]["TRUE"][val] = 0
                    probs[attr]["FALSE"][val] = 0

                probs[attr][c_label][val] += 1

    inputCSV.close()

    return probs, class_counts


# Convert counts to probabilities
def convert(c_types, probs, total):
    for i in range(len(COLUMN_NAMES) - 1):
        attr = COLUMN_NAMES[i]

        # Numeric type
        if c_types[i] == "N":
            # Do the same thing for TRUE/FALSE
            for label in probs[attr]:
                list_values = probs[attr][label]
                mean = sum(list_values)/float(len(list_values))

                # Sum variance
                variance = 0
                for val in list_values:
                    variance += pow(val - mean, 2)

                variance /= float(len(list_values) - 1)

                # Save the estimated mean and standard deviation in a tuple
                probs[attr][label] = (mean, math.sqrt(variance))
        # Discrete type
        else:
            # Do the same thing for TRUE/FALSE
            for label in probs[attr]:
                # Iterate over all attribute values
                for val in probs[attr][label]:
                    probs[attr][label][val] /= float(total[0 if label == "TRUE" else 1])


if __name__ == "__main__":
    column_types = get_column_types(FILE)
    probabilities, totals = create_counts(column_types, FILE)
    convert(column_types, probabilities, totals)

    print(probabilities)
