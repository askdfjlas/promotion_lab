# Code to get column types from preprocessed data


def get_column_types(filename):
    inputCSV = open(filename)
    column_types = []

    for line in inputCSV:
        arr = line.rstrip().split(',')

        for el in arr:
            try:
                float(el)
                column_types.append("N")
            except ValueError:
                column_types.append("D")

        break

    inputCSV.close()
    return column_types


if __name__ == "__main__":
    print(get_column_types("../data/Preprocessed.csv"))