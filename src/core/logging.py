import logging
from logging.handlers import RotatingFileHandler
import os
import json


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "security.log")

logger = logging.getLogger("security")
logger.setLevel(logging.INFO)
logger.propagate = False

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(process)d | %(module)s:%(lineno)d | %(message)s"
)

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5_000_000,  # 5MB
    backupCount=5,
    encoding="utf-8"
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)



# ---------------------------
# Helper function to log sensitive actions
# ---------------------------
def log_action(action, user_id, resource, resource_id, status, ip=None):
    """
    Central function to log sensitive actions.
    action: string e.g. "delete", "update"
    user_id: ID of the user performing the action
    resource: e.g. "objet", "user"
    resource_id: ID of the affected resource
    status: "success", "failed_permission", etc.
    ip: optional client IP
    """
    logger.info(json.dumps({
        "action": action,
        "user_id": user_id,
        "resource": resource,
        "resource_id": resource_id,
        "status": status,
        "ip": ip
    }))
