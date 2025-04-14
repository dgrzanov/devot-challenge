from sqlmodel import Session, select

from auth.auth_models import User


def update_user_balance(session: Session, user_id: int, amount: float) -> None:
    user = session.get(User, user_id)
    if user:
        new_balance = user.balance - amount

        user.balance = new_balance
        session.add(user)
        session.commit()
        session.refresh(user)
