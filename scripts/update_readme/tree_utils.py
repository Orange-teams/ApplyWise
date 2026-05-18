from pathlib import Path

IGNORE_DIRS = {
    "__pycache__",
    ".ipynb_checkpoints",
    ".git",
    ".idea",
}

IGNORE_FILES = {
    ".DS_Store",
}

IGNORE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".webp",
}

def build_tree(path: Path, prefix=""):
    lines = []

    entries = [
        p for p in path.iterdir()
        if p.name not in IGNORE_DIRS
        and p.name not in IGNORE_FILES
        and p.suffix.lower() not in IGNORE_EXTENSIONS
    ]

    entries.sort(key=lambda p: (p.is_file(), p.name.lower()))

    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        lines.append(prefix + connector + entry.name)

        if entry.is_dir():
            extension = "    " if i == len(entries) - 1 else "│   "
            lines.extend(build_tree(entry, prefix + extension))

    return lines