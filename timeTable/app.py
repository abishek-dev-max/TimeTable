from flask import Flask
from timeTable import pages

app = Flask(__name__)
app.register_blueprint(pages.bp)
    
if __name__ == "__main__":
    app.run()
