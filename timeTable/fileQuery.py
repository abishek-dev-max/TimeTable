import pandas as pd
import gspread
from google.oauth2 import service_account


def readSheetFromGoogle():
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = service_account.Credentials.from_service_account_file(
        "./timeTable/credentials.json", scopes=scopes
    )
    googleCredentials = gspread.authorize(credentials)
    spreadsheetTitle = "SRM_Time_Table"
    try:
        sheet = googleCredentials.open(spreadsheetTitle)
    except gspread.exceptions.SpreadsheetNotFound:
        sheet = googleCredentials.create(spreadsheetTitle)

    worksheetTitle = "Time_Table"
    try:
        sheet = googleCredentials.open(spreadsheetTitle)
        worksheet = sheet.worksheet(worksheetTitle)
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
    roomNo=None | int,
    className=None,
):
    query = timeTable.query("`Day` == @day and `Period` == @period")

    if staffName is not None:
        query = query[query["Staff Name"].str.contains(staffName, case=False, na=False)]
    if roomNo:
        query = query[query["Room No"].astype(str) == str(roomNo)]
    if className:
        query = query[query["Class"] == className]

    if not query.empty:
        result = (
            query[
                [
                    "Staff ID",
                    "Staff Name",
                    "Registration No",
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


result = query(day=1, period=1, staffName="John Doe", roomNo=101, className="II CS A")
