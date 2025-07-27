from timeTable.database.prepareFileForQuery import (
    readSheetFromGoogle,
    convertSheetDataIntoDataframe,
)


def initializeTimeTable():
    """Loads and preprocesses the timetable data."""
    sheet_data = readSheetFromGoogle()
    df = convertSheetDataIntoDataframe(sheet_data)
    return df, sheet_data


timeTable, timeTableSheet = initializeTimeTable()


def query(
    day_order: str,
    period: str,
    staff_name: str = None,
    class_room: str = None,
    class_name: str = None,
) -> dict:
    querySubject = timeTable.loc[
        (timeTable["Day Order"] == int(day_order))
        & (timeTable["Period"] == str(period).strip())
    ]

    if staff_name:
        # Strip whitespace and perform a case-insensitive match
        querySubject = querySubject[
            querySubject["Staff Name"]
            .str.contains(staff_name, case=False, na=False)
        ]

    if class_room:
        querySubject = querySubject[
            querySubject["Class Room"].str.strip() == class_room.strip()
        ]

    if class_name:
        querySubject = querySubject[
            querySubject["Class"].str.strip() == class_name.strip()
        ]
    # If no results, return an error message
    if not querySubject.empty:
        return querySubject.iloc[0][
            [
                "Staff ID",
                "Staff Name",
                "Department",
                "Subject",
                "Class Room",
                "Class",
                "Day Order",
                "Period",
            ]
        ].to_dict()

    return {"error": "Free Period"}


def getRelationalMapping(field_one: str, field_two: str, records: list) -> dict:
    mapping = {}
    for record in records:
        key, value = record[field_one], record[field_two]
        (
            mapping.setdefault(key, []).append(value)
            if value not in mapping.get(key, [])
            else None
        )
    return mapping


def getStaffByDepartment() -> dict:
    return getRelationalMapping("Department", "Staff Name", timeTableSheet)


def getClassesByDepartment() -> dict:
    return getRelationalMapping("Department", "Class", timeTableSheet)


def getDepartments() -> list:
    return sorted({entry["Department"] for entry in timeTableSheet})
