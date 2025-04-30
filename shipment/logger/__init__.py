# Goal of this code:
#To create a log file (with a timestamped name) inside a log/ folder in your project and store logs in it using Python’s built-in logging module.
#Logging is used to record events that happen when your code runs — for debugging, monitoring, and tracking the flow of your application.

import logging
import os
from datetime import datetime
from from_root import from_root

LOG_FILE=f"{datetime.now().strftime("%m_%d_%y_%H_%M_%S")}.log"

log_path=os.path.join(from_root(),'log',LOG_FILE)

os.mkdirs(log_path,exist_ok=True)

LOG_FILE_PATH=os.path.join(log_path,LOG_FILE)

logging.basicConfig(
  filename=LOG_FILE_PATH,
  format="[%(asctime)s] %(name)s-%(levelname)s-%(message)s",
  level=logging.INFO
)