import pandas as pd

def readFile(filePath, sheet_name=None):
    if filePath.endswith(".csv"):
        df = pd.read_csv(filePath)
    elif filePath.endswith(".xlsx"):
        df = pd.read_excel(filePath, sheet_name=sheet_name, header=2)
    else:
        raise ValueError(
            "Unsupported file format. Only CSV and Excel files are supported."
        )

    return df


timeTable = readFile("./data/Staff_TT.csv")
timeTable["Room No"] = timeTable["Room No"].fillna(0).astype(int)

def query(
    day,
    period,
    staffName=None,
    roomNo=None | int,
    className=None,
):
    query = timeTable.query("`Day` == @day and `Period` == @period")

    if staffName is not None:
        query = query[query["Staff Name"].str.contains(staffName, case=False, na=False)]
    if roomNo:
        query = query[query["Room No"] == roomNo]
    if className:
        query = query[query["Class"] == className]

    if not query.empty:
        result = query[["Staff Name", "Subject", "Room No", "Class"]].iloc[0].to_dict()
        return result
    else:
        return {"error": "No matching record found."}

