from flask import Flask
from timeTable.pages import bluePrintOfPages
from timeTable.config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(bluePrintOfPages)

if __name__ == "__main__":
    app.run()
