from app import app
from flask import request
from routes.helpers import html
from datetime import datetime
import psycopg2
import math
import os

DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL, sslmode="require")

GENERIC_ERROR = "An error ocurred"


@app.route("/add-warranty")
def add_warranty():
    """
    Add warranty
    """
    # Actually add the warranty
    id_customer = request.args.get("id_customer")
    id_order = request.args.get("id_order")
    # Require passing id for customer and order
    params = [id_customer, id_order]
    with conn.cursor() as cur:
        if not any((x == "" or x is None) for x in params):
            # Check the customer exists
            # Fine to be from customer table
            cur.execute(
                """
                SELECT id
                FROM customer AS c
                WHERE c.id = %s
                """,
                (id_customer),
            )
            customer = cur.fetchone()
            if customer is None:
                return f"id_customer={id_customer} doesn't exist"
            # Check the order exists
            cur.execute(
                """
                SELECT id, total_amt, date
                FROM public.order AS o
                WHERE o.id = %s
                """,
                (id_order),
            )
            order = cur.fetchone()
            if order is None:
                return f"id_order={id_order} doesn't exist"
            # Check if warranty exists
            cur.execute(
                """
                SELECT id
                FROM warranty AS w
                WHERE w.id_order = %s
                """,
                (id_order),
            )
            warranty = cur.fetchone()
            if warranty is not None:
                return "Warranty already exists"
            # Check risk for a particular customer
            # if their personal information exists
            cur.execute(
                """
                SELECT has_risk
                FROM personal_information AS p
                WHERE p.id_customer = %s
                """,
                (id_customer),
            )
            pi = cur.fetchone()
            # Hardcoding for now instead of putting in database
            # Default to 20 when no information is given
            percentage = 20
            if pi is not None:
                has_risk = pi[0]
                if bool(has_risk):
                    percentage = 15
                else:
                    percentage = 10
            order_total_amt = int(order[1])
            warranty_price = math.floor((percentage / 100) * order_total_amt)
            expiration_date = datetime.now().date()
            date_order = order[2]
            # Add the warranty with the id being assigned
            # automatically since it's of serial type
            cur.execute(
                """
                INSERT INTO warranty (expiration_date, price, percentage, id_order, date_order)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    expiration_date,
                    warranty_price,
                    percentage,
                    id_order,
                    # Not sure why this is
                    # needed at the moment
                    date_order,
                ),
            )
            conn.commit()
        cur.execute(
            """
            SELECT id, expiration_date, price, percentage, id_order, date_order
            FROM warranty
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
            </tr>
            """
        return html(
            "Add warranty",
            f"""
            <table border="1">
                <thead>
                    <tr>
                        <th>id</th>
                        <th>expiration_date</th>
                        <th>price</th>
                        <th>percentage</th>
                        <th>id_order</th>
                        <th>date_order</th>
                    </tr>
                </head>
                <tbody>
                    {records}
                </tbody>
            </table>
            """,
        )
