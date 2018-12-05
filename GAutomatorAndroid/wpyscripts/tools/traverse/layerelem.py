"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""

__author__ = 'yifengcai'

class TouchElem(object):
    def __init__(self, scene_name, element):
        self.scene_name = scene_name
        self.element = element

        
    def __eq__(self, other):
        if self.scene_name == other.scene_name and self.element.object_name == other.element.object_name:
            return True
        else:
            return False
        
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.scene_name, self.element.object_name))


    def __str__(self):
        return "TouchElem (scene: %s, element: %s)" % (self.scene_name, self.element)
    
    
class ViewLayer(object):
    def __init__(self, touchelements=None):
        '''
        @param touchelements: TouchElem objects
        '''
        self.touchelems = touchelements if touchelements else []
        self.sort_elems_by_name()
        
    def sort_elems_by_name(self):
        self.touchelems.sort(cmp=_cmp_elem)
        
    def add_element(self, touch_element):
        self.touchelems.append(touch_element)
        
    def __eq__(self, other):
        if len(self.touchelems) != len(other.touchelems):
            return False
         
        for elem in self.touchelems:
            if elem not in other.touchelems:
                return False
             
        for elem in other.touchelems:
            if elem not in self.touchelems:
                return False
             
        return True
    
    def __ne__(self, other):
        return not self.__eq__(other)
 
    def __hash__(self):
        hash_list = map(hash, self.touchelems)
        return hash(tuple(hash_list))
    
    def __str__(self):
        return "ViewLayer (hash: %d, elem num: %d)" % (hash(self), len(self.touchelems))
    
    def fullstr(self):
        res1 = str(self)
        res2 = "\n".join([str(i) for i in self.touchelems])
        return "%s\n>>>\n%s\n<<<" % (res1, res2)
    
def _cmp_elem(a, b):
    if a.scene_name < b.scene_name:
        return -1
    elif a.scene_name > b.scene_name:
        return 1
    
    if a.element.object_name < b.element.object_name:
        return -1
    elif a.element.object_name > b.element.object_name:
        return 1
    else:
        return 0

    
def _test_touch_elem():
    from wpyscripts.wetest.element import Element
    
    elemA = Element("a/b/c", 1)
    elemB = Element("x/y/z", 2)
    elemC = Element("a/b/c", 3)
    
    telemA = TouchElem("scene1", elemA)
    telemB = TouchElem("scene1", elemB)
    telemC = TouchElem("scene1", elemC)
    
    list1 = [telemA, telemB]
    print("telemC in list? %s" % (telemC in list1))
    
    set1 = set()
    set1.add(telemA)
    set1.add(telemB)
    set1.add(telemC)
    print(set1)
    
def _test_view_layer():
    from wpyscripts.wetest.element import Element
    
    elemA = Element("a/b/c", 1)
    elemB = Element("x/y/z", 2)
    elemC = Element("a/b/c", 3)
    
    telemA = TouchElem("scene1", elemA)
    telemB = TouchElem("scene1", elemB)
    telemC = TouchElem("scene1", elemC)
    
    vlayer1 = ViewLayer()
    vlayer1.add_element(telemA)
    vlayer1.add_element(telemB)
    vlayer1.add_element(telemC)
    vlayer1.sort_elems_by_name()
    
    vlayer2 = ViewLayer()
    vlayer2.add_element(telemC)
    vlayer2.add_element(telemA)
    vlayer2.add_element(telemB)
    vlayer1.sort_elems_by_name()
    
    print("vlayer equals? %s" % (vlayer1 == vlayer2))
    print("vlayer1: ", vlayer1.fullstr())
    print("vlayer2: ", vlayer2.fullstr())
    
    set1 = set()
    set1.add(vlayer1)
    set1.add(vlayer2)
    print(set1)
    
    
if __name__ == "__main__":
    #_test_touch_elem()
    _test_view_layer()
    