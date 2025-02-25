import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from timeTable.database.fileQuery import (
    query,
    getDepartments,
    getClassesByDepartment,
    getStaffByDepartment,
)
import pandas as pd
from timeTable.database.prepareFileForQuery import convertDatatypes 

def test_query():
    sample_result = query("Monday", "1")
    assert isinstance(sample_result, dict)


def test_get_staff_by_department():
    staff_map = getStaffByDepartment()
    assert isinstance(staff_map, dict)


def test_get_classes_by_department():
    class_map = getClassesByDepartment()
    assert isinstance(class_map, dict)


def test_get_departments():
    departments = getDepartments()
    assert isinstance(departments, list)


def test_convertDatatypes():
    # Sample test DataFrame
    data = {
        "Day Order": ["1", "2", "Three", None],
        "Period": ["10", "5", "Invalid", "3"],
        "Class Room": ["101", "202", "Invalid", None],
        "Subject": ["Math", "Science", "History", None],
        "Teacher": ["Alice", "Bob", None, "David"],
    }
    df = pd.DataFrame(data)

    # Convert data types
    result_df = convertDatatypes(df)

    # Expected numeric conversions
    assert pd.api.types.is_integer_dtype(
        result_df["Class Room"]
    ), "Class Room should be Int64"
    assert pd.api.types.is_numeric_dtype(result_df["Day Order"]), "Day Order should be numeric"
    assert pd.api.types.is_numeric_dtype(
        result_df["Period"]
    ), "Period should be numeric"

    # Expected NaN handling
    assert pd.isna(result_df.loc[3, "Class Room"]), "Class Room should be NaN"

    # Ensure non-numeric columns are strings
    assert result_df["Subject"].dtype == "object", "Subject should be string"
    assert result_df["Teacher"].dtype == "object", "Teacher should be string"


def test_empty_dataframe():
    df = pd.DataFrame(columns=["Day Order", "Period", "Class Room", "Subject"])
    result_df = convertDatatypes(df)

    assert result_df.empty, "Empty DataFrame should remain empty"


def test_unexpected_data():
    df = pd.DataFrame(
        {
            "Day Order": [None, "A", 5.5],
            "Period": [None, "B", "3"],
            "Class Room": [None, "C", 200],
        }
    )
    result_df = convertDatatypes(df)

    assert pd.isna(result_df.loc[0, "Day Order"]), "Should handle None correctly"
    assert pd.isna(
        result_df.loc[1, "Period"]
    ), "Invalid numeric values should become NaN"
    assert (
        result_df["Class Room"].dtype.name == "Int64"
    ), "Class Room should be converted to Int64"
