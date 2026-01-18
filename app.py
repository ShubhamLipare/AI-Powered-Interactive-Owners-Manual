from logger.custom_looger import CustomLogger
from exceptions.custom_exception import CustomException
logger = CustomLogger().get_logger("app")

logger.info(f"Application started")

try:
    # Simulate some operation that raises an exception
    1 / 0
except ZeroDivisionError as e:
    custom_exc = CustomException("Division by zero error occurred", details={"operation": "1 / 0"})
    logger.error(str(custom_exc))
    logger.debug(f"Exception details: {custom_exc.to_dict()}")