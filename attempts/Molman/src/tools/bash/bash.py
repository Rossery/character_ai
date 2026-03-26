import os
import re
from typing import Optional, Dict

import logging
from langchain_core.tools import tool

from .bash_terminal import BashTerminal

logger = logging.getLogger(__name__)

# --- 会话管理 ---
_TERMINAL_SESSIONS: Dict[str, BashTerminal] = {}

class SecurityValidator:
    """安全校验器：管理白名单和危险模式"""
    
    # 白名单命令
    WHITELIST = {
        "ls", "cd", "pwd", "mkdir", "touch", "cp", "mv", "rm", "cat", 
        "head", "tail", "grep", "find", "echo", "date", "whoami",
        "git", "python", "pip", "pytest", "npm", "node", "tree"
    }

    # 危险模式黑名单
    FORBIDDEN_PATTERNS = [
        r"rm\s+-[rRf]+\s+/$",      # 禁止删除根目录
        r"rm\s+-[rRf]+\s+/\*",     # 禁止删除根目录内容
        r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;", # Fork bomb
        r">\s*/dev/sda",           # 禁止直接写设备
        r"mkfs",                   # 禁止格式化
        r"dd\s+if="                # 禁止 dd 操作
    ]

    @classmethod
    def validate(cls, command: str) -> bool:
        """验证命令是否合法"""
        # 拆分复合命令 (支持 &&, ||, ;, |)
        sub_commands = re.split(r'[;&|]+', command)
        
        for sub_cmd in sub_commands:
            sub_cmd = sub_cmd.strip()
            if not sub_cmd:
                continue
            
            # 获取命令动词 (第一个单词)
            parts = sub_cmd.split()
            cmd_root = parts[0] if parts else ""
            
            # 检查白名单
            if cmd_root not in cls.WHITELIST:
                logger.warning(f"Bash Security: Blocked command '{cmd_root}' not in whitelist.")
                return False

        # 检查危险正则模式
        for pattern in cls.FORBIDDEN_PATTERNS:
            if re.search(pattern, command):
                logger.warning(f"Bash Security: Blocked dangerous pattern in '{command}'.")
                return False
                
        return True
@tool("Bash", parse_docstring=True)
def bash_tool(
    command: str,
    cwd: Optional[str] = None,
    session_id: str = "default_session",
    reset_cwd: Optional[bool] = False,
):
    """Execute a standard bash command in a keep-alive shell, and return the output if successful or error message if failed.

    Use this tool to perform:
    - Create directories
    - Install dependencies
    - Start development server
    - Run tests and linting
    - Git operations

    Never use this tool to perform any harmful or dangerous operations.
	Safety: Only allow-listed commands are permitted.
    
    Args:
        command (str): The command to execute.
        reset_cwd (Optional[bool]): Whether to reset the current working directory to the project root directory. Defaults to False.

    Returns:
        str: Command output or error message formatted in a code block.
    """
    
    # 安全检查
    if not SecurityValidator.validate(command):
        return f"Error: Command '{command}' is not allowed by security policy."

    # 获取上下文信息
    work_dir = cwd or os.getcwd()

    # 会话管理
    global _TERMINAL_SESSIONS
    
    # 如果要求重置，或者会话不存在，则创建新会话
    if reset_cwd and session_id in _TERMINAL_SESSIONS:
        _TERMINAL_SESSIONS[session_id].close()
        del _TERMINAL_SESSIONS[session_id]

    if session_id not in _TERMINAL_SESSIONS:
        _TERMINAL_SESSIONS[session_id] = BashTerminal(cwd=work_dir)
    
    terminal = _TERMINAL_SESSIONS[session_id]

    # 同步工作目录
    terminal.ensure_cwd(work_dir)

    # 执行命令
    result = terminal.execute(command)

    # 格式化输出
    if result.startswith("Error:"):
        return f"```\n{result}\n```"
    elif result == "Success":
        return f"```\n{command} executed successfully.\n```"
    else:
        return f"```\n{result}\n```"
