import logging
import os

class Logger:
    def __init__(self, log_file='vmi_tool.log'):
        # Create logs directory if it doesn't exist
        self.log_dir = 'logs'
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # Set up logging
        self.log_file = os.path.join(self.log_dir, log_file)
        self.logger = logging.getLogger('VMI_Tool')
        self.logger.setLevel(logging.DEBUG)  # Log level can be adjusted

        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)  # File logging level

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # Console logging level

        # Define format for logs
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        """Return the configured logger."""
        return self.logger
