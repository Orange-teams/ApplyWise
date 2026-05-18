from pathlib import Path
from tree_utils import build_tree

START = "<!-- BEGIN TREE -->"
END = "<!-- END TREE -->"

def update_readme_for_dir(directory: Path):
    readme = directory / "README.md"

    if not readme.exists():
        return

    tree_lines = build_tree(directory)
    tree_text = "```text\n" + "\n".join(tree_lines) + "\n```"

    content = readme.read_text()

    if START not in content or END not in content:
        return

    before = content.split(START)[0]
    after = content.split(END)[1]

    new_content = (
        before
        + START + "\n"
        + tree_text + "\n"
        + END
        + after
    )

    readme.write_text(new_content)
    print(f"Updated: {readme}")