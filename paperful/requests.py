import logging

logger = logging.getLogger(
    __name__,
)


def response_hook(
            response,
            *args,
            **kwargs,
        ):
    logger.debug(
        'response: status: %i %s',
        response.status_code,
        response.reason,
    )

    iterator = response.headers.items(
    )
    for header, value in iterator:
        logger.debug(
            'response: header: %s: %s',
            header,
            value,
        )

    if response.encoding:
        logger.debug(
            'response: %s: %s',
            response.encoding,
            response.text,
        )
