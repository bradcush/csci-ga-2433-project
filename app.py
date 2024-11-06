from flask import Flask
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def homepage():
    return datetime.now().strftime("%A, %d %b %Y %l:%M %p")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
