from app import app
from routes.helpers import html


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
