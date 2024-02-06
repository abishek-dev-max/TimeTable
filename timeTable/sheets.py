import gspread
from google.oauth2 import service_account
import pandas as pd


def authorizeAndGetSheet():
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = service_account.Credentials.from_service_account_file(
        "./timeTable/credentials.json", scopes=scopes
    )
    googleCredentials = gspread.authorize(credentials)

    spreadsheetTitle = "SRM_Time_Table"
    worksheetTitle = "Time_Table"
    return {
        "googleCredentials": googleCredentials,
        "spreadsheetTitle": spreadsheetTitle,
        "worksheetTitle": worksheetTitle,
    }


def getStaffNameByDepartment():
    sheetsAndGoogleCredentials = authorizeAndGetSheet()
    sheet = (
        sheetsAndGoogleCredentials["googleCredentials"]
        .open(sheetsAndGoogleCredentials["spreadsheetTitle"])
        .worksheet(sheetsAndGoogleCredentials["worksheetTitle"])
    )
    if sheet:
        data = sheet.get_all_records()
        departmentToStaff = {}

        for entry in data:
            department = entry["Department"]
            staff_name = entry["Staff Name"]

            if department in departmentToStaff:
                departmentToStaff[department].append(staff_name)
            else:
                departmentToStaff[department] = [staff_name]

        departments = list(set(entry["Department"] for entry in data))
        staffNames = list(set(entry["Staff Name"] for entry in data))

        return {
            "departments": departments,
            "staffNames": staffNames,
            "departmentToStaff": departmentToStaff,
        }
    else:
        return "Error accessing Google Sheets", 500


def writeToGoogleDrive(data):
    sheetsAndGoogleCredentials = authorizeAndGetSheet()
    try:
        sheet = sheetsAndGoogleCredentials["googleCredentials"].open(
            sheetsAndGoogleCredentials["spreadsheetTitle"]
        )
    except gspread.exceptions.SpreadsheetNotFound:
        sheet = sheetsAndGoogleCredentials["googleCredentials"].create(
            sheetsAndGoogleCredentials["spreadsheetTitle"]
        )

    worksheet = sheet.worksheet(sheetsAndGoogleCredentials["worksheetTitle"])

    df = pd.DataFrame([data])
    worksheet.append_rows(df.values.tolist())
