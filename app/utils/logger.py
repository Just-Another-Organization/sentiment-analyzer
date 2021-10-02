import logging
import sys
from pprint import pformat

from loguru import logger
from loguru._defaults import LOGURU_FORMAT


# Thanks to nkhitrov: https://github.com/tiangolo/fastapi/issues/1276#issuecomment-615877177


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def format_record(record: dict) -> str:
    format_string = LOGURU_FORMAT

    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"], indent=4, compact=True, width=88
        )
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"
    return format_string


logging.getLogger().handlers = [InterceptHandler()]

logger.configure(
    handlers=[{"sink": sys.stdout, "level": logging.DEBUG, "format": format_record}]
)

logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]


class Logger:

    def __init__(self, instance_name):
        self.instance_name = instance_name

    def format_log(self, log):
        return '''
        Instance: {instance_name}
        Log: {log}
        '''.format(instance_name=self.instance_name, log=log)

    def info(self, log):
        logger.info(self.format_log(log))

    def warning(self, log):
        logger.warning(self.format_log(log))

    def error(self, log):
        logger.error(self.format_log(log))

    def debug(self, log):
        logger.debug(self.format_log(log))

    def critical(self, log):
        logger.critical(self.format_log(log))

    def exception(self, log):
        logger.exception(self.format_log(log))
