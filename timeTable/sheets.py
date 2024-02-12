from flask import make_response
import gspread
from google.oauth2 import service_account
import pandas as pd
from timeTable.enums import googleSheet


def writeToGoogleSheets(data):
    worksheet = openSheet()
    df = pd.DataFrame([data])
    worksheet.append_rows(df.values.tolist())


def downloadCSV():
    try:
        sheet = openSheet()
        sheetData = sheet.get_all_values()
        df = pd.DataFrame(sheetData[1:], columns=sheetData[0])
        response = make_response(df.to_csv(index=False))
        response.headers["Content-Disposition"] = "attachment; filename=periodForm.csv"
        response.headers["Content-type"] = "text/csv"

        return response
    except FileNotFoundError:
        return "File not found", 404


def openSheet():
    sheetsAndGoogleCredentials = authorizeAndGetSheet()
    sheet = sheetsAndGoogleCredentials[
        googleSheet.SheetName.googleCredential.value
    ].open(sheetsAndGoogleCredentials[googleSheet.SheetName.spreadsheetTitle.name])

    worksheet = sheet.worksheet(
        sheetsAndGoogleCredentials[googleSheet.SheetName.worksheetTitle.name]
    )
    return worksheet


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
        googleSheet.SheetName.googleCredential.value: googleCredentials,
        googleSheet.SheetName.spreadsheetTitle.name: spreadsheetTitle,
        googleSheet.SheetName.worksheetTitle.name: worksheetTitle,
    }
