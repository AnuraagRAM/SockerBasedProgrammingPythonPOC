import logging
import sys


def root_log_fun():
    """
    Initialising the logger
    As of now I am using Standard out stream for the logs which is console
    :return: root handler
    """

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    return root


global root_log

root_log = root_log_fun()
