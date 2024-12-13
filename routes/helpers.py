# Helper function to easily template html
# that we want to share across pages
def html(title, content):
    """
    Basic templating
    """
    return f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="styles.css" rel="stylesheet" />
            <title>{title}</title>
        </head>
        <body>
            <h1>{title}</h1>
            {content}
            <footer>
                <a href="/" title="Home">Home</a>
            </footer>
        </body>
    </html>
    """
