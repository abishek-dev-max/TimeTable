from flask import Blueprint, render_template, request, redirect, url_for,session
from timeTable.sheets import getStaffNameByDepartment, download
from timeTable.form import submitForm, searchData

bluePrintOfPages = Blueprint("pages", __name__)


@bluePrintOfPages.route("/")
def home():
    return redirect(url_for("pages.searchForm"))


@bluePrintOfPages.route("/form", methods=["GET", "POST"])
def searchForm():
    staffAndDepartmentData = getStaffNameByDepartment()
    departments = staffAndDepartmentData["departments"]
    staffNames = staffAndDepartmentData["staffNames"]
    departmentToStaff = staffAndDepartmentData["departmentToStaff"]
    result = None

    if request.method == "POST":
        result = searchData()
        return render_template(
            "pages/searchForm.html",
            result=result,
            departments=departments,
            staffNames=staffNames,
            departmentToStaff=departmentToStaff,
        )
    return render_template(
        "pages/searchForm.html",
        result=result,
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
    download()
