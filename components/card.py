from dash import html

def Card(title, content):
    """
    Create a reusable card component.

    Parameters:
    - title (str): The title of the card.
    - content (list): A list of strings or Dash HTML elements to display as the card's content.

    Returns:
    - Dash HTML Div: A styled card component.
    """
    return html.Div(
        [
            html.H3(title, className="card-title"),
            html.Div([
                html.Div(content, className="card-content"),
            ],className="card-container"),
        ],
        className="card",
    )