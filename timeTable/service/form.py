from flask import request
from timeTable.enums import classTable
from timeTable.database.fileQuery import query


def searchData():
    print(request.form)
    staffName = request.form.get(classTable.TimeTable.StaffName.value)
    roomNo = request.form.get(classTable.TimeTable.RoomNo.value)
    className = request.form.get(classTable.TimeTable.Class.value)
    day = request.form.get(classTable.TimeTable.Day.value)
    period = request.form.get(classTable.TimeTable.Period.value)
    result = query(day, period, staffName.strip(), roomNo, className)
    return result
