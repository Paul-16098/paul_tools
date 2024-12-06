from .__init__ import *

# i18n
import json
import locale
from enum import Enum
import os
import time

__all__ = ["I18n"]


class I18n:
    """An internationalization (i18n) module for language translations.

    This module manages the loading and retrieval of localized strings based on
    the specified languages. It supports system language detection and fallback
    to default language files.
    By Paul-16098
    """

    ver = "1.0.0.0"

    LANG_MAP = {
        "sys": "sys",  # 這裡只設置為字符串，實際解析在需要時進行
        "zh": "zh_cn",
        "chinese (traditional)_hong kong sar": "zh_hk"
    }

    @staticmethod
    def langReplace(lang: str) -> str:
        """Replace language keys with their respective codes."""
        if lang == "sys":
            return I18n.langReplace(I18n.getSysLang())
        return I18n.LANG_MAP.get(lang, lang)

    @staticmethod
    def getSysLang() -> str:
        """Get the current system language code."""
        return str(locale.getlocale(locale.LC_CTYPE)[0]).lower()

    def __init__(self, Langs: list[str] | None = None, dirRoot: str = os.getcwd(), langJson: dict[str, dict[str, str]] = {}) -> None:
        self.DIR_ROOT = dirRoot
        self.DIR_LANGS_ROOT: str = os.path.join(self.DIR_ROOT, "langs")
        self.LANG_JSON: dict[str, str] = {}

        self.langs = Langs if Langs is not None else ["sys", "en_us"]
        self.langs = [self.langReplace(lang) for lang in self.langs]

        # #tag load
        for lang in reversed(self.langs):
            # print(lang, end=" ")
            dF = {
                "#": "{file_name}__{class_name}__{func_name}__{id}",
                "updata": time.strftime("%Y/%m/%d %H:%M UTC%z"),
                "any": "{}",
                "file_lang": lang,
            }
            try:
                with open(os.path.join(self.DIR_LANGS_ROOT, f"{lang}.json"), "r", encoding="utf8") as f:
                    fileJson = json.load(f)
            except FileNotFoundError:
                fileJson = dF  # 使用默認值
            except json.JSONDecodeError:
                fileJson = dF

            # breakpoint()
            self.LANG_JSON.update(fileJson)
            self.LANG_JSON.update(langJson.get(lang, {}))

    class Langs(Enum):
        """An Enum for system language keys."""
        LANG_JSON = -1
        updata = 0
        any = 1
        file_lang = 2

    def locale(self, raw: str | Langs, *args: object, **kwargs: object) -> str:
        """Get language text based on provided key.

        Args:
            raw (str | Langs): `Langs.XXX` or `"{file_name}__{class_name}__{func_name}__{id}"`
            kwargs: Format arguments.

        Returns:
            str: Language text or an error message.
        """
        text = raw.name if isinstance(raw, self.Langs) else raw

        langText = self.LANG_JSON.get(text)
        if langText is not None:
            return langText.format(*args, **kwargs)

        errText = f"{{ no {repr(text)} in lang file {repr(self.langs)} }}"
        return errText
