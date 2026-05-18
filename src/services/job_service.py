from src.db.repositories.job_repo import JobRepository


class JobService:

    def __init__(self, crawler):
        self.crawler = crawler
        self.repo = JobRepository()

    def run(self, user_id: int, keywords: list, **kwargs):

        jobs = self.crawler.search_jobs(
            keywords=keywords,
            **kwargs
        )

        self.repo.save_jobs_for_user(
            user_id=user_id,
            jobs=jobs
        )

        return jobs