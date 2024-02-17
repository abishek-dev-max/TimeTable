from timeTable.sheets import openSheet
from timeTable.prepareFileForQuery import readSheetFromGoogle, convertDatatypes

timeTable = readSheetFromGoogle()
convertDatatypes(timeTable)


def query(
    day,
    period,
    staffName=None,
    roomNo=None,
    className=None,
):
    querySubject = timeTable.query("Day == @day and Period == @period")

    if staffName is not None and staffName != "":
        querySubject = querySubject[
            querySubject["Staff Name"].str.contains(staffName, case=False, na=False)
        ]
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
        departmentToStaff = getRelationalItem("Department", "Staff Name", data)
        return departmentToStaff
    else:
        return "Error accessing Google Sheets", 500


def getClassNameByDepartment():
    sheet = openSheet()
    if sheet:
        data = sheet.get_all_records()
        departmentToClassName = getRelationalItem("Department", "Class", data)
        return {
            "departmentToClassName": departmentToClassName,
        }
    else:
        return "Error accessing Google Sheets", 500


def getStaffNamesAndDepartments():
    sheet = openSheet()
    if sheet:
        data = sheet.get_all_records()
        departments = list(set(entry["Department"] for entry in data))
        staffNames = list(set(entry["Staff Name"] for entry in data))
        return {"departments": departments, "staffNames": staffNames}


def getRelationalItem(fieldOne, fieldTwo, data):
    mapperOfTwoFields = {}
    for entry in data:
        inDependentField = entry[fieldOne]
        dependentField = entry[fieldTwo]
        if inDependentField in mapperOfTwoFields:
            if dependentField not in mapperOfTwoFields[inDependentField]:
                mapperOfTwoFields[inDependentField].append(dependentField)
        else:
            mapperOfTwoFields[inDependentField] = [dependentField]
    return mapperOfTwoFields
