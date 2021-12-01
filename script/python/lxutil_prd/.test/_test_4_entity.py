# coding:utf-8
from lxutil import commands

from lxutil_prd import utl_prd_objects, utl_prd_commands, utl_prd_core

for i in [
    '/prod/cg7/work/shots/d10/d10160/lgt/lgt/houdini/d10160.lgt.lgt.v001.hip'
]:
    s = utl_prd_commands.set_scene_load_from_scene(
        i
    )
    entity = s.get_current_entity_obj()
    shot_opt = utl_prd_objects.ShotOpt(entity)
    shot_opt.set_manifests_build()
