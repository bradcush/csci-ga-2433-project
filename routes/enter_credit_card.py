from app import app
from routes.helpers import html


@app.route("/enter-credit-card")
def enter_credit_card():
    """
    Enter credit card
    """
    return html(
        "Enter credit card",
        """
        <form method="GET" action="add-credit-card">
            <input type="input" name="fname" placeholder="Enter first name" /><br />
            <input type="input" name="minit" placeholder="Enter middle initial" /><br />
            <input type="input" name="lname" placeholder="Enter last name" /><br />
            <input type="input" name="number" placeholder="Enter cc number" /><br />
            <input type="input" name="expiration_date" placeholder="Enter expiration date" /><br />
            <input type="input" name="security_code" placeholder="Enter security code" /><br />
            <input type="input" name="zip_code" placeholder="Enter zip code" /><br />
            <input type="input" name="id_customer" placeholder="Enter id_customer" /><br />
            <input type="submit" value="Submit" />
        </form>
        """,
    )
