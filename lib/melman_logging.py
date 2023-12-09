import logging

# Disable other logs
logging.root.setLevel(logging.INFO)


def get_logger(logger_name: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Create the logging output style
    fmt = logging.Formatter(
        fmt="%(asctime)s %(levelname)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S"
    )

    # Write to standard output, and apply our format
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.handlers.clear()
    logger.addHandler(sh)

    return logger
