import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import patch
from flask import Flask, request
from timeTable.service.form import searchData

# Ensure the correct module path is set

# Create a Flask app for testing
app = Flask(__name__)


# Mock dependencies
class MockClassTable:
    class TimeTable:
        StaffName = type("Enum", (), {"value": "staffName"})
        RoomNo = type("Enum", (), {"value": "roomNo"})
        Class = type("Enum", (), {"value": "className"})
        Day = type("Enum", (), {"value": "day"})
        Period = type("Enum", (), {"value": "period"})


classTable = MockClassTable()


@pytest.fixture
def mock_request_form():
    """Fixture to mock request.form.get calls within a Flask test request context."""
    with app.test_request_context(
        method="POST",
        data={
            "staffName": "John Doe",
            "roomNo": "101",
            "className": "Math",
            "day": "1",
            "period": "2",
        },
    ):
        yield request


@pytest.fixture
def mock_query():
    """Fixture to mock query function"""
    with patch(
        "timeTable.database.fileQuery.query", return_value="Mocked Query Result"
    ) as mock_query:
        yield mock_query


def test_search_data(mock_request_form, mock_query):
    """Test searchData function with valid inputs"""
    result = searchData()
    mock_query.assert_called_once_with(1, 2, "John Doe", 101, "Math")
    assert result == "Mocked Query Result"


def test_search_data_missing_room_no(mock_query):
    """Test searchData function when room number is missing (should default to 0)"""
    with app.test_request_context(
        method="POST",
        data={
            "staffName": "Jane Doe",
            "roomNo": None,  # Simulating missing room number
            "className": "Science",
            "day": "2",
            "period": "3",
        },
    ):
        result = searchData()

    mock_query.assert_called_once_with(2, 3, "Jane Doe", 0, "Science")
    assert result == "Mocked Query Result"
