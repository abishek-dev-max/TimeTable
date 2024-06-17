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
    return {
        googleSheet.SheetName.googleCredential.value:  authorize(credentials),
        googleSheet.SheetName.spreadsheetTitle.name: googleSheet.SheetName.spreadsheetTitle.value,
        googleSheet.SheetName.worksheetTitle.name: googleSheet.SheetName.worksheetTitle.value,
    }
