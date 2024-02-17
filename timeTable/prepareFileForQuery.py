import pandas as pd
from timeTable.sheets import openSheet


def readSheetFromGoogle():
    worksheet = openSheet()
    values = worksheet.get_all_values()
    df = pd.DataFrame(values[1:], columns=values[0])
    return df


def convertDatatypes(csvFile):
    numeric_columns = ["Day", "Period"] 
    csvFile[numeric_columns] = csvFile[numeric_columns].apply(
        pd.to_numeric, errors="coerce"
    )

    csvFile["Room No"] = pd.to_numeric(csvFile["Room No"], errors="coerce").astype(
        "Int64"
    )

    string_columns = csvFile.columns.difference(numeric_columns + ["Room No"])
    csvFile[string_columns] = csvFile[string_columns].astype(str)
