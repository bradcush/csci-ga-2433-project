from app import app
from flask import request
from routes.helpers import html
import psycopg2
import pandas as pd
import pickle
import os

DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL, sslmode="require")

GENERIC_ERROR = "An error ocurred"


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
        params = [age, kids_count, pets_count, siblings_count, income, id_customer]
        if not any((x == "" or x is None) for x in params):
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
