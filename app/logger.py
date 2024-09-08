import logging


# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
