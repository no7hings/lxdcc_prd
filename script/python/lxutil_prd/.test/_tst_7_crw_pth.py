# coding:utf-8
from lxutil_prd import utl_prd_configure, utl_prd_objects, utl_prd_commands, utl_prd_core

for i in [
    '/l/prod/cg7/work/shots/d10/d10010/lgt/lgt/houdini/d10010.lgt.lgt.v003.hip'
]:
    s = utl_prd_commands.set_scene_load_from_scene(
        i
    )
    entity = s.get_current_entity_obj()
    shot_opt = utl_prd_objects.ShotOpt(entity)
    shot_opt.set_manifests_build()
    manifests = shot_opt.get_manifests('crd_scm')
    for manifest in manifests:
        manifest_opt = utl_prd_objects.ManifestOpt(manifest)
        manifest_opt.set_containers_build()
        container_type = s.universe.get_obj_type(utl_prd_configure.ObjType.CONTAINER)
        container_objs = container_type.get_objs()
        for container_obj in container_objs:
            container_opt = utl_prd_objects.ContainerOpt(container_obj)
            data_scheme = container_opt.data_scheme
            if data_scheme == 'crd_abc':
                element_opts = container_opt.get_element_opts('shot')
                for element_opt in element_opts:
                    print element_opt.vsn_cmp_raw

