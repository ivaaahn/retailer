import logging


class CustomFormatter(logging.Formatter):
    grey = "\x1b[37m"
    grey_bold = "\x1b[1:37m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[93m"
    yellow_bold = "\x1b[1;93m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    green = "\033[92m"
    green_bold = "\033[1;92m"
    reset = "\x1b[0m"
    white = "\x1b[97m"
    white_bold = "\x1b[1;97m"

    def __init__(self, fmt):
        super().__init__()

        split = fmt.split(":")
        self.lvl = split[0]
        self.other = ":".join(split[1:])

        self._fmt = fmt

        self.lvl2color = {
            logging.DEBUG: (self.grey_bold, self.grey),
            logging.INFO: (self.green_bold, self.white),
            logging.WARNING: (self.yellow_bold, self.yellow),
            logging.ERROR: (self.bold_red, self.red),
            logging.CRITICAL: (self.bold_red, self.bold_red),
        }

    def format(self, record):
        color = self.lvl2color[record.levelno]

        fmt = (
            color[0]
            + self.lvl
            + ":"
            + self.reset
            + color[1]
            + self.other
            + self.reset
        )

        formatter = logging.Formatter(fmt)
        return formatter.format(record)
