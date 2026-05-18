from src.db.session import SessionLocal
from src.db.models import User


class UserRepository:

    def get_by_id(self, user_id: int):
        session = SessionLocal()

        try:
            return session.query(User).filter(User.id == user_id).first()

        finally:
            session.close()