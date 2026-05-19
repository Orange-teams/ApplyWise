import subprocess
from pathlib import Path


class LatexCompiler:

    def compile(
        self,
        tex_path: str,
        output_dir: str,
    ) -> bool:

        result = subprocess.run(
            [
                "pdflatex",
                "-interaction=nonstopmode",
                f"-output-directory={output_dir}",
                tex_path,
            ],
            capture_output=True,
            text=True,
        )

        return result.returncode == 0