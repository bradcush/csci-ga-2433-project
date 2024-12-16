from app import app
from routes.helpers import html
import psycopg2
import os

DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL, sslmode="require")

GENERIC_ERROR = "An error ocurred"


@app.route("/view-warranty")
def view_all():
    """
    View warranty
    """
    with conn.cursor() as cur:
        # Might be of better use to calculate some
        # statistics to see for warranties we have
        cur.execute(
            """
            SELECT c.id, c.email, o.id, o.status, o.date, p.id, p.type, w.id, w.percentage, w.price
            FROM customer as c, public.order as o, product as p, warranty as w
            WHERE c.id = o.id_customer
              AND p.id = o.id_product
              AND o.id = w.id_order
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
                <td>{record[8]}</td>
                <td>{record[9]}</td>
            </tr>
            """
        return html(
            "View warranty",
            f"""
            <p>The below table represents joined entries from the `customer`,
            `order`, `product`, and `warranty` tables for customers that have a
            warranty for a specific product. Populated entries in this table
            show that the prior use cases were executed necessary for the
            creation of a warranty.</p>
            <table border="1">
                <thead>
                    <tr>
                        <th>c.id</th>
                        <th>c.email</th>
                        <th>o.id</th>
                        <th>o.status</th>
                        <th>o.date</th>
                        <th>p.id</th>
                        <th>p.type</th>
                        <th>w.id</th>
                        <th>w.percentage</th>
                        <th>w.price</th>
                    </tr>
                </head>
                <tbody>
                    {records}
                </tbody>
            </table>
            """,
        )
