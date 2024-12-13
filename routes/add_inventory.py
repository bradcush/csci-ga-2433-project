from app import app
from flask import request
from routes.helpers import html
import psycopg2
import os

DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL, sslmode="require")

GENERIC_ERROR = "An error ocurred"


@app.route("/add-inventory")
def add_inventory():
    """
    Add inventory
    """
    # Actually add the inventory
    location = request.args.get("location")
    quantity = request.args.get("quantity")
    id_product = request.args.get("id_product")
    with conn.cursor() as cur:
        if location and quantity and id_product:
            cur.execute(
                """
                SELECT location, quantity, id_product
                FROM inventory
                WHERE location = %s
                  AND id_product = %s
                """,
                (location, id_product),
            )
            if cur.fetchone() is not None:
                return "location, id_product not unique"
            try:
                cur.execute(
                    """
                    INSERT INTO inventory (location, quantity, id_product)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        location,
                        quantity,
                        id_product,
                    ),
                )
                conn.commit()
            except Exception:
                return GENERIC_ERROR
        cur.execute(
            """
            SELECT location, quantity, id_product
            FROM inventory
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
            "Add inventory",
            f"""
            <table border="1">
                <thead>
                    <tr>
                        <th>location</th>
                        <th>quantity</th>
                        <th>id_product</th>
                    </tr>
                </head>
                <tbody>
                    {records}
                </tbody>
            </table>
            """,
        )
