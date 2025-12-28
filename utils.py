import logging
import logging.handlers
import os
import json
import time
from datetime import datetime, timedelta

from config import LOG_FILE, LOG_RETENTION_DAYS, LAST_VIDEO_FILE, LAST_HEARTBEAT_FILE


def setup_logging():
    """Configure rotating file logging."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Rotating file handler
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5  # 5 MB
    )
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def load_last_video_id():
    if not os.path.exists(LAST_VIDEO_FILE):
        return None
    try:
        with open(LAST_VIDEO_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("video_id")
    except Exception as e:
        logging.error(f"Failed to read {LAST_VIDEO_FILE}: {e}")
        return None


def save_last_video_id(video_id):
    try:
        with open(LAST_VIDEO_FILE, "w", encoding="utf-8") as f:
            json.dump({"video_id": video_id}, f)
    except Exception as e:
        logging.error(f"Failed to write {LAST_VIDEO_FILE}: {e}")


def should_send_heartbeat(hours=24):
    now = datetime.utcnow()

    if not os.path.exists(LAST_HEARTBEAT_FILE):
        return True

    try:
        with open(LAST_HEARTBEAT_FILE, "r", encoding="utf-8") as f:
            ts = f.read().strip()
            last = datetime.fromisoformat(ts)
    except Exception as e:
        logging.error(f"Failed to read {LAST_HEARTBEAT_FILE}: {e}")
        return True

    return (now - last) >= timedelta(hours=hours)


def mark_heartbeat_sent():
    now = datetime.utcnow()
    try:
        with open(LAST_HEARTBEAT_FILE, "w", encoding="utf-8") as f:
            f.write(now.isoformat())
    except Exception as e:
        logging.error(f"Failed to write {LAST_HEARTBEAT_FILE}: {e}")


def cleanup_old_logs(log_directory=".", days=7):
    """Delete log files older than N days."""
    now = time.time()
    cutoff = now - (days * 86400)  # seconds in a day

    for filename in os.listdir(log_directory):
        if filename.startswith(os.path.basename(LOG_FILE)):
            path = os.path.join(log_directory, filename)
            if os.path.isfile(path):
                try:
                    mtime = os.path.getmtime(path)
                    if mtime < cutoff:
                        os.remove(path)
                        logging.info(f"Deleted old log file: {filename}")
                except Exception as e:
                    logging.error(f"Failed to delete {filename}: {e}")
