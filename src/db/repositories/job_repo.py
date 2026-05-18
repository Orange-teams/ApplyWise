from src.db.session import SessionLocal
from src.db.models import Job as JobTable, UserJob


class JobRepository:

    def save_jobs_for_user(self, user_id: int, jobs: list):

        session = SessionLocal()

        try:
            for job in jobs:

                # job is Pydantic object → use dot access
                db_job = session.query(JobTable).filter_by(
                    url=job.url
                ).first()

                if not db_job:
                    db_job = JobTable(
                        title=job.title,
                        company=job.company,
                        location=job.location,
                        url=job.url,
                        source=job.source,
                    )
                    session.add(db_job)
                    session.flush()

                # check user-job relation
                exists = session.query(UserJob).filter_by(
                    user_id=user_id,
                    job_id=db_job.id,
                ).first()

                if exists:
                    continue

                session.add(UserJob(
                    user_id=user_id,
                    job_id=db_job.id,
                    matched_keyword=job.matched_keyword,
                ))

            session.commit()

        finally:
            session.close()