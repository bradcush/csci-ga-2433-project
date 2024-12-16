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
        <p>Enter the details for an order. The `status` must be one of `placed`
        | `filled` | `backorder`. Any `quantity` is acceptable and the
        `id_customer` and `id_product` must be a valid id for an existing
        customer and product in the database respectively.</p>
        <form method="GET" action="add-order">
            <input type="input" name="status" placeholder="Enter status" /><br />
            <input type="input" name="quantity" placeholder="Enter quantity" /><br />
            <input type="input" name="id_customer" placeholder="Enter id_customer" /><br />
            <input type="input" name="id_product" placeholder="Enter id_product" /><br />
            <input type="submit" value="Submit" />
        </form>
        """,
    )
