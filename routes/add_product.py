from app import app
from flask import request
from routes.helpers import html
import os
import psycopg2

DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL, sslmode="require")


@app.route("/add-product")
def add_product():
    """
    Add product
    """
    # Actually add the product
    type = request.args.get("type")
    price = request.args.get("price")
    with conn.cursor() as cur:
        if type and price:
            cur.execute(
                """
                INSERT INTO product (type, price)
                VALUES (%s, %s)
                """,
                (
                    type,
                    price,
                ),
            )
            conn.commit()
        cur.execute(
            """
            SELECT id, type, price
            FROM product
            """
        )
        records = ""
        for record in cur:
            records += f"""
            <tr>
                <td>{record[0]}</td>
                <td>{record[1]}</td>
                <td>{record[2]}</td>
            </tr>
            """
        return html(
            "Add product",
            f"""
            <table border="1">
                <thead>
                    <tr>
                        <th>id</th>
                        <th>type</th>
                        <th>price</th>
                    </tr>
                </head>
                <tbody>
                    {records}
                </tbody>
            </table>
            """,
        )
