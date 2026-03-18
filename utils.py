from datetime import datetime
import os

LOG_DIR = "logs"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def get_log_file():
    return os.path.join(
        LOG_DIR,
        f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.enc"
    )

def get_timestamp():
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")