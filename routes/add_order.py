from app import app
from flask import request
from datetime import datetime
from routes.helpers import html
import psycopg2
import os

DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL, sslmode="require")

GENERIC_ERROR = "An error ocurred"


@app.route("/add-order")
def add_order():
    """
    Add order
    """
    # Actually add the order
    status = request.args.get("status")
    quantity = request.args.get("quantity")
    id_customer = request.args.get("id_customer")
    id_product = request.args.get("id_product")
    with conn.cursor() as cur:
        if status and quantity and id_customer and id_product:
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
                SELECT price
                FROM product as p
                WHERE p.id = %s
                """,
                (id_product,),
            )
            product = cur.fetchone()
            if product is None:
                return "product_id doesn't exist"
            # Calculate amount based on product price
            # Everything comes in as a string so change it
            total_amt = int(product[0]) * int(quantity)
            date = datetime.now().date()
            # We should be updating the amount of inventory in
            # one of the separate inventory tables we have
            # when an order has the status of filled
            try:
                cur.execute(
                    """
                    INSERT INTO public.order (status, date, quantity, total_amt, id_customer, id_product)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        status,
                        date,
                        quantity,
                        total_amt,
                        id_customer,
                        id_product,
                    ),
                )
                conn.commit()
            except Exception:
                return GENERIC_ERROR
        cur.execute(
            """
            SELECT id, status, date, quantity, total_amt, id_customer, id_product
            FROM public.order
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
            </tr>
            """
        return html(
            "Add order",
            f"""
            <table border="1">
                <thead>
                    <tr>
                        <th>id</th>
                        <th>status</th>
                        <th>date</th>
                        <th>quantity</th>
                        <th>total_amt</th>
                        <th>id_customer</th>
                        <th>id_product</th>
                    </tr>
                </head>
                <tbody>
                    {records}
                </tbody>
            </table>
            """,
        )
