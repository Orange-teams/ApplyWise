from src.resume.latex_parser import LatexCVParser
class CVService:

    def __init__(self, db):
        self.db = db
        self.parser = LatexCVParser()

    def create_user_cv(self, user_id: int, latex: str):

        parsed = self.parser.parse(latex)

        cv = UserCV(
            user_id=user_id,
            raw_latex=latex,
            parsed_json=parsed_to_dict(parsed)
        )

        self.db.add(cv)
        self.db.commit()

        return cv