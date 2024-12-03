from flask import Flask, request, jsonify
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


@app.route("/")
def home():
    return datetime.now().strftime("%A, %d %b %Y %l:%M %p")


@app.route("/api/predict")
def predict():
    """
    Predict risk given indicators as arguments which returns
    an integer 1 if risk exists or 0 if no risk exists
    """
    id = request.args.get("id")
    age = request.args.get("age")
    kids_count = request.args.get("kids_count")
    pets_count = request.args.get("pets_count")
    siblings_count = request.args.get("siblings_count")
    income = request.args.get("income")
    # All arguments are required for prediction
    params = [id, age, kids_count, pets_count, siblings_count, income]
    if any(x == None for x in params):
        reason = "Missing required arguments"
        return jsonify(error=True, reason=reason), 400
    # Check if particular user exists
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id
            FROM customer
            WHERE id = %s
            """,
            (id),
        )
        customers = cur.fetchall()
        if len(customers) < 1:
            reason = f"No such id={id} exists"
            return jsonify(error=True, reason=reason), 400
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
    with conn.cursor() as cur:
        # Update regardless of if an entry already exists
        # which makes testing this endpoint a bit easier
        cur.execute(
            """
            INSERT INTO personal_information (age, kids_count, pets_count, siblings_count, income, has_risk, id_customer)
            VALUES (%(age)s, %(kids_count)s, %(pets_count)s, %(siblings_count)s, %(income)s, %(has_risk)s, %(id)s)
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
                "id": id,
            },
        )
        conn.commit()
    return jsonify(prediction=has_risk)


@app.route("/api/warranty/purchase")
def purchase():
    """
    Purchase a warranty based on personal
    information and associated risk
    """
    id_customer = request.args.get("id_customer")
    id_order = request.args.get("id_order")
    # Require passing id for customer and order
    params = [id_customer, id_order]
    if any(x == None for x in params):
        return jsonify(error=True, reason="Missing required arguments"), 400
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
        customers = cur.fetchall()
        if len(customers) < 1:
            reason = f"id_customer={id_customer} doesn't exist"
            return jsonify(error=True, reason=reason), 400
        # Check the order exists
        cur.execute(
            """
            SELECT id, total_amt
            FROM public.order AS o
            WHERE o.id = %s
            """,
            (id_order),
        )
        orders = cur.fetchall()
        if len(orders) < 1:
            reason = f"id_order={id_order} doesn't exist"
            return jsonify(error=True, reason=reason), 400
        # Check if warranty exists
        cur.execute(
            """
            SELECT id
            FROM warranty AS w
            WHERE w.id_order = %s
            """,
            (id_order),
        )
        warranties = cur.fetchall()
        if len(warranties) > 0:
            reason = "Warranty already exists"
            return jsonify(error=True, reason=reason), 400
        # Check risk for a particular customer
        # if their personal information exists
        cur.execute(
            """
            SELECT has_risk
            FROM personal_information AS pi
            WHERE pi.id_customer = %s
            """,
            (id_customer),
        )
        pis = cur.fetchall()
        # Hardcoding for now instead of putting in database
        # Default to 20 when no information is given
        percentage = 20
        if len(pis) > 0:
            has_risk = pis[0]
            if bool(has_risk):
                percentage = 15
            else:
                percentage = 10

    order_total_amt = int(orders[0][1])
    warranty_price = math.floor((percentage / 100) * order_total_amt)
    expiration_date = datetime.now().date()
    # Add the warranty with the id being assigned
    # automatically since it's of serial type
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO warranty (expiration_date, price, percentage, id_order)
            VALUES (%s, %s, %s, %s)
            """,
            (
                expiration_date,
                warranty_price,
                percentage,
                id_order,
            ),
        )
        conn.commit()
    return jsonify(price=warranty_price, percentage=percentage)


@app.route("/api/stackhero/test")
def stackhero():
    """
    Temporary S3 storage integration to make
    sure things are hooked up properly
    """
    client = Minio(
        # Hardcoding the host value for now
        # os.environ.get("STACKHERO_MINIO_HOST")
        endpoint="jqqdw6.stackhero-network.com:443",
        secure=True,
        access_key=os.environ.get("STACKHERO_MINIO_ACCESS_KEY"),
        secret_key=os.environ.get("STACKHERO_MINIO_SECRET_KEY"),
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
    return "Success"


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
