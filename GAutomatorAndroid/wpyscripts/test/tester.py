#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

import time
import wpyscripts.manager as manager

if __name__ == '__main__':
    engine=manager.get_engine()

    for i in range(1,200):
        element = engine.find_element("Sample")
        result = engine.click(element)
        time.sleep(0.3)

        tree=engine._get_dump_tree()
        print(tree)
