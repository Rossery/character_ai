from langchain_core.tools import tool

@tool("Read", parse_docstring=True)
def read_tool(file_path: str = "", offset: int = 1, limit: int = 200):
    """Reads a file from the local filesystem. You can access any file directly by using this tool.
    Assume this tool is able to read all files on the machine. If the User provides a path to a file assume that path is valid. It is okay to read a file that does not exist; an error will be returned.
    Usage:
        - The file_path parameter must be an absolute path, not a relative path
        - By default, it reads up to 2000 lines starting from the beginning of the file
        - You can optionally specify a line offset and limit (especially handy for long files), but it's recommended to read the whole file by not providing these parameters
        - Any lines longer than 2000 characters will be truncated
        - Results are returned using cat -n format, with line numbers starting at 1
        - This tool allows Claude Code to read images (eg PNG, JPG, etc). When reading an image file the contents are presented visually as Claude Code is a multimodal LLM.
        - This tool can read PDF files (.pdf). PDFs are processed page by page, extracting both text and visual content for analysis.
        - This tool can read Jupyter notebooks (.ipynb files) and returns all cells with their outputs, combining code, text, and visualizations.
        - You can call multiple tools in a single response. It is always better to speculatively read multiple potentially useful files in parallel
        - You will regularly be asked to read screenshots. If the user provides a path to a screenshot, ALWAYS use this tool to view the file at the path. This tool will work with all temporary file paths.
        - If you read a file that exists but has empty contents you will receive a system reminder warning in place of file contents.

    Args:
        file_path (str): The absolute path to the file to read.
        offset (int): The line number to start reading from. Only provide if the file is too large to read at once.
        limit (int): The number of lines to read. Only provide if the file is too large to read at once.

    Returns:
        str: File contents with line numbers in cat -n format.
    """
    file_path = file_path or ""
    if not file_path:
        raise ValueError("file_path required")
    offset = int(offset or 1)
    limit = int(limit or 200)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    start = max(0, offset - 1)
    end = min(len(lines), start + limit)
    out = []
    numw = len(str(end))
    for i in range(start, end):
        out.append("{}\t{}".format(str(i+1).rjust(numw), lines[i].rstrip('\\n')))
    return '\n'.join(out)
