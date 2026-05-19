from src.db.repositories.job_repo import JobRepository
from src.core.exceptions import JobNotFoundException


class JobService:

    def __init__(self, crawler=None):
        self.crawler = crawler
        self.repo = JobRepository()

    # ---------------------------------
    # FETCH JOBS
    # ---------------------------------
    def fetch_jobs(
        self,
        keywords: list,
        **kwargs
    ):

        if not self.crawler:
            raise ValueError(
                "Crawler is required"
            )

        return self.crawler.search_jobs(
            keywords=keywords,
            **kwargs
        )

    # ---------------------------------
    # SAVE JOBS
    # ---------------------------------
    def save_jobs(
        self,
        user_id: int,
        jobs: list,
    ):

        self.repo.save_jobs_for_user(
            user_id=user_id,
            jobs=jobs,
        )

    # ---------------------------------
    # GET JOB BY ID
    # ---------------------------------
    def get_job(
        self,
        job_id: int
    ):
        job = self.repo.get_job(job_id)
        if not job:
            raise JobNotFoundException(f"Job {job_id} not found")
        return job