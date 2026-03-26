import glob, os
from langchain_core.tools import tool


@tool("Glob", parse_docstring=True)
def glob_tool(pattern: str = "**/*", path: str = os.getcwd()):
    """- Fast file pattern matching tool that works with any codebase size
    - Supports glob patterns like "**/*.js" or "src/**/*.ts"
    - Returns matching file paths sorted by modification time
    - Use this tool when you need to find files by name patterns
    - You have the capability to call multiple tools in a single response. It is always better to speculatively perform multiple searches as a batch that are potentially useful.

    Args:
        pattern (str): 匹配模式
        path (str): 根目录

    Returns:
        list[str]: 匹配的文件路径，按修改时间排序
    """
    path = path or os.getcwd()
    matches = glob.glob(os.path.join(path, pattern), recursive=True)
    return sorted(matches)
