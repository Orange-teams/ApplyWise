from src.services.user_service import UserService
from src.services.job_service import JobService
from src.crawlers.linkedin import LinkedInCrawler
from src.core.exceptions import UserNotFoundException

class ApplicationPipeline:

    def run(self, user_id: int):

        # 1. get user keywords from DB
        user_service = UserService()
        try:
            keywords = user_service.get_keywords(user_id)

        except UserNotFoundException:
            print("User missing → stopping pipeline")
            return

        # 2. crawl jobs
        crawler = LinkedInCrawler()
        job_service = JobService(crawler)

        jobs = job_service.run(
            user_id=user_id,
            keywords=keywords,
            location="Germany",
            job_format="full-time",
            experience_level="entry",
            max_jobs=20,
        )

        return jobs