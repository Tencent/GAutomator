#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

from .tools import *

import pytest
# content of test_class.py
class TestClass:
    def test_one(self):
        print('one')
        x = "this"
        assert 'h' in x
    def test_two(self):
        print('two')
        x = "hello"
        assert hasattr(x, 'check')

if __name__ == '__main__':
    pytest.main("-q --html=a.html")
# btn=engine.find_element("CallPC")
# engine.click(btn)
#
# engine.click("CallPC")
