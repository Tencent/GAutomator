# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com'

class Element(object):
    """
        in unity game Element is just GameObject
    Attributes:
        object_name:GameObject的全路径
        instance:GameObject Instance,the instance id of gameobject is always guarnnteed to be unique
    """

    def __init__(self, object_name, instance):
        self.__object_name = object_name
        self.__instance = instance

    @property
    def object_name(self):
        return self.__object_name

    @property
    def instance(self):
        return self.__instance

    def __str__(self):
        return "GameObject {0} Instance = {1}".format(self.object_name, self.instance)

    def __eq__(self, element):
        return hasattr(element, 'instance') and self.__instance == element.instance

    def __ne__(self, element):
        return not self.__eq__(element)

    def __repr__(self):
        return '<{0.__module__}.{0.__name__} (object_name="{1}", instance="{2}")>'.format(type(self), self.object_name, self.instance)

