import logging

# Create logger
logger = logging.getLogger("lvs_logger")

# Set level
logger.setLevel(logging.INFO)

# Create console handler
console_handler = logging.StreamHandler()

# Format of logs
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

console_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(console_handler)
