from src.db.session import SessionLocal
from src.db.models import Keyword


class KeywordRepository:

    def get_keywords(self, user_id: int):

        session = SessionLocal()

        try:
            rows = session.query(Keyword).filter(
                Keyword.user_id == user_id
            ).all()

            return [r.value for r in rows]

        finally:
            session.close()