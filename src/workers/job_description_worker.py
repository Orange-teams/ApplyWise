import logging
from bs4 import BeautifulSoup
from src.utils.http import get
from src.models.job import Job


logger = logging.getLogger(__name__)


class JobDescriptionWorker:

    def enrich(self, jobs: list[Job]) -> list[Job]:

        enriched_jobs = []

        for job in jobs:

            logger.info(
                f"Fetching description: {job.url}"
            )

            try:
                description = self._extract_text(job.url)
                # update pydantic object
                job.job_description = description

                enriched_jobs.append(job)

            except Exception as e:
                logger.warning(
                    f"Failed extracting {job.url} | {e}"
                )

        return enriched_jobs

    def _extract_text(self, url: str) -> str:
        response = get(url)
        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        # remove noisy elements
        for tag in soup(
            ["script", "style", "footer", "nav"]
        ):
            tag.decompose()

        return soup.get_text(
            separator=" ",
            strip=True,
        )