import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('myLogger')

logger.debug('This message is a debug message')
logger.info('This message is an informational message')
logger.warning('This message is a warning')
logger.error('This message is an error message')
logger.critical('This message is a critical message')


handler = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, handlers=[handler])

logger = logging.getLogger("MyLogger")

logger.debug("This message is a debug message")
logger.info("This message is a informational message")


console = logging.StreamHandler()
file_handler = logging.FileHandler("file.log")
logging.basicConfig(level=logging.DEBUG, handlers=[console, file_handler])

logger = logging.getLogger("MyLogger")

logger.debug("This message is a debug message")
logger.info("This message is a informational message")


console = logging.StreamHandler()
file = logging.FileHandler("file.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s:%(lineno)d %(message)s",
    handlers=[console, file],
)

logger = logging.getLogger("MyLogger")

logger.debug("This message is a debug message")
logger.info("This message is a informational message")


logger = logging.getLogger("MyLogger")
logger.setLevel(logging.DEBUG)

console = logging.StreamHandler()
file_handler = logging.FileHandler("file.log")

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s:%(lineno)d %(message)s"
)

console.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console)
logger.addHandler(file_handler)

logger.debug("This message is a debug message")
logger.info("This message is an informational message")

print(__name__)

