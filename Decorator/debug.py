from .__init__ import *


__all__ = ["debug"]


def debug(func: Callable):
    @functools.wraps(func)  # 保留原函數的元數據
    def wrapper(*args, **kwargs):
        print(
            f"before {func.__name__},args: {args},kwargs: {kwargs},locals: {locals()},globals: {globals()}")
        r = func(*args, **kwargs)
        print(
            f"after {func.__name__}, result: {r}")
        return r
    return wrapper
