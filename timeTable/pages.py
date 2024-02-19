from flask import Blueprint, render_template, request, redirect, url_for, session
from timeTable.form import searchData
from timeTable.fileQuery import (
    getStaffNameByDepartment,
    getDepartments,
    getClassNameByDepartment,
)

bluePrintOfPages = Blueprint("pages", __name__)


@bluePrintOfPages.route("/")
def home():
    return redirect(url_for("pages.searchForm"))


@bluePrintOfPages.route("/form", methods=["GET", "POST"])
def searchForm():
    staffAndDepartmentMapper = getStaffNameByDepartment()
    classNameAndDepartmentMapper = getClassNameByDepartment()
    departments = getDepartments()

    if request.method == "POST":
        result = searchData()
        session["searchResult"] = result
        return redirect(url_for(".searchForm"))

    result = session.pop("searchResult", None)

    return render_template(
        "pages/searchForm.html",
        result=result,
        departments=departments,
        departmentToStaff=staffAndDepartmentMapper,
        departmentToClassName=classNameAndDepartmentMapper,
    )
