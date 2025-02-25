import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from unittest.mock import patch, MagicMock
from timeTable.database.sheets import openSheet, authorizeAndGetSheet
from timeTable.enums import googleSheet
from google.oauth2 import service_account
import gspread 


# Mocking the gspread and Google authentication functions
@pytest.fixture
def mock_authorize_and_get_sheet():
    with patch("timeTable.database.sheets.authorize") as mock_authorize, patch(
        "timeTable.database.sheets.service_account.Credentials.from_service_account_file"
    ) as mock_credentials:
        mock_credentials.return_value = MagicMock()
        mock_client = MagicMock(spec=gspread.Client)
        mock_authorize.return_value = mock_client

        mock_client.open.return_value = MagicMock()
        mock_client.open.return_value.worksheet.return_value = MagicMock()

        return {
            googleSheet.SheetName.googleCredential.value: mock_client,
            googleSheet.SheetName.spreadsheetTitle.name: googleSheet.SheetName.spreadsheetTitle.value,
            googleSheet.SheetName.worksheetTitle.name: googleSheet.SheetName.worksheetTitle.value,
        }


@patch("timeTable.database.sheets.authorizeAndGetSheet")
def test_open_sheet(mock_authorize_get_sheet, mock_authorize_and_get_sheet):
    mock_authorize_get_sheet.return_value = mock_authorize_and_get_sheet
    worksheet = openSheet()

    assert worksheet is not None
    assert mock_authorize_get_sheet.called
    assert mock_authorize_get_sheet.return_value[
        googleSheet.SheetName.googleCredential.value
    ].open.called
    assert mock_authorize_get_sheet.return_value[
        googleSheet.SheetName.googleCredential.value
    ].open.return_value.worksheet.called


@patch(
    "timeTable.database.sheets.service_account.Credentials.from_service_account_file"
)
@patch("timeTable.database.sheets.authorize")
def test_authorize_and_get_sheet(mock_authorize, mock_credentials):
    mock_credentials.return_value = MagicMock()
    mock_client = MagicMock(spec=gspread.Client)
    mock_authorize.return_value = mock_client

    result = authorizeAndGetSheet()

    assert googleSheet.SheetName.googleCredential.value in result
    assert googleSheet.SheetName.spreadsheetTitle.name in result
    assert googleSheet.SheetName.worksheetTitle.name in result
    assert result[googleSheet.SheetName.googleCredential.value] is mock_client
    assert mock_authorize.called
    assert mock_credentials.called
