from src.db.session import SessionLocal
from src.db.models import User, Keyword
from src.db.init_db import init_db


def seed():

    init_db()

    session = SessionLocal()

    try:
        # Create user
        edit_policy = {
            "summary": True,
            "experience": False,
            "skills": False,
            "education": False
        }

        user = User(name="test_user",cv_edit_policy=edit_policy)
        session.add(user)
        session.flush()  # get user.id

        # Add keywords
        keywords = ["Applied Scientist", "Data Analyst", "ML Engineer"]

        for kw in keywords:
            session.add(Keyword(
                user_id=user.id,
                value=kw
            ))

        session.commit()

        print(f"Seeded user_id={user.id}")

    finally:
        session.close()


if __name__ == "__main__":
    seed()