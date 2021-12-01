# coding:utf-8
from lxutil_prd import utl_prd_objects, utl_prd_commands, utl_prd_core

for i in [
    '/prod/cg7/work/shots/d10/d10010/rlo/rough_layout/maya/scenes/d10010.rlo.rough_layout.v002.ma'
]:
    s = utl_prd_commands.set_scene_load_from_scene(
        i
    )

    # s._test()

    s.set_load_by_reference_file_paths(
        [
            ('/prod/cg7/publish/assets/cam/camera_rig/rig/rigging/camera_rig.rig.rigging/maya/camera_rig.ma', 'd10010_cam'),
            ('/prod/cg7/publish/assets/env/temple_d10010a/mod/model/temple_d10010a.mod.model/maya/temple_d10010a.ma', 'temple_d10010a')
        ]
    )
    for obj in s.get_objs():
        d = obj.get_variant('asset/maya/source/rlt_plf_file_path')
        op = utl_prd_objects.ObjOpt(obj)
        # print obj
        # print op
        storage_op = utl_prd_objects.ObjStorageOp(obj)
        # print storage_op
        print storage_op.get_src_path('image')
        print storage_op.get_prd_path('image')
        print storage_op.get_tmp_path('image')

        print storage_op.get_src_path('main')
        print storage_op.get_prd_path('main')
        print storage_op.get_tmp_path('main')

        print storage_op.get_src_file_path('dcc')
        print storage_op.get_prd_file_path('dcc')
        print storage_op.get_tmp_file_path('dcc')

    # step_obj = s.get_current_step_obj()


