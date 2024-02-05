import csv
from flask import Blueprint, render_template, request, make_response, redirect, url_for, jsonify
import pandas as pd
import gspread
from google.oauth2 import service_account
from timeTable import fileQuery

bp = Blueprint("pages", __name__)


def authorizeAndGetSheet():
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = service_account.Credentials.from_service_account_file(
        "./timeTable/credentials.json", scopes=scopes
    )
    googleCredentials = gspread.authorize(credentials)

    spreadsheetTitle = "SRM_Time_Table"
    worksheetTitle = "Time_Table"
    return {
        "googleCredentials": googleCredentials,
        "spreadsheetTitle": spreadsheetTitle,
        "worksheetTitle": worksheetTitle,
    }


def getStaffNameByDepartment():
    sheetsAndGoogleCredentials = authorizeAndGetSheet()
    sheet = (
        sheetsAndGoogleCredentials["googleCredentials"]
        .open(sheetsAndGoogleCredentials["spreadsheetTitle"])
        .worksheet(sheetsAndGoogleCredentials["worksheetTitle"])
    )
    if sheet:
        data = sheet.get_all_records()
        departmentToStaff = {}

        for entry in data:
            department = entry["Department"]
            staff_name = entry["Staff Name"]

            if department in departmentToStaff:
                departmentToStaff[department].append(staff_name)
            else:
                departmentToStaff[department] = [staff_name]

        departments = list(set(entry["Department"] for entry in data))
        staffNames = list(set(entry["Staff Name"] for entry in data))

        return {
            "departments": departments,
            "staffNames": staffNames,
            "departmentToStaff": departmentToStaff,
        }
    else:
        return "Error accessing Google Sheets", 500


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


def writeToGoogleDrive(data):
    sheetsAndGoogleCredentials = authorizeAndGetSheet()
    try:
        sheet = sheetsAndGoogleCredentials["googleCredentials"].open(
            sheetsAndGoogleCredentials["spreadsheetTitle"]
        )
    except gspread.exceptions.SpreadsheetNotFound:
        sheet = sheetsAndGoogleCredentials["googleCredentials"].create(
            sheetsAndGoogleCredentials["spreadsheetTitle"]
        )

    worksheet = sheet.worksheet(sheetsAndGoogleCredentials["worksheetTitle"])

    df = pd.DataFrame([data])
    worksheet.append_rows(df.values.tolist())


@bp.route("/")
def home():
    return redirect(url_for("pages.createForm"))


@bp.route("/form", methods=["GET", "POST"])
def searchForm():
    staffAndDepartmentData = getStaffNameByDepartment()
    departments = staffAndDepartmentData["departments"]
    staffNames = staffAndDepartmentData["staffNames"]
    departmentToStaff = staffAndDepartmentData["departmentToStaff"]
    if request.method == "POST":
        staffName = request.form["staffName"]
        roomNo = request.form["roomNo"]
        className = request.form["class"]
        day = request.form["day"]
        period = request.form["period"]

        if roomNo:
            roomNo = int(roomNo)
        else:
            roomNo = 0
        result = fileQuery.query(int(day), int(period), staffName, roomNo, className)

        return render_template(
            "pages/searchForm.html",
            result=result,
            departments=departments,
            staffNames=staffNames,
            departmentToStaff=departmentToStaff,
        )

    return render_template(
        "pages/searchForm.html",
        result="Enter your Inputs",
        departments=departments,
        staffNames=staffNames,
        departmentToStaff=departmentToStaff,
    )


@bp.route("/create")
def createForm():
    return render_template("pages/createForm.html")


@bp.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        submitForm()
        return render_template("pages/successPage.html")
    else:
        return render_template("404.html"), 404


@bp.route("/download")
def download():
    try:
        sheetsAndGoogleCredentials = authorizeAndGetSheet()
        sheet = (
            sheetsAndGoogleCredentials["googleCredentials"]
            .open(sheetsAndGoogleCredentials["spreadsheetTitle"])
            .worksheet(sheetsAndGoogleCredentials["worksheetTitle"])
        )

        sheet_data = sheet.get_all_values()
        print(sheet_data)
        df = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])

        response = make_response(df.to_csv(index=False))
        response.headers["Content-Disposition"] = "attachment; filename=periodForm.csv"
        response.headers["Content-type"] = "text/csv"

        return response

    except FileNotFoundError:
        return "File not found", 404
