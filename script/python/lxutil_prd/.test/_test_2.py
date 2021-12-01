# coding:utf-8
import glob

from lxutil_prd import utl_prd_objects, utl_prd_commands, utl_prd_core


s = utl_prd_commands.set_scene_load_from_scene('/prod/cg7/*')

u = s.universe

entity_type = u.get_obj_type('shot')

asset_type_op = utl_prd_objects.ObjTypeOp(entity_type)

v = asset_type_op.get_variant('self.plf_path')
glob_pattern = utl_prd_core._var__get_glob_pattern_(v)
results = glob.glob(glob_pattern)
# print results

step_category = u.get_obj_category('step')

step_types = step_category.get_types()

for step_type in step_types:
    obj_type_op = utl_prd_objects.ObjTypeOp(step_type)
    # print obj_type_op
    v = obj_type_op.get_variant('self.asset.plf_path')
    if v is not None:
        print v
        glob_pattern = utl_prd_core._var__get_glob_pattern_(v)
        results = glob.glob(glob_pattern)
        print step_type
        print results
