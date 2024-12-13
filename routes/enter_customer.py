from app import app
from routes.helpers import html


@app.route("/enter-customer")
def enter_customer():
    """
    Enter customer
    """
    return html(
        "Enter customer",
        """
        <form method="GET" action="add-customer">
            <input type="input" name="name" placeholder="Enter name" /><br />
            <input type="input" name="email" placeholder="Enter email" /><br />
            <input type="input" name="phone" placeholder="Enter phone" /><br />
            <input type="submit" value="Submit" />
        </form>
        """,
    )
