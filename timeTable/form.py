from flask import request
from timeTable.sheets import writeToGoogleDrive
from timeTable.fileQuery import query


def submitForm():
    staffId = request.form["staffID"]
    staffName = request.form["staffName"]
    department = request.form["department"]
    subject = request.form["subject"]
    roomNo = request.form["roomNo"]
    day = request.form["day"]
    period = request.form["period"]
    className = request.form["class"]
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
    writeToGoogleDrive(periodForm)

def searchData():
    staffName = request.form.get('staffName')
    roomNo = request.form.get('roomNo')
    className = request.form.get('class')  
    day = request.form.get('day')
    period = request.form.get('period')

    if roomNo:
        roomNo = int(roomNo)
    else:
        roomNo = 0
    result = query(int(day), int(period), staffName, roomNo, className)
    return result
