import logging
import logging.handlers
from loguru import logger
import functools
import os

from config import cfg

logger.add(
    os.path.join("logs", cfg.logging.filename),
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    rotation="1 week",
    retention="2 months",
    level=cfg.logging.level,
)


def logger_wraps(*, entry=True, exit=True, level="DEBUG"):
    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)
            if entry:
                logger_.log(
                    level, "Entering '{}' (args={}, kwargs={})", name, args, kwargs
                )
            result = func(*args, **kwargs)
            if exit:
                logger_.log(level, "Exiting '{}' (result={})", name, result)
            return result

        return wrapped

    return wrapper


logging.basicConfig(
    level=cfg.logging.level,
)
rotating_file_handler = logging.handlers.RotatingFileHandler(
    filename=os.path.join("logs", cfg.logging.filename),
    maxBytes=100_000,
    backupCount=9,
)

rotating_file_handler.setFormatter(
    logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d | %(levelname)-8s | %(module)s:%(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
rotating_file_handler.setLevel(cfg.logging.level)

default_logger = logging.getLogger()
default_logger.addHandler(rotating_file_handler)

logger = default_logger


def log_deco(
    _func=None, *, exit=True, level=logging.DEBUG, my_logger: logging.Logger = default_logger
):
    def decorator_log(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger()
            try:
                if my_logger is None:
                    first_args = next(
                        iter(args), None
                    )  # capture first arg to check for `self`
                    logger_params = [  # does kwargs have any logger
                        x for x in kwargs.values() if isinstance(x, logging.Logger)
                    ] + [  # # does args have any logger
                        x for x in args if isinstance(x, logging.Logger)
                    ]
                    if hasattr(first_args, "__dict__"):  # is first argument `self`
                        logger_params = (
                            logger_params
                            + [
                                x
                                for x in first_args.__dict__.values()  # does class (dict) members have any logger
                                if isinstance(x, logging.Logger)
                            ]
                        )
                    h_logger = next(
                        iter(logger_params), logger
                    )  # get the next/first/default logger
                else:
                    h_logger = my_logger  # logger is passed explicitly to the decorator

                logger = h_logger

                args_repr = [repr(a) for a in args]
                kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
                signature = ", ".join(args_repr + kwargs_repr)
                logger.log(
                    level, f"function {func.__name__} called with args {signature}"
                )
            except Exception:
                pass

            try:
                result = func(*args, **kwargs)
                if exit:
                    logger.log(level, f"Exiting '{func.__name__}' (result={result})")
                return result
            except Exception as e:
                logger.exception(
                    f"Exception raised in {func.__name__}. exception: {str(e)}"
                )
                raise e

        return wrapper

    if _func is None:
        return decorator_log
    else:
        return decorator_log(_func)


logger_wraps = log_deco
