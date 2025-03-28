from flask import current_app as app
from models import User


def get_users():
    """
    Retrieve users from the database.
    """
    with app.app_context():
        users = User.query.all()
        return [{"username": user.username, "name": f"{user.firstname} {user.lastname}", "private": user.private} for
                user in users]


def search_users(query):
    """
    Search for users by username.

    Args:
        query (str): The username query to search for.

    Returns:
        list: A list of users that match the query.
    """
    users = get_users()  # Ensure users list is populated within app context
    results = [user for user in users if query.lower() in user['username'].lower()]
    return results


# Example usage
if __name__ == "__main__":
    from app import create_app

    app = create_app()
    with app.app_context():
        search_results = search_users('john')
        for user in search_results:
            print(user)
