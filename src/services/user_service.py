from src.db.repositories.user_repo import UserRepository
from src.core.exceptions import UserNotFoundException
from src.db.repositories.keyword_repo import KeywordRepository


class UserService:

    def __init__(self):
        self.user_repo = UserRepository()
        self.keyword_repo = KeywordRepository()

    def get_keywords(self, user_id: int):

        # 1. check if user exists in DB
        user = self.user_repo.get_by_id(user_id)

        if not user:
            raise UserNotFoundException(f"User {user_id} not found")

        # 2. return keywords
        return self.keyword_repo.get_keywords(user_id)