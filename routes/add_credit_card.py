from app import app
from flask import request
from routes.helpers import html
import psycopg2
import os

DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL, sslmode="require")

GENERIC_ERROR = "An error ocurred"


@app.route("/add-credit-card")
def add_credit_card():
    """
    Add credit card
    """
    # Actually add the credit card
    fname = request.args.get("fname")
    minit = request.args.get("minit")
    lname = request.args.get("lname")
    number = request.args.get("number")
    expiration_date = request.args.get("expiration_date")
    security_code = request.args.get("security_code")
    zip_code = request.args.get("zip_code")
    id_customer = request.args.get("id_customer")
    with conn.cursor() as cur:
        # All arguments are required
        params = [
            fname,
            minit,
            lname,
            number,
            expiration_date,
            security_code,
            zip_code,
            id_customer,
        ]
        if not any((x == "" or x is None) for x in params):
            cur.execute(
                """
                SELECT id
                FROM customer as c
                WHERE c.id = %s
                """,
                (id_customer,),
            )
            if cur.fetchone() is None:
                return "customer_id doesn't exist"
            cur.execute(
                """
                INSERT INTO credit_card (fname, minit, lname, number, expiration_date, security_code, zip_code, id_customer)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    fname,
                    minit,
                    lname,
                    number,
                    expiration_date,
                    security_code,
                    zip_code,
                    id_customer,
                ),
            )
            conn.commit()
        cur.execute(
            """
            SELECT fname, minit, lname, number, expiration_date, security_code, zip_code, id_customer
            FROM credit_card
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
                <td>{record[4]}</td>
                <td>{record[5]}</td>
                <td>{record[6]}</td>
                <td>{record[7]}</td>
            </tr>
            """
        return html(
            "Add credit card",
            f"""
            <table border="1">
                <thead>
                    <tr>
                        <th>fname</th>
                        <th>minit</th>
                        <th>lname</th>
                        <th>number</th>
                        <th>expiration_date</th>
                        <th>security_code</th>
                        <th>zip_code</th>
                        <th>id_customer</th>
                    </tr>
                </head>
                <tbody>
                    {records}
                </tbody>
            </table>
            """,
        )
