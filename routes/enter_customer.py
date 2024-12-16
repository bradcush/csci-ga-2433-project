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
        <p>Enter the name, email, and phone to create a new customer. Each
        customer is automatically assigned a distinct identifier by the system.
        The `id` will be used to identify a specific user when entering data
        into other forms related to other use cases.</p>
        <form method="GET" action="add-customer">
            <input type="input" name="name" placeholder="Enter name" /><br />
            <input type="input" name="email" placeholder="Enter email" /><br />
            <input type="input" name="phone" placeholder="Enter phone" /><br />
            <input type="submit" value="Submit" />
        </form>
        """,
    )
