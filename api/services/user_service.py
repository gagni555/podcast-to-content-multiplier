from sqlalchemy.orm import Session
from api.models import User
from api.utils import verify_password


def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user by email and password
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_user_by_email(db: Session, email: str):
    """
    Get a user by email
    """
    return db.query(User).filter(User.email == email).first()