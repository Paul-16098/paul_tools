from .__init__ import *
from typing import Any


DEBUG: bool = False


def JsonEdit(name: str | None = None):
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


def color(*value: Any, color: str = "") -> list[Any]:
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
    new_value.insert(0, eval(f"colorama.Fore.{color}"))
    # 添加重置顏色碼
    new_value.append(colorama.Fore.RESET)

    return new_value


def typeToColor(type: str) -> str:
    match type.upper():
        case "ERROR" | "ERR":
            return "RED"
        case "WARN" | "WARNING":
            return "YELLOW"
        case _:
            return type.upper()


class clipboard():
    @staticmethod
    def copy_to_clipboard(text: str):
        """複製文本到剪貼簿

        Args:
            text (str): 文本
        """
        import pyperclip
        pyperclip.copy(text)

    @staticmethod
    def paste_from_clipboard():
        """從剪貼簿粘貼文本

        Returns:
            str: 剪貼簿文本
        """
        import pyperclip
        return pyperclip.paste()


def use(obj: dict[str, Any]):
    logger.debug(f"use({obj})--init")
    for k, v in obj.items():
        if globals()[k] is not None:
            # raise
            continue
        logger.debug(f"k({repr(k)}), v({repr(v)})")
        globals()[k] = v
    logger.debug(f"use--end")
