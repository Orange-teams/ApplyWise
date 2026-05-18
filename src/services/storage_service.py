from config.settings import settings
import json


class StorageService:

    @staticmethod
    def save_jobs(jobs, filename):

        output_dir = settings.OUTPUT_DIR

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = output_dir / filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(
                [job.model_dump() for job in jobs],
                f,
                indent=4,
                ensure_ascii=False,
            )