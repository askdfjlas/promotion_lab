FILE = "data/Clothing_Store.csv"
OUT = "data/Preprocessed.csv"

# Names of attributes
columns = ["CUSTOMER_ID", "ZIP_CODE", "TOTAL_VISITS", "TOTAL_SPENT", "AVRG_SPENT_PER_VISIT", "HAS_CREDIT_CARD",
           "PSWEATERS", "PKNIT_TOPS", "PKNIT_DRES", "PBLOUSES", "PJACKETS", "PCAR_PNTS", "PCAS_PNTS", "PSHIRTS",
           "PDRESSES", "PSUITS", "POUTERWEAR", "PJEWELRY", "PFASHION", "PLEGWEAR", "PCOLLSPND", "AMSPEND", "PSSPEND",
           "CCSPEND", "AXSPEND", "SPEND_LAST_MONTH", "SPEND_LAST_3MONTH", "SPEND_LAST_6MONTH", "SPENT_LAST_YEAR",
           "GMP", "PROMOS_ON_FILE", "DAYS_ON_FILE", "FREQ_DAYS", "MARKDOWN", "PRODUCT_CLASSES", "COUPONS", "STYLES",
           "STORES", "STORELOY", "VALPHON", "WEB", "MAILED", "RESPONDED", "RESPONSERATE", "LTFREDAY", "CLUSTYPE",
           "PERCRET", "RESP"]

# Generate dict from columns
columns_dict = {}
for i in range(len(columns)):
    columns_dict[columns[i]] = i

# Attributes which aren't useful
remove = ["CUSTOMER_ID", "ZIP_CODE", "SPEND_LAST_MONTH", "SPEND_LAST_3MONTH", "SPEND_LAST_6MONTH",
          "SPENT_LAST_YEAR", "DAYS_ON_FILE", "STORELOY"]

# Bins for attributes made discrete
bins = {"TOTAL_VISITS": [1, 2, 5, 10, 20], "TOTAL_SPENT": [0, 100, 400, 1000, 2000],
        "AVRG_SPENT_PER_VISIT": [0, 50, 150, 300], "PCLOTHING": [0, 0.05, 0.2, 0.5, 0.9],
        "GMP": [0, 0.5, 0.6], "PROMOS_ON_FILE": [0, 5, 15, 25], "FREQ_DAYS": [0, 50, 150, 300],
        "MARKDOWN": [0, 0.1, 0.25, 0.4], "PRODUCT_CLASSES": [0, 4, 10, 20], "STYLES": [0, 5, 15, 30],
        "MAILED": [0, 3, 5, 8], "RESPONDED": [0, 0.1, 1, 3, 6], "RESPONSERATE": [0, 0.1, 1, 25, 50, 75],
        "LTFREDAY": [0, 40, 80, 150], "PERC_RET": [0, 0.000001, 0.1, 0.4, 0.8]}


# General function for placing a value into an appropriate bin
def place_into_bin(val, breakpoints):
    for index in range(1, len(breakpoints)):
        if val <= breakpoints[index]:
            return breakpoints[index - 1]
    return breakpoints[-1]


# Attributes needing specific changes
def franchise_visit(val):
    if val == 0:
        return "UNVISITED"
    return "VISITED"


def coupons(val):
    if val <= 3:
        return val
    return 4


def stores(val):
    if val <= 4:
        return val
    return 5


def clusters(val):
    if val in [10, 1, 4, 16, 8, 15]:
        return "C" + str(val)
    return "Other"


def num_to_bool(val):
    if val == 1:
        return "TRUE"
    return "FALSE"


# Attribute names mapped to their changing function
changes = {"AMSPEND": franchise_visit, "PSSPEND": franchise_visit, "CCSPEND": franchise_visit,
           "AXSPEND": franchise_visit, "COUPONS": coupons, "STORES": stores, "CLUSTYPE": clusters,
           "HAS_CREDIT_CARD": num_to_bool, "WEB": num_to_bool, "RESP": num_to_bool}


def main():
    inputCSV = open(FILE)
    outputCSV = open(OUT, "w")

    for line in inputCSV:
        arr = line.rstrip().split(',')

        for i in range(len(arr)):
            attribute = columns[i]

            # If the attribute is irrelevant, remove it
            if attribute in remove:
                continue

            # If attribute is one of the clothing proportions
            if columns_dict["PSWEATERS"] <= columns_dict[attribute] <= columns_dict["PCOLLSPND"]:
                trueName = "PCLOTHING"
            else:
                trueName = attribute

            # See if the attribute is one of which needs to be made discrete
            if trueName in bins:
                outputCSV.write(str(place_into_bin(float(arr[i]), bins[trueName])))
            # If it needs to undergo a changing function
            elif trueName in changes:
                outputCSV.write(str(changes[trueName](float(arr[i]))))
            # If it remains the same
            else:
                outputCSV.write(arr[i])

            outputCSV.write("\n" if i == len(arr) - 1 else ",")

    inputCSV.close()
    outputCSV.close()


if __name__ == "__main__":
    main()