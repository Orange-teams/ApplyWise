from abc import ABC, abstractmethod


class BaseCrawler(ABC):

    @abstractmethod
    def search_jobs(
        self,
        keywords,
        location,
        job_format,
        experience_level,
        max_jobs,
    ):
        pass