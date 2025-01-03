from loguru import logger


__version__ = "1.0.0"
DEBUG = False

if not DEBUG:
    from sys import stdout
    logger.remove()
    logger.add("./log/log_paul-tools_{time}.log")
    logger.add(stdout, level=("DEBUG" if DEBUG else "INFO"),
               format="<level>{message}</level>")
else:
    pass
