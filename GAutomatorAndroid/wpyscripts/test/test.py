#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu wukenaihesos@gmail.com'

import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..\\..\\")))

from game_engine_test import GameEngineTest
from native_devices_test import DeviceTest
from reporter_test import ReportTest

if __name__ == '__main__':
    test_classes=[GameEngineTest,DeviceTest,ReportTest]

    loader=unittest.TestLoader()

    suites_list=[]

    for test_class in test_classes:
        suite=loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    suites=unittest.TestSuite(suites_list)
    runner=unittest.TextTestRunner()
    results=runner.run(suites)