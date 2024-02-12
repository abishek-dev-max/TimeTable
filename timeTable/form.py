from flask import request
from timeTable.enums import timeTable
from timeTable.sheets import writeToGoogleSheets
from timeTable.fileQuery import query


def submitForm():
    staffId = request.form[timeTable.TimeTable.StaffId.value]
    staffName = request.form[timeTable.TimeTable.StaffName.value]
    department = request.form[timeTable.TimeTable.Department.value]
    subject = request.form[timeTable.TimeTable.Subject.value]
    roomNo = request.form[timeTable.TimeTable.RoomNo.value]
    day = request.form[timeTable.TimeTable.Day.value]
    period = request.form[timeTable.TimeTable.Period.value]
    className = request.form[timeTable.TimeTable.ClassName.value]
    periodForm = {
        "Staff ID": staffId,
        "Staff Name": staffName,
        "Department": department,
        "Subject": subject,
        "Room No": roomNo,
        "Day": day,
        "Period": period,
        "Class": className,
    }
    writeToGoogleSheets(periodForm)


def searchData():
    staffName = request.form.get(timeTable.TimeTable.StaffName.value)
    roomNo = request.form.get(timeTable.TimeTable.RoomNo.value)
    className = request.form.get(timeTable.TimeTable.ClassName.value)
    day = request.form.get(timeTable.TimeTable.Day.value)
    period = request.form.get(timeTable.TimeTable.Period.value)

    if roomNo:
        roomNo = int(roomNo)
    else:
        roomNo = 0
    result = query(int(day), int(period), staffName, roomNo, className)
    return result
