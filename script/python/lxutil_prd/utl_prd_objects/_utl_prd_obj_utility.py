# coding:utf-8
from lxutil_prd import utl_prd_configure, utl_prd_abstract

from lxutil_prd.utl_prd_objects import _utl_prd_obj_scene


class ObjTypeOp(utl_prd_abstract.AbsObjTypeOp):
    def __init__(self, obj_type):
        super(ObjTypeOp, self).__init__(obj_type)


class ObjOpt(utl_prd_abstract.AbsObjOp):
    OBJ_TYPE_OP_CLASS = ObjTypeOp
    def __init__(self, obj):
        super(ObjOpt, self).__init__(obj)


class ObjReferenceOp(utl_prd_abstract.AbsObjReferenceOp):
    OBJ_TYPE_OP_CLASS = ObjTypeOp
    def __init__(self, obj):
        super(ObjReferenceOp, self).__init__(obj)


class ObjStorageOp(utl_prd_abstract.AbsObjStorageOp):
    OBJ_TYPE_OP_CLASS = ObjTypeOp
    def __init__(self, obj):
        super(ObjStorageOp, self).__init__(obj)


class IstOpt(utl_prd_abstract.AbsIstOpt):
    def __init__(self, obj):
        super(IstOpt, self).__init__(obj)


class ElementOpt(utl_prd_abstract.AbsElementOpt):
    IST_OPT_CLASS = IstOpt
    def __init__(self, obj):
        super(ElementOpt, self).__init__(obj)


class ContainerOpt(utl_prd_abstract.AbsContainerOpt):
    OBJ_TYPE_OP_CLASS = ObjTypeOp
    IST_OPT_CLASS = IstOpt
    ELEMENT_OPT_CLASS = ElementOpt
    def __init__(self, obj):
        super(ContainerOpt, self).__init__(obj)


class ManifestOpt(utl_prd_abstract.AbsManifestOpt):
    CONTAINER_OPT_CLASS = ContainerOpt
    def __init__(self, obj):
        super(ManifestOpt, self).__init__(obj)


class AssetOpt(utl_prd_abstract.AbsAssetQuery):
    OBJ_TYPE_OP_CLASS = ObjTypeOp
    #
    ENTITY_TYPE_NAME = utl_prd_configure.ObjType.ASSET
    def __init__(self, obj):
        super(AssetOpt, self).__init__(obj)


class ShotOpt(utl_prd_abstract.AbsShotOpt):
    OBJ_TYPE_OP_CLASS = ObjTypeOp
    #
    ENTITY_TYPE_NAME = utl_prd_configure.ObjType.SHOT
    MANIFEST_OPT_CLASS = ManifestOpt
    def __init__(self, obj):
        super(ShotOpt, self).__init__(obj)


class SceneOpt(utl_prd_abstract.AbsSceneOpt):
    SCENE_CLASS = _utl_prd_obj_scene.Scene
    SHOT_OPT_CLASS = ShotOpt
    def __init__(self, **kwargs):
        super(SceneOpt, self).__init__(**kwargs)


class AssetsOpt(utl_prd_abstract.AbsAssetsOpt):
    ENTITY_TYPE_NAME = utl_prd_configure.ObjType.ASSET
    #
    SCENE_CLASS = _utl_prd_obj_scene.Scene
    ENTITY_OPT_CLASS = AssetOpt
    def __init__(self, **kwargs):
        super(AssetsOpt, self).__init__(**kwargs)
