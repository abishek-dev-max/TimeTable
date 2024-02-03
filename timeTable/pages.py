import csv
from flask import Blueprint, render_template, request, make_response,redirect,url_for
import pandas as pd
from query import fileQuery

bp = Blueprint("pages", __name__)


def submitForm():
    staffId = request.form["staffID"]
    staffName = request.form["staffName"]
    regNo = request.form["registrationNo"]
    department = request.form["department"]
    subject = request.form["subject"]
    roomNo = request.form["roomNo"]
    day = request.form["day"]
    period = request.form["period"]
    form_data = {
        "Staff ID": staffId,
        "Staff Name": staffName,
        "Registration No": regNo,
        "Department": department,
        "Subject": subject,
        "Room No": roomNo,
        "Day": day,
        "Period": period,
    }
    writeCsv(form_data)

def writeCsv(data):
    csv_file_path = "form_data.csv"

    with open(csv_file_path, "a", newline="") as csvfile:
        field_names = [
            "Staff ID",
            "Staff Name",
            "Registration No",
            "Department",
            "Subject",
            "Room No",
            "Day",
            "Period",
        ]

        writer = csv.DictWriter(csvfile, fieldnames=field_names)

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(data)

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
        file_path = "form_data.csv"

        csv_data = pd.read_csv(file_path)

        response = make_response(csv_data.to_csv(index=False))

        response.headers["Content-Disposition"] = "attachment; filename=form_data.csv"
        response.headers["Content-type"] = "text/csv"

        return response
    except FileNotFoundError:
        return "File not found", 404
