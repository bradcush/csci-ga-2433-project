from app import app
from routes.helpers import html


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
