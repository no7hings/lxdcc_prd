# coding:utf-8
from lxutil_prd import utl_prd_objects, utl_prd_commands, utl_prd_core

for i in [
    '/prod/cg7/work/shots/d10/d10160/lgt/lgt/houdini/d10160.lgt.lgt.v001.hip'
]:
    s = utl_prd_commands.set_scene_load_from_scene(
        i
    )
    entity = s.get_current_entity_obj()

    # element_type = universe.get_obj_type('element')
    # element_objs = element_type.get_objs()
    # for element_obj in element_objs:
    #     element_opt = utl_prd_objects.ElementOpt(element_obj)
    #     print element_opt
    #     # print element_opt.instance
    #     print element_opt.dcc_path
    #     print element_opt.plf_file_path
    #     # element_opt.set_variant_print()
    #     # print element_opt.instance
