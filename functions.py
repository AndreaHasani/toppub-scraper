import csv



def writeCsv(filename, data):
    """
    | Write to a csv file from $data with $filename.
    | data needs to be a list for parsing exmple [[], []]
    """

    with open(filename + '.csv', 'w') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=',')

        for item in data:
            row = []
            for i in item:
                if len(i) == 1:
                    row.append(i[0].strip())
                else:
                    if type(i[0]) == list:

                        row.append(', '.join([', '.join(x) for x in i]))
                    else:
                        row.append(', '.join(i))

            csvWriter.writerow(row)

