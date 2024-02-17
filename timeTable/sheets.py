from gspread import authorize
from google.oauth2 import service_account
from timeTable.enums import googleSheet

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
    googleCredentials = authorize(credentials)

    spreadsheetTitle = googleSheet.SheetName.spreadsheetTitle.value
    worksheetTitle = googleSheet.SheetName.worksheetTitle.value
    return {
        googleSheet.SheetName.googleCredential.value: googleCredentials,
        googleSheet.SheetName.spreadsheetTitle.name: spreadsheetTitle,
        googleSheet.SheetName.worksheetTitle.name: worksheetTitle,
    }
