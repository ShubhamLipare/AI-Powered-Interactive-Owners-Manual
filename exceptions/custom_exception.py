import sys
import traceback

class CustomException(Exception):
    """Custom exception class that captures detailed error information including file and line number."""
    
    def __init__(self, message, details=None):
        """
        Initialize the exception.
        
        :param message: The error message.
        :param details: Optional additional details (e.g., dict of context).
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}
        
        # Capture traceback information at the point of exception creation
        exc_type, exc_value, exc_tb = sys.exc_info()
        if exc_tb:
            # Get the frame where the exception was raised
            tb_frame = exc_tb.tb_frame
            self.file_name = tb_frame.f_code.co_filename
            self.line_no = tb_frame.f_lineno
            self.function_name = tb_frame.f_code.co_name
        else:
            self.file_name = "unknown"
            self.line_no = 0
            self.function_name = "unknown"
    
    def __str__(self):
        """Return a formatted error message."""
        base_msg = f"Error in {self.file_name}:{self.line_no} ({self.function_name}): {self.message}"
        if self.details:
            base_msg += f" | Details: {self.details}"
        return base_msg
    
    def to_dict(self):
        """Return exception details as a dictionary for logging/serialization."""
        return {
            "message": self.message,
            "file_name": self.file_name,
            "line_no": self.line_no,
            "function_name": self.function_name,
            "details": self.details
        }
