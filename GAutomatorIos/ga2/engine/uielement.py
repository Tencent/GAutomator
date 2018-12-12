# -*- coding: UTF-8 -*-


class UIElement():
    """
        in unity game Element is just GameObject
    Attributes:
        object_name:GameObject的全路径
        instance:GameObject Instance,the instance id of gameobject is always guarnnteed to be unique
    """

    def __init__(self, element,bound):
        self.__element = element
        self.__bound = bound

    @property
    def element(self):
        return self.__element

    @property
    def bound(self):
        return self.__bound

    def __str__(self):
        return "element {0} bound = {1}".format(self.element, self.bound)

    def __eq__(self, uielement):
        return hasattr(uielement, 'element') and self.element.instance == uielement.element.instance

    def __ne__(self, uielement):
        return not self.__eq__(uielement)

    def __repr__(self):
        return '<{0.__module__}.{0.__name__} (object_name="{1}", instance="{2}", bound="{3}")>'.format(type(self), self.element.object_name, self.element.instance,self.element.bound)

