from logger.custom_looger import CustomLogger
from exceptions.custom_exception import CustomException

logger = CustomLogger().get_logger(__name__)
logger.info("Ingestion module loaded successfully.")

