import pandas as pd
import gspread
from timeTable.sheets import authorizeAndGetSheet
from timeTable.enums import googleSheet

def readSheetFromGoogle():
    sheetsAndGoogleCredentials = authorizeAndGetSheet()
    try:
        sheet = sheetsAndGoogleCredentials[googleSheet.SheetName.GoogleCredential.value].open(
            sheetsAndGoogleCredentials[googleSheet.SheetName.spreadsheetTitle.name]
        )
        worksheet = sheet.worksheet(
            sheetsAndGoogleCredentials[googleSheet.SheetName.worksheetTitle.name]
        )
        values = worksheet.get_all_values()
        df = pd.DataFrame(values[1:], columns=values[0])
        return df
    except gspread.exceptions.SpreadsheetNotFound:
        raise FileNotFoundError("Google Sheet not found.")


def convertDatatypes():
    numeric_columns = ["Room No", "Day", "Period"]
    timeTable[numeric_columns] = timeTable[numeric_columns].apply(
        pd.to_numeric, errors="coerce"
    )
    string_columns = timeTable.columns.difference(numeric_columns)
    timeTable[string_columns] = timeTable[string_columns].astype(str)


timeTable = readSheetFromGoogle()
convertDatatypes()


def query(
    day,
    period,
    staffName=None,
    roomNo=None,
    className=None,
):
    query = timeTable.query("Day == @day and Period == @period")

    if staffName is not None:
        query = query[query["Staff Name"].str.contains(staffName, case=False, na=False)]
    if roomNo:
        query = query[query["Room No"] == roomNo]
    if className:
        query = query[query["Class"] == className]

    if not query.empty:
        result = (
            query[
                [
                    "Staff ID",
                    "Staff Name",
                    "Department",
                    "Subject",
                    "Room No",
                    "Class",
                    "Day",
                    "Period",
                ]
            ]
            .iloc[0]
            .to_dict()
        )
        return result
    else:
        return {"error": "No matching record found."}
