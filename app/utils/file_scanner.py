from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
}
IGNORED_DIRECTORIES = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    ".idea",
    ".vscode",
    ".pytest_cache",
    ".mypy_cache",
}

def scan_repo(repo_path:Path)->list[Path]:
    files=[]
    for path in repo_path.rglob("*"):
        if not path.is_file():
            continue
        if any(parent.name in IGNORED_DIRECTORIES for parent in path.parents):
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        files.append(path)

    return files