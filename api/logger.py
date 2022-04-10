import logging
import os

from dotenv import load_dotenv
from slack_logger import SlackFormatter, SlackHandler

load_dotenv()

if os.getenv("DEBUG") == "FALSE":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(
        logging.Formatter(
            "%(levelname)8s : [%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S"
        )
    )
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler("debug.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(
            "%(levelname)8s : [%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S"
        )
    )
    logger.addHandler(file_handler)

    slack_handler = SlackHandler(
        username="logger",
        icon_emoji=":robot_face:",
        url=os.getenv("SLACK_ERROR_LOG_ENDPOINT"),
    )
    slack_handler.setLevel(logging.ERROR)
    slack_handler.setFormatter(
        SlackFormatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    )
    logger.addHandler(slack_handler)

else:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
