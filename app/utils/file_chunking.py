import ast,json
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
    lines = source_code.splitlines()
    for node in tree.body:
        if isinstance(node,ast.FunctionDef):
            code = "\n".join(lines[node.lineno - 1 : node.end_lineno])

            chunks.append({
                "file_path": str(file_path),
                "type": "function",
                "name": node.name,
                "start_line": node.lineno,
                "end_line": node.end_lineno,
                "code": code,
            })
        elif isinstance(node,ast.AsyncFunctionDef):
            code = "\n".join(lines[node.lineno - 1 : node.end_lineno])

            chunks.append({
                "file_path": str(file_path),
                "type": "async_function",
                "name": node.name,
                "start_line": node.lineno,
                "end_line": node.end_lineno,
                "code": code,
            })
        elif isinstance(node,ast.ClassDef):
            code = "\n".join(lines[node.lineno - 1 : node.end_lineno])

            chunks.append({
                "file_path": str(file_path),
                "type": "class",
                "name": node.name,
                "start_line": node.lineno,
                "end_line": node.end_lineno,
                "code": code,
            })
        

    return chunks


def chunk_markdown(file_path: Path):
    readme=read_file(file_path)
    if not readme:
        return []
    lines=readme.splitlines()
    has_heading = any(line.lstrip().startswith("#") for line in lines)
    if not has_heading:
        return [{
            "file_path":str(file_path),
            "type":"markdown",
            "name":file_path.stem,
            "code":readme
        }]
    current_chunk=[]
    
    chunks=[]

    for line in lines:
        if line.lstrip().startswith('#'):
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk=[line]
        else:
            current_chunk.append(line)
    if current_chunk:
        chunks.append(current_chunk)
    result=[]
    for chunk in chunks:
        title = chunk[0].lstrip("#").strip()
        code = "\n".join(chunk)
        result.append({
                "file_path": str(file_path),
                "type": "markdown",
                "name": title,
                "code": code,
            })
    return result

def chunk_json(file_path: Path):
    content=read_file(file_path)
    if not content:
        return []
    try:
        json.loads(content)
    except json.JSONDecodeError:
        return []
    return [{
        "file_path": str(file_path),
        "type": "json",
        "name": file_path.stem,
        "code": content
    }]

    


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

        