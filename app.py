from flask import Flask
import psycopg2
import os


DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL, sslmode="require")

app = Flask(__name__)

GENERIC_ERROR = "An error ocurred"


# Declared routes implicit by import
# Uses circular dependency which isn't great
# but good enough for out needs for now
import routes.home
import routes.styles
import routes.enter_product
import routes.add_product
import routes.enter_personal
import routes.add_personal
import routes.enter_inventory
import routes.add_inventory
import routes.enter_customer
import routes.add_customer
import routes.enter_credit_card
import routes.add_credit_card
import routes.place_order
import routes.add_order
import routes.purchase_warranty
import routes.add_warranty
import routes.view_warranty


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
