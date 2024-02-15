import pandas as pd
from timeTable.sheets import openSheet


def readSheetFromGoogle():
    worksheet = openSheet()
    values = worksheet.get_all_values()
    df = pd.DataFrame(values[1:], columns=values[0])
    return df


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
    roomNo=None,
    className=None,
):
    querySubject = timeTable.query("Day == @day and Period == @period")

    if staffName is not None and staffName != "":
        querySubject = querySubject[querySubject["Staff Name"].str.contains(staffName, case=False, na=False)]
    if roomNo:
        querySubject = querySubject[querySubject["Room No"] == roomNo]
    if className:
        querySubject = querySubject[querySubject["Class"] == className]

    if not querySubject.empty:
        result = (
            querySubject[
                [
                    "Staff ID",
                    "Staff Name",
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


def getStaffNameByDepartment():
    sheet = openSheet() 
    if sheet:
        data = sheet.get_all_records()
        departmentToStaff = {}

        for entry in data:
            department = entry["Department"]
            staffName = entry["Staff Name"]

            if department in departmentToStaff:
                if staffName not in departmentToStaff[department]:
                    departmentToStaff[department].append(staffName)
            else:
                departmentToStaff[department] = [staffName]

        departments = list(set(entry["Department"] for entry in data))
        staffNames = list(set(entry["Staff Name"] for entry in data))
        return {
            "departments": departments,
            "staffNames": staffNames,
            "departmentToStaff": departmentToStaff,            
        }
    else:
        return "Error accessing Google Sheets", 500
