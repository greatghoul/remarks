# coding: utf-8
import sys, logging

log = logging.getLogger('remarks')
log.addHandler(logging.StreamHandler(sys.stderr))
log.setLevel(logging.INFO)