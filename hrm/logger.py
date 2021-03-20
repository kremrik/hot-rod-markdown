import logging


__all__ = ["logger"]


def logger(name: str):
    _logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
    return _logger
