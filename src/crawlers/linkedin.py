import logging
import time

from bs4 import BeautifulSoup

from src.crawlers.base import BaseCrawler
from src.models.job import Job
from src.utils.http import get
from src.constants.filters import (
    JOB_FORMAT_MAP,
    EXPERIENCE_LEVEL_MAP,
)
from config.settings import settings


logger = logging.getLogger(__name__)


class LinkedInCrawler(BaseCrawler):

    BASE_URL = (
        "https://www.linkedin.com/jobs-guest/"
        "jobs/api/seeMoreJobPostings/search"
    )

    SOURCE = "linkedin"

    def search_jobs(
        self,
        keywords,
        location="Germany",
        job_format="full-time",
        experience_level="entry",
        max_jobs=10,
    ):

        jobs = []

        api_job_format = JOB_FORMAT_MAP.get(
            job_format.lower(),
            "F",
        )

        api_exp_level = EXPERIENCE_LEVEL_MAP.get(
            experience_level.lower(),
            "2",
        )

        logger.info(
            f"Searching LinkedIn | "
            f"location={location} | "
            f"format={job_format} | "
            f"level={experience_level}"
        )

        for keyword in keywords:

            if len(jobs) >= max_jobs:
                break

            logger.info(f"Scanning keyword={keyword}")

            params = {
                "keywords": keyword,
                "location": location,
                "f_JT": api_job_format,
                "f_E": api_exp_level,
                "start": 0,
            }

            try:
                response = get(self.BASE_URL, params=params)

                soup = BeautifulSoup(
                    response.text,
                    "html.parser",
                )

                cards = soup.find_all("li")

                for card in cards:

                    if len(jobs) >= max_jobs:
                        break

                    parsed_job = self._parse_card(
                        card,
                        keyword,
                        location,
                        job_format,
                        experience_level,
                    )

                    if parsed_job:
                        jobs.append(parsed_job)

                        logger.info(
                            f"Found: {parsed_job.title}"
                        )

                time.sleep(settings.REQUEST_DELAY)

            except Exception as e:
                logger.exception(
                    f"Failed keyword={keyword} | error={e}"
                )

        return jobs

    def _parse_card(
        self,
        card,
        keyword,
        default_location,
        job_format,
        experience_level,
    ):

        title_element = card.find(
            "h3",
            class_="base-search-card__title",
        )

        company_element = card.find(
            "h4",
            class_="base-search-card__subtitle",
        )

        link_element = card.find(
            "a",
            class_="base-card__full-link",
        )

        location_element = card.find(
            "span",
            class_="job-search-card__location",
        )

        if not (
            title_element
            and company_element
            and link_element
        ):
            return None

        title = title_element.text.strip()

        if keyword.lower() not in title.lower():
            return None

        return Job(
            title=title,
            company=company_element.text.strip(),
            location=(
                location_element.text.strip()
                if location_element
                else default_location
            ),
            job_format=job_format.capitalize(),
            experience_level=experience_level.capitalize(),
            url=link_element["href"].split("?")[0],
            matched_keyword=keyword,
            source=self.SOURCE,
        )