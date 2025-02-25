import pandas as pd
from timeTable.database.sheets import openSheet

def readSheetFromGoogle():
    return openSheet().get_all_records()


def convertSheetDataIntoDataframe(sheetValues):
    return pd.DataFrame(sheetValues[1:], columns=sheetValues[0])
