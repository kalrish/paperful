import logging
import sys

logger = logging.getLogger(
    __name__,
)
root_logger = logging.getLogger(
    name=None,
)


def set_up(
        ):
    for existing_handler in root_logger.handlers:
        root_logger.removeHandler(
            existing_handler,
        )

    handler = logging.StreamHandler(
        stream=sys.stderr,
    )

    formatter = logging.Formatter(
        datefmt=None,
        fmt='%(name)s: %(levelname)s: %(message)s',
        style='%',
    )

    handler.setFormatter(
        formatter,
    )

    root_logger.addHandler(
        handler,
    )


def set_level(
            level,
        ):
    root_logger.setLevel(
        level,
    )
