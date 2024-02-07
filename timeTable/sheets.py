from flask import make_response
import gspread
from google.oauth2 import service_account
import pandas as pd
from timeTable.enums import googleSheet


def authorizeAndGetSheet():
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = service_account.Credentials.from_service_account_file(
        "./timeTable/credentials.json", scopes=scopes
    )
    googleCredentials = gspread.authorize(credentials)

    spreadsheetTitle = googleSheet.SheetName.spreadsheetTitle.value
    worksheetTitle = googleSheet.SheetName.worksheetTitle.value
    return {
        googleSheet.SheetName.GoogleCredential.value: googleCredentials,
        googleSheet.SheetName.spreadsheetTitle.name: spreadsheetTitle,
        googleSheet.SheetName.worksheetTitle.name: worksheetTitle,
    }


def getStaffNameByDepartment():
    sheetsAndGoogleCredentials = authorizeAndGetSheet()
    sheet = (
        sheetsAndGoogleCredentials[googleSheet.SheetName.GoogleCredential.value]
        .open(sheetsAndGoogleCredentials[googleSheet.SheetName.spreadsheetTitle.name])
        .worksheet(
            sheetsAndGoogleCredentials[googleSheet.SheetName.worksheetTitle.name]
        )
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


getStaffNameByDepartment()


def writeToGoogleDrive(data):
    sheetsAndGoogleCredentials = authorizeAndGetSheet()
    try:
        sheet = sheetsAndGoogleCredentials[
            googleSheet.SheetName.GoogleCredential.value
        ].open(sheetsAndGoogleCredentials[googleSheet.SheetName.spreadsheetTitle.name])
    except gspread.exceptions.SpreadsheetNotFound:
        sheet = sheetsAndGoogleCredentials[
            googleSheet.SheetName.GoogleCredential.value
        ].create(
            sheetsAndGoogleCredentials[googleSheet.SheetName.spreadsheetTitle.name]
        )

    worksheet = sheet.worksheet(
        sheetsAndGoogleCredentials[googleSheet.SheetName.worksheetTitle.name]
    )

    df = pd.DataFrame([data])
    worksheet.append_rows(df.values.tolist())


def download():
    try:
        sheetsAndGoogleCredentials = authorizeAndGetSheet()
        sheet = (
            sheetsAndGoogleCredentials[googleSheet.SheetName.GoogleCredential.value]
            .open(
                sheetsAndGoogleCredentials[googleSheet.SheetName.spreadsheetTitle.name]
            )
            .worksheet(
                sheetsAndGoogleCredentials[googleSheet.SheetName.worksheetTitle.name]
            )
        )

        sheet_data = sheet.get_all_values()
        df = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])

        response = make_response(df.to_csv(index=False))
        response.headers["Content-Disposition"] = "attachment; filename=periodForm.csv"
        response.headers["Content-type"] = "text/csv"

        return response

    except FileNotFoundError:
        return "File not found", 404
