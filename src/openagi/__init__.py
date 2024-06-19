import logging
import os
from datetime import datetime
from pathlib import Path

# Define custom formatter with ANSI escape codes for colors
class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[94m",    # Blue
        logging.INFO: "\033[92m",     # Green
        logging.WARNING: "\033[93m",  # Yellow
        logging.ERROR: "\033[91m",    # Red
        logging.CRITICAL: "\033[95m", # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, self.RESET)
        log_fmt = f"{log_color}%(asctime)s :%(funcName)s: %(message)s{self.RESET}"
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


BASE_PATH = "logs"
pth = Path(BASE_PATH)
pth.mkdir(parents=True, exist_ok=True)
filename = f'{pth.absolute()}/application_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'

LOG_LEVEL = getattr(
    logging,
    os.environ.get("OPENAGI_LOG_LEVEL", "INFO").upper(),
    logging.INFO,
)

console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)
console_handler.setFormatter(ColoredFormatter())
# Setup basic logging configuration
logging.basicConfig(
    level=LOG_LEVEL,
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(filename=filename),
        console_handler
    ]
)
