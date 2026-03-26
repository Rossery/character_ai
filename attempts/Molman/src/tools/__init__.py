from typing import Callable, List

from tools.bash.bash import bash_tool
from tools.edit.edit import edit_tool
from tools.fs.grep import grep_tool
from tools.fs.ls import ls_tool
from tools.fs.tree import tree_tool
from tools.glob.glob import glob_tool
from tools.read.read import read_tool
from tools.todo_write.todo_write import todo_write_tool
from tools.write.write import write_tool


def get_all_tools() -> List[Callable]:
    """Get all available tools for the agent.
    
    Returns:
        List of all LangChain-compatible tools configured from tools.json.
    """
    tools = [
        bash_tool,
        edit_tool,
        grep_tool,
        ls_tool,
        glob_tool,
        read_tool,
        tree_tool,
        todo_write_tool,
        write_tool,
    ]
    return tools


__all__ = [
    "get_all_tools",
    "bash_tool",
    "edit_tool",
    "grep_tool",
    "ls_tool",
    "glob_tool",
    "read_tool",
    "tree_tool",
    "todo_write_tool",
    "write_tool",
]
