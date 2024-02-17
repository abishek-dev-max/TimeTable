# form.py


# def submitForm():
#     staffId = request.form[timeTable.TimeTable.StaffId.value]
#     staffName = request.form[timeTable.TimeTable.StaffName.value]
#     department = request.form[timeTable.TimeTable.Department.value]
#     subject = request.form[timeTable.TimeTable.Subject.value]
#     roomNo = request.form[timeTable.TimeTable.RoomNo.value]
#     day = request.form[timeTable.TimeTable.Day.value]
#     period = request.form[timeTable.TimeTable.Period.value]
#     className = request.form[timeTable.TimeTable.ClassName.value]
#     periodForm = {
#         "Staff ID": staffId,
#         "Staff Name": staffName,
#         "Department": department,
#         "Subject": subject,
#         "Room No": roomNo,
#         "Day": day,
#         "Period": period,
#         "Class": className,
#     }
#     writeToGoogleSheets(periodForm)


# pages.py


# @bluePrintOfPages.route("/create")
# def createForm():
#     return render_template("pages/createForm.html")


# @bluePrintOfPages.route("/submit", methods=["POST"])
# def submit():
#     if request.method == "POST":
#         submitForm()
#         return render_template("pages/successPage.html")
#     else:
#         return 404


# @bluePrintOfPages.route("/download")
# def download():
#     return downloadCSV()


# sheets.py


# def writeToGoogleSheets(data):
#     worksheet = openSheet()
#     df = pd.DataFrame([data])
#     worksheet.append_rows(df.values.tolist())


# def downloadCSV():
#     try:
#         sheet = openSheet()
#         sheetData = sheet.get_all_values()
#         df = pd.DataFrame(sheetData[1:], columns=sheetData[0])
#         response = make_response(df.to_csv(index=False))
#         response.headers["Content-Disposition"] = "attachment; filename=periodForm.csv"
#         response.headers["Content-type"] = "text/csv"

#         return response
#     except FileNotFoundError:
#         return "File not found", 404
