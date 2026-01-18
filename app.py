from logger.custom_looger import CustomLogger
logger = CustomLogger().get_logger("app")

logger.info(f"Application started")