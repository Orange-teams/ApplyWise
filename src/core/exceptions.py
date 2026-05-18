class UserNotFoundException(Exception):
    """Raised when a user does not exist in the database."""
    pass


class JobNotFoundException(Exception):
    pass


class CrawlerException(Exception):
    pass