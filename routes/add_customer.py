from app import app
from flask import request
from routes.helpers import html
import psycopg2
import os

DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL, sslmode="require")

GENERIC_ERROR = "An error ocurred"


@app.route("/add-customer")
def add_customer():
    """
    Add customer
    """
    # Actually add the customer
    name = request.args.get("name")
    email = request.args.get("email")
    phone = request.args.get("phone")
    with conn.cursor() as cur:
        if name and email and phone:
            # We allow two customers with the same details
            # but different automatically incremented ids
            try:
                cur.execute(
                    """
                    INSERT INTO customer (name, email, phone)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        name,
                        email,
                        phone,
                    ),
                )
                conn.commit()
            except Exception:
                return GENERIC_ERROR
        cur.execute(
            """
            SELECT id, name, email, phone
            FROM customer
            """
        )
        records = ""
        for record in cur:
            records += f"""
            <tr>
                <td>{record[0]}</td>
                <td>{record[1]}</td>
                <td>{record[2]}</td>
                <td>{record[3]}</td>
            </tr>
            """
        return html(
            "Add customer",
            f"""
            <table border="1">
                <thead>
                    <tr>
                        <th>id</th>
                        <th>name</th>
                        <th>email</th>
                        <th>phone</th>
                    </tr>
                </head>
                <tbody>
                    {records}
                </tbody>
            </table>
            """,
        )
