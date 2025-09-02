from app.extensions import db
from app.utils.func import handle_db_errors
from app.models.user import User


@handle_db_errors()
def create_user(
    email: str,
    password: str,
    name: str,
    auth_provider: str = "email",
):
    user = User(email=email, name=name, auth_provider=auth_provider)

    user.set_password(password)

    db.session.add(user)
    db.session.commit()


@handle_db_errors()
def find_by_email(email: str) -> User | None:
    return User.query.filter_by(email=email).first()
