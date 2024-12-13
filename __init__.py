from sys import stdout
from loguru import logger


__version__ = "1.0.0"
DEBUG = False

logger.remove()
logger.add("./log/log_paul-tools_{time}.log", compression="zip")
logger.add(stdout, level=("DEBUG" if DEBUG else "INFO"),
           format="<level>{message}</level>")
del stdout
