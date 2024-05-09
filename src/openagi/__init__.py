import logging
from datetime import datetime
from pathlib import Path

BASE_PATH = "logs"
pth = Path(BASE_PATH)
pth.mkdir(parents=True, exist_ok=True)
filename = (
    f'{pth.absolute()}/application_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'
)

# Setup basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(pathname)s:%(lineno)d:%(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    # filename=f'{pth.absolute()}/application_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log',
    # filemode="w",
)
