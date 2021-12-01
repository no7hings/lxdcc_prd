# coding:utf-8
from lxobj.core_objects import _obj_utility

from .. import utl_prd_abstract


class Scene(utl_prd_abstract.AbsObjScene):
    UNIVERSE_CLASS = _obj_utility.ObjUniverse
    def __init__(self):
        super(Scene, self).__init__()
