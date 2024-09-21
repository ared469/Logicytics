# If using the future annotations, it should be ontop of the file
# from __future__ import annotations

# Other Imports if needed or necessary go here

# This imports everything needed including the unique logger called by log - It is not optional
# To know more check the WiKi [Section 2, Coding Rules and Tips, Custom Libraries, __lib_class.py]
from __lib_class import *
log = Log(debug=DEBUG)
log_funcs = {
    "INFO": log.info,
    "WARNING": log.warning,
    "ERROR": log.error,
    "CRITICAL": log.critical,
    None: log.debug,
}

# Your actual code, must be able to run without any interference by outside actions
# USE log.info, log.error, log.warning and log.debug as well
# You can choose to use any other of the code without issues
# Example of said code:-
#
# def MOD_EXAMPLE() -> None:
#     """
#     This function MOD is used to log different types of messages.
#
#     It logs an error message, a warning message, an info message, and a debug message.
#
#     Parameters:
#     None
#
#     Returns:
#     None
#     """
#     log.error("This is an error")
#     log.warning("This is a warning")
#     log.info("This is a info message")
#     log.debug("This is a debug message")
#     pass  # Your code here with proper logging
#
#
# MOD_EXAMPLE()
