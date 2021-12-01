# coding:utf-8
from lxutil_prd import utl_prd_configure, utl_prd_core, utl_prd_objects, utl_prd_commands

for i in [
    '/l/prod/cg7/work/shots/d10/d10240/lgt/lgt/houdini/d10240.lgt.lgt.v003.hip'
]:
    s = utl_prd_commands.set_scene_load_from_scene(
        i
    )
    entity = s.get_current_entity_obj()
    shot_opt = utl_prd_objects.ShotOpt(entity)
    shot_opt.set_manifests_build()
    manifests = shot_opt.get_manifests('anm_scm')
    for manifest in manifests:
        manifest_opt = utl_prd_objects.ManifestOpt(manifest)
        manifest_opt.set_containers_build()
        container_type = s.universe.get_obj_type(utl_prd_configure.ObjType.CONTAINER)
        container_objs = container_type.get_objs()
        for container_obj in container_objs:
            container_opt = utl_prd_objects.ContainerOpt(container_obj)
            if container_opt.data_scheme in ['har_xgn', 'xgn_glo_abc']:
                element_opts = container_opt.get_element_opts()
                if element_opts:
                    for element_opt in element_opts:
                        print container_opt.use_ign
                        print element_opt.vsn_cmp_raw
                        print element_opt.dcc_port, element_opt.use_brh
                        print element_opt.cmp_dcc_type, element_opt.cmp_dcc_name, element_opt.cmp_dcc_path, element_opt.cmp_dcc_port
