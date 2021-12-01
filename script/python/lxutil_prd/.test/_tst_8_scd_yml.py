# coding:utf-8
from lxutil_prd import utl_prd_objects, utl_prd_commands, utl_prd_core

for i in [
    '/l/prod/cg7/work/shots/d10/d10010/lgt/lgt/houdini/d10010.lgt.lgt.v003.hip'
]:
    s = utl_prd_commands.set_scene_load_from_scene(
        i
    )
    entity = s.get_current_entity_obj()
    shot_opt = utl_prd_objects.ShotOpt(entity)
    shot_opt.set_manifests_build()
    manifests = shot_opt.get_anm_scm_manifests()
    for manifest in manifests:
        print manifest
