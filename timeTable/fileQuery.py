from timeTable.sheets import openSheet
from timeTable.prepareFileForQuery import readSheetFromGoogle, convertDatatypes

timeTable = readSheetFromGoogle()

convertDatatypes(timeTable)

sheet = openSheet()

timeTableData = sheet.get_all_records()


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
    else:
        result = {"error": "Free Period"}
    return result


def getStaffNameByDepartment():
    departmentToStaff = getRelationalItem("Department", "Staff Name", timeTableData)
    return departmentToStaff


def getClassNameByDepartment():
    departmentToClassName = getRelationalItem("Department", "Class", timeTableData)
    return departmentToClassName


def getDepartments():
    departments = list(set(entry["Department"] for entry in timeTableData))
    return departments


def getRelationalItem(fieldOne, fieldTwo, records):
    fieldOneToFieldtwoMapping = {}
    for record in records:
        fieldOneValue = record[fieldOne]
        fieldTwoValue = record[fieldTwo]
        if fieldOneValue in fieldOneToFieldtwoMapping:
            if fieldTwoValue not in fieldOneToFieldtwoMapping[fieldOneValue]:
                fieldOneToFieldtwoMapping[fieldOneValue].append(fieldTwoValue)
        else:
            fieldOneToFieldtwoMapping[fieldOneValue] = [fieldTwoValue]
    return fieldOneToFieldtwoMapping
