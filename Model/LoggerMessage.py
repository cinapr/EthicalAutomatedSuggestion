class LoggerMessage:
    def log(self, message, callback=None):
        print(message)  # Log to the terminal
        if callback:
            callback(message)  # Log to the GUI
 