import logging


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    green = "\033[92m"
    reset = "\x1b[0m"

    def __init__(self, fmt):
        super().__init__()

        split = fmt.split(":")
        self.lvl = split[0]
        self.other = "".join(split[1:])

        self._fmt = fmt

        self.lvl2color = {
            logging.DEBUG: self.grey,
            logging.INFO: self.green,
            logging.WARNING: self.yellow,
            logging.ERROR: self.red,
            logging.CRITICAL: self.bold_red,
        }

    def format(self, record):
        color = self.lvl2color[record.levelno]

        fmt = color + self.lvl + ":" + self.reset + self.other

        formatter = logging.Formatter(fmt)
        return formatter.format(record)
