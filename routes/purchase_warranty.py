from app import app
from routes.helpers import html


@app.route("/purchase-warranty")
def purchase_warranty():
    """
    Purchase warranty
    """
    return html(
        "Purchase warranty",
        """
        <p>Enter the id of a valid customer and order that already exists in
        the datbase. A `price` and `percentage` of the order cost will be
        calculated based on the risk prediction already made.</p>
        <form method="GET" action="add-warranty">
            <input type="input" name="id_customer" placeholder="Enter id_customer" /><br />
            <input type="input" name="id_order" placeholder="Enter id_order" /><br />
            <input type="submit" value="Submit" />
        </form>
        """,
    )
