import logging
import os

os.makedirs("logs", exist_ok=True)
# Configure logging
logging.basicConfig(
    filename="logs/app.log",  # Logs are saved in logs/app.log
    level=logging.INFO,  # Log INFO and higher levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Create logger instance
logger = logging.getLogger(__name__)
