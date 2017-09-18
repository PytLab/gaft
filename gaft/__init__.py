import logging
import sys

from .engine import GAEngine

__version__ = '0.3.0'
__author__ = 'ShaoZhengjiang <shaozhengjiang@gmail.com>'

# Set root logger.
logger = logging.getLogger('gaft')
logger.setLevel(logging.INFO)
console_hdlr = logging.StreamHandler(sys.stdout)
console_hdlr.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s   %(levelname)-8s %(message)s')
console_hdlr.setFormatter(formatter)
logger.addHandler(console_hdlr)

