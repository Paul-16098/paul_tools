from .__init__ import *

import sys
import os


__all__ = ["noPrint"]


class ContextManagersNoPrint:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        return self._original_stdout

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def noPrint(func):
    @functools.wraps(func)  # 保留原函數的元數據
    def wrapper(*args, **kwargs):
        with ContextManagersNoPrint():  # 使用上下文管理器禁用打印
            return func(*args, **kwargs)
    return wrapper
