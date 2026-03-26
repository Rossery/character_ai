from langchain_core.tools import tool

@tool("Edit", parse_docstring=True)
def edit_tool(file_path: str, old_string: str, new_string: str, replace_all: bool = False):
    """Performs exact string replacements in files.

    Usage:
    - You must use your `Read` tool at least once in the conversation before editing. This tool will error if you attempt an edit without reading the file.
    - When editing text from Read tool output, ensure you preserve the exact indentation (tabs/spaces) as it appears AFTER the line number prefix. The line number prefix format is: spaces + line number + tab. Everything after that tab is the actual file content to match. Never include any part of the line number prefix in the old_string or new_string.
    - ALWAYS prefer editing existing files in the codebase. NEVER write new files unless explicitly required.
    - Only use emojis if the user explicitly requests it. Avoid adding emojis to files unless asked.
    - The edit will FAIL if `old_string` is not unique in the file. Either provide a larger string with more surrounding context to make it unique or use `replace_all` to change every instance of `old_string`.
    - Use `replace_all` for replacing and renaming strings across the file. This parameter is useful if you want to rename a variable for instance.

    Args:
        file_path (str): The absolute path to the file to modify.
        new_string (str): The text to replace it with (must be different from old_string).
        old_string (str): The text to replace.
        replace_all (bool): Replace all occurences of old_string. Defaults to False.

    Returns:
        dict: Result with `file_path` and replacements count.

    """
    if not file_path or not isinstance(file_path, str):
        raise ValueError("file_path required")
    if old_string is None or new_string is None:
        raise ValueError("old_string and new_string required")
    if not isinstance(old_string, str) or not isinstance(new_string, str):
        raise ValueError("old_string and new_string must be strings")
    if old_string == new_string:
        raise ValueError("old_string and new_string must differ")
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    count = content.count(old_string)
    if replace_all:
        if count == 0:
            raise ValueError("old_string not found")
        updated = content.replace(old_string, new_string)
        with open(file_path, "w", encoding="utf-8", errors="ignore") as f:
            f.write(updated)
        return {"file_path": file_path, "replacements": count}
    else:
        if count == 0:
            raise ValueError("old_string not found")
        if count > 1:
            raise ValueError("old_string must be unique; use replace_all to replace multiple")
        updated = content.replace(old_string, new_string, 1)
        with open(file_path, "w", encoding="utf-8", errors="ignore") as f:
            f.write(updated)
        return {"file_path": file_path, "replacements": 1}
