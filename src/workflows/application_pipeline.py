from src.services.user_service import UserService
from src.services.job_service import JobService
from src.crawlers.linkedin import LinkedInCrawler
from src.core.exceptions import UserNotFoundException
from src.workers.job_description_worker import (
    JobDescriptionWorker,
)
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

        jobs = job_service.fetch_jobs(
            keywords=keywords,
            location="Germany",
            job_format="full-time",
            experience_level="entry",
            max_jobs=20,
        )
        worker = JobDescriptionWorker()
        enriched_jobs = worker.enrich(jobs)

        job_service.save_jobs(
            user_id=user_id,
            jobs=enriched_jobs,
        )

        return enriched_jobs