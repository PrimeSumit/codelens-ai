import ast
from pathlib import Path
from app.utils.file_reader import read_file
def chunk_python(file_path: Path):
    source_code=read_file(file_path)
    if not source_code:
        return []
    try:
        tree=ast.parse(source_code)
    except SyntaxError:
        return []

    chunks = []

    for node in tree.body:
        if isinstance(node,ast.FunctionDef):
            pass
        elif isinstance(node,ast.AsyncFunctionDef):
            pass

    return chunks


def chunk_markdown(file_path: Path):
    pass


def chunk_json(file_path: Path):
    pass


def chunk_yaml(file_path: Path):
    pass


def chunk_text(file_path: Path):
    pass



CHUNKER={
    ".py": chunk_python,
    ".md": chunk_markdown,
    ".json": chunk_json,
    ".yaml": chunk_yaml,
    ".yml": chunk_yaml,
    ".txt": chunk_text,
}
def chunk_file(file_path:Path):
    chunker=CHUNKER.get(file_path.suffix,chunk_text)
    return chunker(file_path)

        