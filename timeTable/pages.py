from flask import Blueprint, render_template, request, redirect, url_for, session
from timeTable.form import searchData
from timeTable.fileQuery import getStaffNameByDepartment,getStaffNamesAndDepartments

bluePrintOfPages = Blueprint("pages", __name__)


@bluePrintOfPages.route("/")
def home():
    return redirect(url_for("pages.searchForm"))


@bluePrintOfPages.route("/form", methods=["GET", "POST"])
def searchForm():
    staffAndDepartmentMapper = getStaffNameByDepartment()
    staffNamesAndDepartments = getStaffNamesAndDepartments()
    departments = staffNamesAndDepartments["departments"]
    staffNames = staffNamesAndDepartments["staffNames"]

    if request.method == "POST":
        result = searchData()
        session["search_result"] = result
        return redirect(url_for(".searchForm"))

    result = session.pop("search_result", None)

    return render_template(
        "pages/searchForm.html",
        result=result,
        departments=departments,
        staffNames=staffNames,
        departmentToStaff=staffAndDepartmentMapper,
    )