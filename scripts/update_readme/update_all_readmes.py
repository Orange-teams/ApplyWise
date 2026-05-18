from pathlib import Path
from update_readme import update_readme_for_dir

def walk_dirs(root: Path):
    for path in root.rglob("*"):
        if path.is_dir():
            update_readme_for_dir(path)

if __name__ == "__main__":
    repo_root = Path("..").resolve()
    walk_dirs(repo_root)