# coding: utf-8
import sys, logging

logger = logging.getLogger('remarks')
logger.addHandler(logging.StreamHandler(sys.stderr))
logger.setLevel(logging.INFO)
