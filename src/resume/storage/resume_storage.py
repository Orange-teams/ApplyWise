from pathlib import Path


class ResumeStorage:

    def load_template(self, path: str) -> str:
        return Path(path).read_text(encoding="utf-8")

    def save_tex(self, path: str, content: str):

        Path(path).write_text(
            content,
            encoding="utf-8",
        )