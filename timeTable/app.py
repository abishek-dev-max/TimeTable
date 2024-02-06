from flask import Flask
from timeTable.pages import bluePrintOfPages

app = Flask(__name__)
app.register_blueprint(bluePrintOfPages)

if __name__ == "__main__":
    app.run()
