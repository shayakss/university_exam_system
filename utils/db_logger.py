"""
Database Error Logger
Logs all database errors for debugging and monitoring
"""
import logging
import os
from datetime import datetime
import config


class DatabaseLogger:
    """Logger for database operations and errors"""
    
    def __init__(self):
        # Create logs directory
        log_dir = os.path.join(os.path.dirname(config.DATABASE_PATH), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # Setup logger
        self.logger = logging.getLogger('database')
        self.logger.setLevel(logging.INFO)
        
        # File handler - daily log files
        log_file = os.path.join(log_dir, f'database_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_query(self, query, params=None):
        """Log a database query"""
        self.logger.info(f"QUERY: {query} | PARAMS: {params}")
    
    def log_error(self, error, query=None, params=None):
        """Log a database error"""
        error_msg = f"ERROR: {error}"
        if query:
            error_msg += f" | QUERY: {query}"
        if params:
            error_msg += f" | PARAMS: {params}"
        self.logger.error(error_msg)
    
    def log_connection(self, status):
        """Log connection status"""
        self.logger.info(f"CONNECTION: {status}")
    
    def log_backup(self, success, path):
        """Log backup operation"""
        if success:
            self.logger.info(f"BACKUP SUCCESS: {path}")
        else:
            self.logger.error(f"BACKUP FAILED: {path}")


# Global logger instance
db_logger = DatabaseLogger()
