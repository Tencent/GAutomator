#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

from testcase.tools import *

if __name__ == '__main__':
    engine.set_camera("UICamera(Clone)")
    version=engine.get_sdk_version()
    engine.swipe_position(245,832,387,695,20,2000)