from src.workflows.application_pipeline import ApplicationPipeline
from src.utils.logger import setup_logger
from src.db.bootstrap import bootstrap_db


def main():

    setup_logger()
    bootstrap_db()


    pipeline = ApplicationPipeline()

    pipeline.run(user_id=1)


if __name__ == "__main__":
    main()