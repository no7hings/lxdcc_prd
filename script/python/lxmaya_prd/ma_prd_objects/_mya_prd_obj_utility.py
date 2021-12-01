# coding:utf-8
from lxmaya_prd import ma_prd_abstract


class ObjOpt(ma_prd_abstract.AbsMaObjOp):
    def __init__(self, obj):
        super(ObjOpt, self).__init__(obj)


class ObjReferenceOp(ma_prd_abstract.AbsMaObjReferenceOp):
    def __init__(self, obj):
        super(ObjReferenceOp, self).__init__(obj)
