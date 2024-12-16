from app import app
from routes.helpers import html


@app.route("/enter-personal")
def enter_personal():
    """
    Enter personal information
    """
    return html(
        "Enter personal information",
        """
        <p>Personal information can be entered for a customer which is used to
        predict the risk of that customer. Upon submission, a risk prediction
        will be calculated using a pre-trained model and entered with the
        customer's personal information in the database. A valid id for an
        existing customer must be entered for the `id_customer` field.</p>
        <form method="GET" action="add-personal">
            <input type="input" name="age" placeholder="Enter age" /><br />
            <input type="input" name="kids_count" placeholder="Enter kids_count" /><br />
            <input type="input" name="pets_count" placeholder="Enter pets_count" /><br />
            <input type="input" name="siblings_count" placeholder="Enter siblings_count" /><br />
            <input type="input" name="income" placeholder="Enter income" /><br />
            <input type="input" name="id_customer" placeholder="Enter id_customer" /><br />
            <input type="submit" value="Submit" />
        </form>
        """,
    )
