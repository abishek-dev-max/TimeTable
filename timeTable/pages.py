import csv
from flask import Blueprint, render_template, request, make_response, redirect, url_for
import pandas as pd
import gspread
from google.oauth2 import service_account
from timeTable import fileQuery

bp = Blueprint("pages", __name__)


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
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = service_account.Credentials.from_service_account_file(
        "./timeTable/credentials.json", scopes=scopes
    )
    googleCredentials = gspread.authorize(credentials)
    spreadsheetTitle = "SRM_Time_Table"
    try:
        sheet = googleCredentials.open(spreadsheetTitle)
    except gspread.exceptions.SpreadsheetNotFound:
        sheet = googleCredentials.create(spreadsheetTitle)

    worksheetTitle = "Time_Table"
    worksheet = sheet.worksheet(worksheetTitle)

    df = pd.DataFrame([data])
    worksheet.append_rows(df.values.tolist())


@bp.route("/")
def home():
    return redirect(url_for("pages.createForm"))


@bp.route("/form", methods=["GET", "POST"])
def searchForm():
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

        return render_template("pages/searchForm.html", result=result)

    return render_template("pages/searchForm.html", result="Enter your Inputs")


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
        sheet = googleCredentials.open(spreadsheetTitle).worksheet(worksheetTitle)

        sheet_data = sheet.get_all_values()

        df = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])

        response = make_response(df.to_csv(index=False))
        response.headers["Content-Disposition"] = "attachment; filename=periodForm.csv"
        response.headers["Content-type"] = "text/csv"

        return response

    except FileNotFoundError:
        return "File not found", 404
