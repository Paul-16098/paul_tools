from .__init__ import *
from typing import Any


DEBUG: bool = False


__all__ = ["JsonEdit", "color", "typeToColor", "clipboard", "use"]


def JsonEdit(name: str | None = None):
    """
    Edit a JSON file interactively.
    Parameters:
    name (str | None): The name of the JSON file (without extension). If None, the user will be prompted to input a name.
    The function allows the user to:
    - View the current contents of the JSON file.
    - Add or update key-value pairs.
    - Delete key-value pairs.
    - Save the changes to the JSON file.
    Commands:
    - "save": Save the current state of the JSON file.
    - "del": Prompt the user to input a key to delete from the JSON file.
    - "del <key>": Delete the specified key from the JSON file.
    - "<key>=<value>": Add or update the specified key with the given value.
    - "<key>": Display the value associated with the specified key.
    The JSON file is saved in the current directory with the specified name.
    """
    import json
    import os
    import re
    import time

    dirRoot: str = "."

    def writeJson(mode: str = "wt"):
        with open(jsonPath, mode, encoding="utf-8") as f:
            json.dump(jsonDict, f, indent=2)
            f.write("\n")

    def save():
        """save json file."""
        jsonDict.update({
            "updata": time.strftime("%Y/%m/%d %H:%M UTC%z")
        })
        writeJson("wt")

    while name is None or name == "":
        name = input("name: ")
    jsonPath = os.path.join(dirRoot, f"{name}.json")

    jsonDict: dict[str, str]
    try:
        with open(jsonPath, "rt", encoding="utf-8") as f:
            # load load json file.
            jsonDict = json.load(f)
    except FileNotFoundError:
        jsonDict = {}
        writeJson("xt")

    def delFromKey(key: str | None = None):
        if key is None:
            delKey = input("key: ")
        else:
            delKey = key
        jsonDict.pop(delKey)
        del delKey

    try:
        while True:
            print(jsonDict)
            ip = input(">")
            match ip:
                case "save":
                    save()
                case "del":
                    delFromKey()
                case _:
                    reDel = re.search(r"^(del )(\S+)", ip)
                    if not reDel == None:
                        delFromKey(reDel.group(2))
                        continue

                    _ = ip.split("=")
                    key: str = ""
                    value: str | None = None

                    if len(_) == 2:
                        key, value = _
                    elif len(_) == 1:
                        key = _[0]
                        value = None

                    if key == "":
                        continue
                    elif value == None:
                        print(f"<{jsonDict.get(key, None)}")
                    else:
                        jsonDict.update({
                            key: eval(value)
                        })
                    del key, value
    except EOFError:
        pass


def color(*value: str, color: str = "") -> list[str]:
    """
    Adds ANSI color codes to the given strings using the colorama library.
    Args:
        *value (str): One or more strings to which the color will be applied.
        color (str, optional): The name of the color to apply. Defaults to an empty string, which means no color will be applied.
    Returns:
        list[str]: A list of strings with the specified color applied. If no color is specified, returns the original strings.
    Raises:
        ValueError: If the specified color is not defined in colorama.
    Example:
        >>> color("Hello", "World", color="red")
        ['\x1b[31m', 'Hello', 'World', '\x1b[39m']
    """
    import colorama
    colorama.init()

    # 將顏色轉換為大寫
    color = color.upper()

    if color == "":
        return list(value)

    # 檢查顏色是否在 colorama 中定義
    if not hasattr(colorama.Fore, color):
        raise ValueError(f"顏色 {repr(color)} 不存在於 colorama 中。")

    # 建立新的值列表
    new_value = list(value)
    # 插入顏色碼
    new_value.insert(0, getattr(colorama.Fore, color))
    # 添加重置顏色碼
    new_value.append(colorama.Fore.RESET)

    return new_value


def typeToColor(type: str) -> str:
    """
    Converts a given type string to a corresponding color string.

    Args:
        type (str): The type string to convert. Expected values are "ERROR", "ERR", "WARN", "WARNING", or any other string.

    Returns:
        str: The corresponding color string. Returns "RED" for "ERROR" or "ERR", "YELLOW" for "WARN" or "WARNING", and the uppercase version of the input type for any other string.
    """
    match type.upper():
        case "ERROR" | "ERR":
            return "RED"
        case "WARN" | "WARNING":
            return "YELLOW"
        case _:
            return type.upper()


class clipboard():
    """
    A utility class for interacting with the system clipboard using the pyperclip library.
    Methods
    -------
    copy_to_clipboard(text: str)
        Copies the given text to the system clipboard.
    paste_from_clipboard() -> str
        Retrieves and returns the current text from the system clipboard.
    """
    @staticmethod
    def copy_to_clipboard(text: str):
        """
        Copies the given text to the system clipboard.

        Args:
            text (str): The text to be copied to the clipboard.
        """
        import pyperclip
        pyperclip.copy(text)

    @staticmethod
    def paste_from_clipboard():
        """
        Retrieve text from the system clipboard using the pyperclip module.

        Returns:
            str: The text currently stored in the system clipboard.
        """
        import pyperclip
        return pyperclip.paste()


def use(obj: dict[str, Any]):
    """
    Updates the global namespace with the key-value pairs from the provided dictionary.

    Args:
        obj (dict[str, Any]): A dictionary containing key-value pairs to be added to the global namespace.

    Notes:
        - If a key from the dictionary already exists in the global namespace and is not None, it will be skipped.
        - This function logs the process at the debug level.

    Example:
        obj = {'var1': 10, 'var2': 'hello'}
        use(obj)
        print(var1)  # 10
    """
    logger.debug(f"use({obj})--init")
    for k, v in obj.items():
        if k in globals() and globals()[k] is not None:
            # raise
            # continue
            pass
        logger.debug(f"k({repr(k)}), v({repr(v)})")
        globals()[k] = v
