import dtree_build
import sys
import csv


def main(col_names=None):
    # parse command-line arguments to read the name of the input csv file
    # and optional 'draw tree' parameter
    if len(sys.argv) < 2:  # input file name should be specified
        print ("Please specify input csv file name")
        return

    csv_file_name = sys.argv[1]

    data = []
    with open(csv_file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            arr = list(row)

            # Try converting to numeric if possible
            for i in range(len(arr)):
                try:
                    arr[i] = float(arr[i])
                except ValueError:
                    pass

            data.append(arr)

    print("Total number of records = ",len(data))
    tree = dtree_build.buildtree(data, min_gain=0.002, min_samples=80)

    dtree_build.printtree(tree, '', col_names)

    max_tree_depth = dtree_build.max_depth(tree)
    print("max number of questions=" + str(max_tree_depth))

    if len(sys.argv) > 2: # draw option specified
        import dtree_draw
        dtree_draw.drawtree(tree, jpeg=csv_file_name+'.jpg')

    if len(sys.argv) > 3:  # create json file for d3.js visualization
        import json
        import dtree_to_json
        json_tree = dtree_to_json.dtree_to_jsontree(tree, col_names)
        print(json_tree)

        # create json data for d3.js interactive visualization
        with open(csv_file_name + ".json", "w") as write_file:
            json.dump(json_tree, write_file)


if __name__ == "__main__":
    col_names = ["TOTAL_VISITS", "TOTAL_SPENT", "AVRG_SPENT_PER_VISIT", "HAS_CREDIT_CARD",
           "PSWEATERS", "PKNIT_TOPS", "PKNIT_DRES", "PBLOUSES", "PJACKETS", "PCAR_PNTS", "PCAS_PNTS", "PSHIRTS",
           "PDRESSES", "PSUITS", "POUTERWEAR", "PJEWELRY", "PFASHION", "PLEGWEAR", "PCOLLSPND", "AMSPEND", "PSSPEND",
           "CCSPEND", "AXSPEND", "GMP", "PROMOS_ON_FILE", "FREQ_DAYS", "MARKDOWN", "PRODUCT_CLASSES", "COUPONS",
           "STYLES", "STORES", "VALPHON", "WEB", "MAILED", "RESPONDED", "RESPONSERATE", "LTFREDAY", "CLUSTYPE",
           "PERCRET", "RESP"]
    main(col_names)





