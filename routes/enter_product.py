from routes.helpers import html
from app import app


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
