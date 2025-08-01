"""
Logging module
"""


import logging
import logging.handlers
import re
from enum import Enum


class ColorCodes(Enum):
    """
    Definitions of the codes
    """

    GREEN = "\x1b[1;32m"
    YELLOW = "\x1b[33;21m"
    RED = "\x1b[31;21m"
    BOLD_RED = "\x1b[31;1m"
    BLUE = "\x1b[1;34m"
    LIGHT_BLUE = "\x1b[1;36m"
    PURPLE = "\x1b[1;35m"
    RESET = "\x1b[0m"


class ColorizedArgsFormatter(logging.Formatter):
    """
    Formatter for the color logs
    """

    arg_colors = [ColorCodes.PURPLE.value, ColorCodes.LIGHT_BLUE.value]
    level_fields = ["levelname", "levelno"]
    level_to_color = {
        logging.DEBUG: ColorCodes.BLUE.value,
        logging.INFO: ColorCodes.GREEN.value,
        logging.WARNING: ColorCodes.YELLOW.value,
        logging.ERROR: ColorCodes.RED.value,
        logging.CRITICAL: ColorCodes.BOLD_RED.value,
    }

    def __init__(self, fmt: str, datefmt: str = None):
        super().__init__()
        self.level_to_formatter = {}
        self.datefmt = datefmt

        def add_color_format(level: int):
            """
            Adding color format of the certain level
            """
            color = ColorizedArgsFormatter.level_to_color[level]
            _format = fmt
            for fld in ColorizedArgsFormatter.level_fields:
                search = r"(%\(" + fld + r"\).*?s)"
                _format = re.sub(search, f"{color}\\1{ColorCodes.RESET.value}", _format)
            formatter = logging.Formatter(_format, datefmt=self.datefmt)
            self.level_to_formatter[level] = formatter

        add_color_format(logging.DEBUG)
        add_color_format(logging.INFO)
        add_color_format(logging.WARNING)
        add_color_format(logging.ERROR)
        add_color_format(logging.CRITICAL)

    @staticmethod
    def rewrite_record(record: logging.LogRecord):
        """
        Changing message to add colors
        """
        if not BraceFormatStyleFormatter.is_brace_format_style(record):
            return

        msg = record.msg
        msg = msg.replace("{", "_{{")
        msg = msg.replace("}", "_}}")
        placeholder_count = 0
        # add ANSI escape code for next alternating color before each formatting parameter
        # and reset color after it.
        while True:
            if "_{{" not in msg:
                break
            color_index = placeholder_count % len(ColorizedArgsFormatter.arg_colors)
            color = ColorizedArgsFormatter.arg_colors[color_index]
            msg = msg.replace("_{{", color + "{", 1)
            msg = msg.replace("_}}", "}" + ColorCodes.RESET.value, 1)
            placeholder_count += 1

        record.msg = msg.format(*record.args)
        record.args = []

    def format(self, record):
        """
        Formatting record
        """
        orig_msg = record.msg
        orig_args = record.args
        formatter = self.level_to_formatter.get(record.levelno)
        self.rewrite_record(record)
        formatted = formatter.format(record)

        # restore logs record to original state for other handlers
        record.msg = orig_msg
        record.args = orig_args
        return formatted


class BraceFormatStyleFormatter(logging.Formatter):
    """
    Formatter for Brace style
    """

    def __init__(self, fmt: str):
        super().__init__()
        self.formatter = logging.Formatter(fmt)

    @staticmethod
    def is_brace_format_style(record: logging.LogRecord):
        """
        Checking if record follows to Brace format style
        """
        if len(record.args) == 0:
            return False

        msg = record.msg
        if "%" in msg:
            return False

        count_of_start_param = msg.count("{")
        count_of_end_param = msg.count("}")

        if count_of_start_param != count_of_end_param:
            return False

        if count_of_start_param != len(record.args):
            return False

        return True

    @staticmethod
    def rewrite_record(record: logging.LogRecord):
        """
        Rewriting logger record
        """
        if not BraceFormatStyleFormatter.is_brace_format_style(record):
            return

        record.msg = record.msg.format(*record.args)
        record.args = []

    def format(self, record):
        """
        Formatting message
        """
        orig_msg = record.msg
        orig_args = record.args
        self.rewrite_record(record)
        formatted = self.formatter.format(record)

        # restore logs record to original state for other handlers
        record.msg = orig_msg
        record.args = orig_args
        return formatted
