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
        <p>Enter the product type and price. Note that valid types are `bundle`
        | `battery` | `block`. Prices should be entered as whole numbers of
        dollars and cents (eg. 2499) without a decimal point.</p>
        <form method="GET" action="add-product">
            <input type="input" name="type" placeholder="Enter type" /><br />
            <input type="input" name="price" placeholder="Enter price" /><br />
            <input type="submit" value="Submit" />
        </form>
        """,
    )
