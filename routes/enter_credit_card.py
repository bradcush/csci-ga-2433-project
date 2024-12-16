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
        <p>Enter credit card information tied to a specific customer. Note that
        the credit card `number` field should be 16 digits long in the format
        `XXXXXXXXXXXXXXXX` and must be unique acros all customers. The
        `expiration_date` must be in the format `2024-01-01`. We also enforce
        that `security_code` is 3 digits and the `zip_code` is 5 digits. Credit
        cards can only be added for a valid customer id already in the
        database.</p>
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
