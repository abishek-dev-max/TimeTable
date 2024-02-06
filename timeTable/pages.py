from flask import Blueprint, render_template, request, make_response, redirect, url_for
import pandas as pd
from timeTable.sheets import (
    authorizeAndGetSheet,
    getStaffNameByDepartment,
)
from timeTable.form import submitForm, searchQuery

bluePrintOfPages = Blueprint("pages", __name__)


@bluePrintOfPages.route("/")
def home():
    return redirect(url_for("pages.createForm"))


@bluePrintOfPages.route("/form", methods=["GET", "POST"])
def searchForm():
    staffAndDepartmentData = getStaffNameByDepartment()
    departments = staffAndDepartmentData["departments"]
    staffNames = staffAndDepartmentData["staffNames"]
    departmentToStaff = staffAndDepartmentData["departmentToStaff"]
    if request.method == "POST":
        result=searchQuery(request.form)
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


@bluePrintOfPages.route("/create")
def createForm():
    return render_template("pages/createForm.html")


@bluePrintOfPages.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        submitForm()
        return render_template("pages/successPage.html")
    else:
        return render_template("404.html"), 404


@bluePrintOfPages.route("/download")
def download():
    try:
        sheetsAndGoogleCredentials = authorizeAndGetSheet()
        sheet = (
            sheetsAndGoogleCredentials["googleCredentials"]
            .open(sheetsAndGoogleCredentials["spreadsheetTitle"])
            .worksheet(sheetsAndGoogleCredentials["worksheetTitle"])
        )

        sheet_data = sheet.get_all_values()
        df = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])

        response = make_response(df.to_csv(index=False))
        response.headers["Content-Disposition"] = "attachment; filename=periodForm.csv"
        response.headers["Content-type"] = "text/csv"

        return response

    except FileNotFoundError:
        return "File not found", 404
