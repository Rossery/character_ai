from langchain_core.tools import tool
import logging

logger = logging.getLogger(__name__)


@tool("Write", parse_docstring=True)
def write_tool(content: str, file_path: str):
    """Writes a file to the local filesystem.

    Usage:
    - This tool will overwrite the existing file if there is one at the provided path.
    - If this is an existing file, you MUST use the Read tool first to read the file's contents. This tool will fail if you did not read the file first.
    - ALWAYS prefer editing existing files in the codebase. NEVER write new files unless explicitly required.
    - NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.
    - Only use emojis if the user explicitly requests it. Avoid writing emojis to files unless asked.

    Args:
        content (str): The content to write to the file.
        file_path (str): The absolute path to the file to write.

    Returns:
        dict: Result info containing `file_path` and bytes written.
    """
    if content is None or file_path is None:
        raise ValueError("content and file_path required")
    if not isinstance(file_path, str):
        raise ValueError("file_path must be a string")
    import os
    try:
        dirpath = os.path.dirname(file_path)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)
        data = content if isinstance(content, str) else str(content)
        logger.info(f"Writing {len(data)} bytes to {os.path.abspath(file_path)}")
        with open(file_path, "w", encoding="utf-8", errors="ignore") as f:
            f.write(data)
    except Exception as e:
        logger.error(f"Error writing to {file_path}: {e}")
        raise e
    return {"file_path": file_path, "bytes": len(data)}
