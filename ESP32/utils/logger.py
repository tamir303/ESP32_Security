import sys
import time

class Logger:
    # ANSI escape codes for colors
    COLORS = {
        "INFO": "\033[37m",    # White
        "DEBUG": "\033[33m",   # Yellow
        "WARNING": "\033[33m", # Yellow
        "ERROR": "\033[31m",   # Red
        "RESET": "\033[0m"     # Reset
    }

    def __init__(self, name=None, level="DEBUG"):
        self.name = name if name else "MAIN"
        self.level = level
        self.levels = {
            "DEBUG": 0,
            "INFO": 1,
            "WARNING": 2,
            "ERROR": 3,
        }

    def log(self, level, message):
        """
        Log a message with the given level and appropriate color.
        """
        if self.levels[level] >= self.levels[self.level]:
            timestamp = time.localtime()  # Use RTC if available
            formatted_time = f"{timestamp[3]:02}:{timestamp[4]:02}:{timestamp[5]:02}"
            color = self.COLORS.get(level, self.COLORS["RESET"])
            reset = self.COLORS["RESET"]

            # Print the log with a newline before each message
            print(f"{color}[{formatted_time}] [{level}] [{self.name}] {message}{reset}")

    def debug(self, message):
        self.log("DEBUG", message)

    def info(self, message):
        self.log("INFO", message)

    def warning(self, message):
        self.log("WARNING", message)

    def error(self, message):
        self.log("ERROR", message)
