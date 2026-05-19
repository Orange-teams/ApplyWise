import os
from src.utils.time import now
from src.db.init_db import init_db
from src.db.session import SessionLocal
from src.db.models import User, UserCV, Keyword
from src.resume.latex_parser import LatexCVParser
from config.settings import MY_LATEX

DEFAULT_NAME = "Salar Mohtaj"
DEFAULT_EMAIL = "salar.mohtaj@gmail.com"
DEFAULT_LATEX = MY_LATEX
# -----------------------------
# Helpers
# -----------------------------

def load_latex(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parsed_to_dict(parsed):
    """
    Convert dataclass CVData → dict for JSON storage
    """
    return {
        "profile": parsed.profile,
        "skills": parsed.skills,
        "experience": [
            {
                "title": e.title,
                "duration": e.duration,
                "company": e.company,
                "location": e.location,
                "bullets": e.bullets,
            }
            for e in parsed.experience
        ],
        "projects": parsed.projects,
        "education": parsed.education,
    }


# -----------------------------
# Main pipeline
# -----------------------------

def run(full_name: str, user_email: str, latex_path: str):
    init_db()
    session = SessionLocal()
    try:
        parser = LatexCVParser()

        # 1. Create or fetch user
        user = session.query(User).filter(User.email == user_email).first()

        if not user:
            edit_policy = {
                "summary": True,
                "experience": False,
                "skills": False,
                "education": False
            }
            user = User(
                email=user_email,
                name=full_name,
                added_at=now()
            )
            session.add(user)
            session.flush()
            keywords = ["Applied Scientist", "Data Analyst", "ML Engineer"]

            for kw in keywords:
                session.add(Keyword(
                    user_id=user.id,
                    value=kw
                ))

        print(f"✅ User ready: {user.email} (id={user.id})")

        # 2. Load LaTeX
        latex = load_latex(latex_path)
        print("📄 LaTeX loaded")

        # 3. Parse LaTeX → structured CV
        parsed_cv = parser.parse(latex)
        cv_json = parsed_to_dict(parsed_cv)

        print("🧠 CV parsed into JSON")

        # 4. Save CV in DB
        user_cv = UserCV(
            user_id=user.id,
            raw_latex=latex,
            cv_edit_policy=edit_policy,
            parsed_json=cv_json
        )

        session.add(user_cv)
        session.commit()

        print(f"💾 CV stored (cv_id={user_cv.id})")

    finally:
        session.close()


# -----------------------------
# CLI entry
# -----------------------------

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--full_name", default=DEFAULT_NAME)
    parser.add_argument("--email", default=DEFAULT_EMAIL)
    parser.add_argument("--latex", default=DEFAULT_LATEX)

    args = parser.parse_args()

    run(args.full_name ,args.email, args.latex)