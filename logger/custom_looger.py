from datetime import datetime
import logging
import os

class CustomLogger:
    def __init__(self, log_dir='logs'):
        self.log_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.log_dir, exist_ok=True)

        log_file=f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        self.log_file_path = os.path.join(self.log_dir, log_file)
    
    def get_logger(self, name=__name__):
        logging.basicConfig(
            filename=self.log_file_path,
            format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
            level=logging.INFO
        )
        logger = logging.getLogger(name)
        return logger


