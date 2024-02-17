import pandas as pd
from timeTable.sheets import openSheet


def readSheetFromGoogle():
    worksheet = openSheet()
    values = worksheet.get_all_values()
    df = pd.DataFrame(values[1:], columns=values[0])
    return df


def convertDatatypes(csvFile):
    numeric_columns = ["Room No", "Day", "Period"]
    csvFile[numeric_columns] = csvFile[numeric_columns].apply(
        pd.to_numeric, errors="coerce"
    )
    string_columns = csvFile.columns.difference(numeric_columns)
    csvFile[string_columns] = csvFile[string_columns].astype(str)
