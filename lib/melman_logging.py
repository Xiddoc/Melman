import logging

MELMAN_LOGGER = "Melman"

# Create base logger which we will configure
logger = logging.getLogger(MELMAN_LOGGER)
logger.setLevel(logging.INFO)

# Create the logging output style
fmt = logging.Formatter("%(asctime)s %(levelname)s | %(message)s")

# Write to standard output, and apply our format
sh = logging.StreamHandler()
sh.setFormatter(fmt)
logger.handlers.clear()
logger.addHandler(sh)
