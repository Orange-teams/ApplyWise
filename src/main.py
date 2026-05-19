from src.workflows.application_pipeline import ApplicationPipeline
from src.workflows.cv_tailoring_pipeline import CVTailoringPipeline
from src.utils.logger import setup_logger
from src.db.bootstrap import bootstrap_db


def main():

    setup_logger()
    bootstrap_db()


    #pipeline = ApplicationPipeline()
    pipeline = CVTailoringPipeline()
    pipeline.run(job_id=1)
    #pipeline.run(user_id=1)


if __name__ == "__main__":
    main()
