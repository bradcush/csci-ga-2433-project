from flask import Flask, request, send_file
from datetime import datetime
from minio import Minio
import os
import psycopg2
import pandas as pd
import pickle
import math


DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL, sslmode="require")

app = Flask(__name__)

GENERIC_ERROR = "An error ocurred"


# Helper function to easily template html
# that we want to share across pages
def html(title, content):
    """
    Basic templating
    """
    return f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="style.css" rel="stylesheet" />
            <title>{title}</title>
        </head>
        <body>
            <h1>{title}</h1>
            {content}
            <footer>
                <a href="/" title="Home">Home</a>
            </footer>
        </body>
    </html>
    """


@app.route("/style.css")
def style():
    """
    Only CSS is static
    """
    return send_file("style.css")


@app.route("/")
def home():
    """
    Homepage that contains links to all use cases
    which can be run consecutively or separately
    """
    return html(
        "Use cases",
        """
        <p>The below use cases are assumed to be executed in order by either an
        employee or customer of Circuit Blocks, Inc. Proper execution leads to
        the creation of a warranty whose price is prediction based and
        determined by a pre-trained model.</p>
        <p>Each link navigates to a form with a description of the use case and
        a form where data can be entered. Upon submission of the form, a
        results page with the added entry in the database is shown. Otherwise,
        if an entry cannot be added, an error is shown.</p>
        <ul>
            <li> Employee
                <ul>
                    <li><a href="enter-product" title="Enter product">Enter product</a></li>
                    <li><a href="enter-inventory" title="Enter inventory">Enter inventory</a></li>
                    <li><a href="enter-customer" title="Enter customer">Enter customer</a></li>
                </ul>
            </li>
            <li> Customer
                <ul>
                    <li><a href="place-order" title="Place order">Place order</a></li>
                    <li><a href="enter-personal" title="Enter personal information">Enter personal information</a></li>
                    <li><a href="purchase-warranty" title="Purchase warranty">Purchase warranty</a></li>
                    <li><a href="view-warranty" title="View warranty">View warranty</a></li>
                </ul>
            </li>
        </ul>
        """,
    )


@app.route("/enter-product")
def enter_product():
    """
    Enter product
    """
    return html(
        "Enter product",
        """
        <form method="GET" action="add-product">
            <input type="input" name="type" placeholder="Enter type" /><br />
            <input type="input" name="price" placeholder="Enter price" /><br />
            <input type="submit" value="Submit" />
        </form>
        """,
    )


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


@app.route("/enter-inventory")
def enter_inventory():
    """
    Enter inventory
    """
    return html(
        "Enter inventory",
        """
        <form method="GET" action="add-inventory">
            <input type="input" name="location" placeholder="Enter location" /><br />
            <input type="input" name="quantity" placeholder="Enter quantity" /><br />
            <input type="input" name="id_product" placeholder="Enter id_product" /><br />
            <input type="submit" value="Submit" />
        </form>
        """,
    )


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


@app.route("/enter-customer")
def enter_customer():
    """
    Enter customer
    """
    return html(
        "Enter customer",
        """
        <form method="GET" action="add-customer">
            <input type="input" name="name" placeholder="Enter name" /><br />
            <input type="input" name="email" placeholder="Enter email" /><br />
            <input type="input" name="phone" placeholder="Enter phone" /><br />
            <input type="submit" value="Submit" />
        </form>
        """,
    )


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
            SELECT name, email, phone
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
            </tr>
            """
        return html(
            "Add customer",
            f"""
            <table border="1">
                <thead>
                    <tr>
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


@app.route("/place-order")
def place_order():
    """
    Place order
    """
    return html(
        "Place order",
        """
        <form method="GET" action="add-order">
            <input type="input" name="status" placeholder="Enter status" /><br />
            <input type="input" name="quantity" placeholder="Enter quantity" /><br />
            <input type="input" name="id_customer" placeholder="Enter id_customer" /><br />
            <input type="input" name="id_product" placeholder="Enter id_product" /><br />
            <input type="submit" value="Submit" />
        </form>
        """,
    )


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


@app.route("/enter-personal")
def enter_personal():
    """
    Enter personal information
    """
    return html(
        "Enter personal information",
        """
        <form method="GET" action="add-personal">
            <input type="input" name="age" placeholder="Enter age" /><br />
            <input type="input" name="kids_count" placeholder="Enter kids_count" /><br />
            <input type="input" name="pets_count" placeholder="Enter pets_count" /><br />
            <input type="input" name="siblings_count" placeholder="Enter siblings_count" /><br />
            <input type="input" name="income" placeholder="Enter income" /><br />
            <input type="input" name="id_customer" placeholder="Enter id_customer" /><br />
            <input type="submit" value="Submit" />
        </form>
        """,
    )


@app.route("/add-personal")
def add_personal():
    """
    Add personal
    """
    """
    Predict risk given indicators as arguments which returns
    an integer 1 if risk exists or 0 if no risk exists. Note that
    we have made overwriting personal information and risk okay.
    """
    age = request.args.get("age")
    kids_count = request.args.get("kids_count")
    pets_count = request.args.get("pets_count")
    siblings_count = request.args.get("siblings_count")
    income = request.args.get("income")
    id_customer = request.args.get("id_customer")
    with conn.cursor() as cur:
        # All arguments are required for prediction
        params = [id_customer, age, kids_count, pets_count, siblings_count, income]
        if any(x == None for x in params):
            return "Missing arguments"
        # Check if particular user exists
        cur.execute(
            """
            SELECT id
            FROM customer
            WHERE id = %s
            """,
            (id_customer),
        )
        customer = cur.fetchone()
        if customer is None:
            return "id_customer doesn't exist"
        # Load the exsting model locally for now
        with open("prediction/model.pkl", "rb") as f:
            model = pickle.load(f)
        # Query should be a data frame
        query = pd.DataFrame(
            data=(
                {
                    "age": age,
                    "kids_count": kids_count,
                    "pets_count": pets_count,
                    "siblings_count": siblings_count,
                    "income": income,
                },
            )
        )
        # int64 requires int coversion first
        has_risk = int(model.predict(query)[0])
        # Update regardless of if an entry already exists
        # which makes testing this endpoint a bit easier
        try:
            cur.execute(
                """
                INSERT INTO personal_information (age, kids_count, pets_count, siblings_count, income, has_risk, id_customer)
                VALUES (%(age)s, %(kids_count)s, %(pets_count)s, %(siblings_count)s, %(income)s, %(has_risk)s, %(id_customer)s)
                ON CONFLICT (id_customer) DO UPDATE
                  SET age = %(age)s,
                  kids_count = %(kids_count)s,
                  pets_count = %(pets_count)s,
                  siblings_count = %(siblings_count)s,
                  income = %(income)s,
                  has_risk = %(has_risk)s;
                """,
                {
                    "age": age,
                    "kids_count": kids_count,
                    "pets_count": pets_count,
                    "siblings_count": siblings_count,
                    "income": income,
                    "has_risk": has_risk,
                    "id_customer": id_customer,
                },
            )
            conn.commit()
        except Exception:
            return GENERIC_ERROR
        cur.execute(
            """
            SELECT age, kids_count, pets_count, siblings_count, income, has_risk, id_customer
            FROM personal_information
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
            "Add personal information",
            f"""
            <table border="1">
                <thead>
                    <tr>
                        <th>age</th>
                        <th>kids_count</th>
                        <th>pets_count</th>
                        <th>siblings_count</th>
                        <th>income</th>
                        <th>has_risk</th>
                        <th>id_customer</th>
                    </tr>
                </head>
                <tbody>
                    {records}
                </tbody>
            </table>
            """,
        )


@app.route("/purchase-warranty")
def purchase_warranty():
    """
    Purchase warranty
    """
    return html(
        "Purchase warranty",
        """
        <form method="GET" action="add-warranty">
            <input type="input" name="id_customer" placeholder="Enter id_customer" /><br />
            <input type="input" name="id_order" placeholder="Enter id_order" /><br />
            <input type="submit" value="Submit" />
        </form>
        """,
    )


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
    if any(x == None for x in params):
        return "Missing arguments"
    with conn.cursor() as cur:
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


@app.route("/stackhero")
def stackhero():
    """
    Temporary S3 storage integration to make
    sure things are hooked up properly
    """
    endpoint = os.environ.get("STACKHERO_MINIO_HOST")
    if endpoint is None:
        return "Missing endpoint"
    endpoint = endpoint + ":443"
    client = Minio(
        endpoint=endpoint,
        secure=True,
        access_key=os.environ.get("STACKHERO_MINIO_ACCESS_KEY"),
        secret_key=os.environ.get("STACKHERO_MINIO_SECRET_KEY"),
        region="us-east-1",
    )
    found = client.bucket_exists("test")
    if not found:
        client.make_bucket("test")
    else:
        return "Bucket already exists"
    # Upload 'README.md' as object name
    # 'README.md' to bucket 'test'
    client.fput_object(
        "test",
        "README.md",
        "/home/bradcush/Documents/repos/csci-ga-2433-project/README.md",
    )
    return "Successful test"


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
