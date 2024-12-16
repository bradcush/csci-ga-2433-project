from routes.helpers import html
from app import app


@app.route("/")
def home():
    """
    Homepage that contains links to all use cases
    which can be run consecutively or separately
    """
    return html(
        "Use cases",
        """
        <p>The below use cases are assumed to be executed in order by either an
        employee or customer of Circuit Blocks, Inc. Proper execution leads to
        the creation of a warranty whose price is prediction based and
        determined by a pre-trained model.</p>
        <p>Each link navigates to a form with a description of the use case and
        a form where data can be entered. Upon submission of the form, a
        results page with the added entry in the database is shown. Otherwise,
        if an entry cannot be added, an error is shown.</p>
        <p><i>Note: If a form is missing data we just show the results. Therefore,
        you can submit an empty form if you would like to see the contents of a
        given table without submission.</i></p>
        <ul>
            <li> Employee
                <ul>
                    <li><a href="enter-product" title="Enter product">Enter product</a></li>
                    <li><a href="enter-inventory" title="Enter inventory">Enter inventory</a></li>
                </ul>
            </li>
            <li> Customer
                <ul>
                    <li><a href="enter-customer" title="Enter customer">Enter customer</a></li>
                    <li><a href="enter-credit-card" title="Enter credit card">Enter credit card</a></li>
                    <li><a href="place-order" title="Place order">Place order</a></li>
                    <li><a href="enter-personal" title="Enter personal information">Enter personal information</a></li>
                    <li><a href="purchase-warranty" title="Purchase warranty">Purchase warranty</a></li>
                    <li><a href="view-warranty" title="View warranty">View warranty</a></li>
                </ul>
            </li>
        </ul>
        """,
    )
