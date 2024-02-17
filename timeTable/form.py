from flask import request
from timeTable.enums import timeTable
from timeTable.fileQuery import query

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
