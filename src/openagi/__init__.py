import logging
from datetime import datetime
from pathlib import Path

BASE_PATH = "logs"
pth = Path(BASE_PATH)
pth.mkdir(parents=True, exist_ok=True)
filename = (f'{pth.absolute()}/application_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')

# Setup basic logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s::%(thread)d::%(pathname)s:%(lineno)d:%(funcName)s:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=f'{pth.absolute()}/application_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log',
    filemode="w",
)
print(f"Logs stored at {filename}")
logging.info(f"Logs stored at {pth.absolute()}")
