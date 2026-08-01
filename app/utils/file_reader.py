from pathlib import Path

def read_file(file_path:Path)->str:
    try:
        return file_path.read_text(encoding="utf-8",errors="ignore")
    except (OSError, UnicodeError):
        return ""