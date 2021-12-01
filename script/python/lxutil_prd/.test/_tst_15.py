# coding:utf-8
from lxutil_prd import utl_prd_objects

s = utl_prd_objects.Scene()

u = s.universe

asset = u.get_obj_type('asset')

print asset.get_variant('plf_path')
print asset.get_variant('prd.plf_path')

model_step = u.get_obj_type('model')

print model_step.get_variant('asset.prd.plf_path')
