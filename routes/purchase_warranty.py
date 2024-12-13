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
        <form method="GET" action="add-warranty">
            <input type="input" name="id_customer" placeholder="Enter id_customer" /><br />
            <input type="input" name="id_order" placeholder="Enter id_order" /><br />
            <input type="submit" value="Submit" />
        </form>
        """,
    )
