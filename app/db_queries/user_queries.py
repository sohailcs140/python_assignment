from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(value: str, db: Session) -> User:
    """
    Retrieve a user from the database by their email.

    Args:
        value (str): The email address of the user.
        db (Session): The database session.

    Returns:
        User: The user associated with the provided email, or None if not found.
    """
    return db.query(User).filter(User.email == value).first()


def register_new_user(user: User, db: Session) -> User:
    """
    Add a new user to the database.

    Args:
        user (User): The user instance to be added.
        db (Session): The database session.

    Returns:
        User: The added user instance.
    """
    db.add(user)
    db.commit()
    return user
