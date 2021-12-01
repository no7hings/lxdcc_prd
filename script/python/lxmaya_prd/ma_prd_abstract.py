# coding:utf-8
from lxutil_prd import utl_prd_abstract


class AbsMaObjOp(utl_prd_abstract.AbsObjOp):
    def __init__(self, obj):
        super(AbsMaObjOp, self).__init__(obj)


class AbsMaObjReferenceOp(utl_prd_abstract.AbsObjReferenceOp):
    def __init__(self, obj):
        super(AbsMaObjReferenceOp, self).__init__(obj)
