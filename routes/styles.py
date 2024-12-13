from app import app
from flask import send_file


@app.route("/styles.css")
def style():
    """
    Only CSS is static
    """
    return send_file("routes/styles.css")
