# coding:utf-8
from lxutil_prd import utl_prd_configure, utl_prd_objects, utl_prd_commands, utl_prd_core

from lxutil_prd import utl_prd_objects

scene_opt = utl_prd_objects.SceneOpt(project='cg7', stage='publish')
scene_opt.set_shots_build()
shot_opts = scene_opt.get_shot_opts()
for shot_opt in shot_opts:
    print shot_opt

