import os
import re
import uuid
import pexpect

class BashTerminal:
    """
    A keep-alive terminal for executing bash commands with state persistence 
    and exit code validation.
    """

    def __init__(self, cwd=None):
        """
        Initialize BashTerminal
        Args:
            cwd: Initial working directory, defaults to current directory
        """
        self.cwd = cwd or os.getcwd()

        # 使用 UUID 生成唯一的 Prompt 标记，防止命令输出内容与 Prompt 冲突
        self.unique_prompt = f"BASH_CTX_{uuid.uuid4().hex}>"

        # 启动 bash shell
        # echo=False 防止输入的命令被重复打印到输出中
        self.shell = pexpect.spawn("/bin/bash", encoding="utf-8", echo=False)

        # 设置环境变量 PS1，以便准确通过 expect 捕获命令结束
        self.shell.sendline(f'export PS1="{self.unique_prompt}"')
        self.shell.expect(self.unique_prompt, timeout=5)

        # 初始化目录
        if cwd:
            self.ensure_cwd(cwd)

    def ensure_cwd(self, target_dir):
        """
        Ensure the terminal is in the correct directory.
        Only executes 'cd' if the target directory is different from current state.
        """
        if target_dir and target_dir != self.cwd:
            # 执行 cd，这里不需要检查输出，假设路径存在
            # 实际生产中可能需要 try-catch cd 的结果，但这里依赖 execute 的通用报错即可
            self.shell.sendline(f'cd "{target_dir}"')
            self.shell.expect(self.unique_prompt, timeout=5)
            self.cwd = target_dir

    def execute(self, command, timeout=60):
        """
        Execute bash command and return output.
        Checks exit code ($?) to verify success.

        Args:
            command: Command to execute
            timeout: Timeout in seconds (default 60s)

        Returns:
            str: Command output, "Success", or Error message.
        """
        try:
            # 执行用户命令
            self.shell.sendline(command)
            self.shell.expect(self.unique_prompt, timeout=timeout)
            
            # 获取原始内容
            output = self.shell.before
            
            # 清理命令回显
            lines = output.split("\n")
            if lines and command.strip() in lines[0].strip():
                lines = lines[1:]

            # 保留左侧缩进
            command_output = "\n".join([line.rstrip() for line in lines]).strip()
            # 去除 ANSI 颜色控制字符
            command_output = re.sub(r"\x1b\[[0-9;]*m", "", command_output)

            # 检查退出码
            self.shell.sendline("echo $?")
            self.shell.expect(self.unique_prompt, timeout=5)
            
            exit_output = self.shell.before
            exit_lines = exit_output.split("\n")
            # 清理 echo $? 的回显
            if exit_lines and "echo $?" in exit_lines[0]:
                exit_lines = exit_lines[1:]
            
            try:
                # 获取第一行非空内容作为退出码
                exit_code_str = next((line.strip() for line in exit_lines if line.strip()), "0")
                exit_code = int(exit_code_str)
            except (ValueError, StopIteration):
                exit_code = 0  # 如果解析失败，保守默认成功，避免阻塞

            # 命令执行失败
            if exit_code != 0:
                error_msg = f"Command failed with exit code {exit_code}."
                if command_output:
                    return f"{command_output}\n\n({error_msg})"
                return error_msg

            # 命令成功，且没有输出
            if not command_output or len(command_output.strip()) == 0:
                return "Success"

            # 命令成功，且有输出
            return command_output

        except pexpect.TIMEOUT:
            # 发送中断信号 (Ctrl+C) 尝试恢复 Shell 状态
            self.shell.sendintr()
            # 尝试消耗掉中断后的输出
            try:
                self.shell.expect(self.unique_prompt, timeout=5)
            except:
                pass
            return f"Error: Command '{command}' timed out after {timeout} seconds."
            
        except Exception as e:
            return f"Error executing command: {str(e)}"

    def close(self):
        """Close the shell session."""
        if self.shell.isalive():
            try:
                self.shell.sendline("exit")
                self.shell.close()
            except:
                pass

    def __del__(self):
        self.close()