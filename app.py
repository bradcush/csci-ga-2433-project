from flask import Flask
from datetime import datetime
import os
import psycopg2

DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL, sslmode="require")

app = Flask(__name__)


@app.route("/")
def homepage():
    return datetime.now().strftime("%A, %d %b %Y %l:%M %p")


@app.route("/create")
def create():
    """
    Create a table in PostgreSQL
    """
    with conn.cursor() as cur:
        # Execute a command: this creates a new table
        # Hardcoding table and attributes to make things easier
        cur.execute(
            """
            CREATE TABLE sample (
                partition text,
                itemid text PRIMARY KEY,
                date text,
                comment text,
                url text)
            """
        )
        return "Created sample"


@app.route("/query")
def query():
    """
    Query table in PostgreSQL
    """
    with conn.cursor() as cur:
        # Query the database and obtain data as Python objects.
        cur.execute("SELECT * FROM sample")
        print(cur.fetchone())

        # You can use `cur.fetchmany()`, `cur.fetchall()` to return a
        # list of several records, or even iterate on the cursor
        for record in cur.fetchall():
            print(record)

        # Make the changes to the database persistent
        conn.commit()
    return "Queried sample"


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
