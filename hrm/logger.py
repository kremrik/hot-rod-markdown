import logging


__all__ = ["logger"]


def logger(name: str):
    _logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(pathname)s | %(message)s"  # noqa E501
    )
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
    return _logger
