import pandas as pd
from timeTable.database.sheets import openSheet

def readSheetFromGoogle():
    return openSheet().get_all_records()


def convertSheetDataIntoDataframe(sheetValues):
    df = pd.DataFrame(sheetValues)
    return df
