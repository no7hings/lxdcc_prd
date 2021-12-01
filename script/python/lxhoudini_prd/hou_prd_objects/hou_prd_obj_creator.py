# coding:utf-8
# noinspection PyUnresolvedReferences
import hou

from lxutil import utl_core, methods

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxutil_prd import utl_prd_abstract, utl_prd_commands

from lxutil_prd.utl_prd_objects import _utl_prd_obj_utility

import lxhoudini.dcc.dcc_objects as hou_dcc_objects


class ElementCreator(utl_prd_abstract.AbsElementCreator):
    CONTAINER_OPT_CLASS = _utl_prd_obj_utility.ContainerOpt
    DCC_OBJ_CLASS = hou_dcc_objects.Node
    DCC_DEFAULT_MATERIAL_PATH = '/shop/default_arnold_material'
    def __init__(self, element_opt, **build_kwargs):
        super(ElementCreator, self).__init__(element_opt)

    def set_create(self):
        element_opt = self._element_opt
        container_opt = self.container_opt
        #
        hou_obj_paths = []
        hou_out_paths = []
        #
        entities_dcc_type = container_opt.entities_dcc_type
        entities_dcc_path = container_opt.entities_dcc_path
        dcc_entities = hou_dcc_objects.Node(entities_dcc_path)
        hou_entities, _ = dcc_entities.get_dcc_instance(entities_dcc_type, entities_dcc_path)
        hou_obj_paths.append(entities_dcc_path)
        #
        hou_input = hou_entities
        # shot-camera
        if container_opt.get_scheme_is_sot_cmr():
            if container_opt.get_data_scheme_is_cmr_abc():
                self._set_cmr_abc_create_(container_opt, element_opt, hou_input, hou_obj_paths)
        # shot-geometry
        elif container_opt.get_scheme_is_sot_anm():
            # material-materialx
            if container_opt.get_data_scheme_is_mtl_mtx():
                self._set_mtl_mtx_create_(container_opt, element_opt, hou_input, hou_out_paths)
            # geometry-alembic
            elif container_opt.get_data_scheme_is_gmt_abc():
                self._set_gmt_abc_create_(container_opt, element_opt, hou_input, hou_obj_paths)
            elif container_opt.get_data_scheme_is_har_xgn():
                self._set_har_xgn_create_(container_opt, element_opt, hou_input, hou_obj_paths)
            elif container_opt.get_data_scheme_is_xgn_glo_abc():
                self._set_har_xgn_create_(container_opt, element_opt, hou_input, hou_obj_paths)
        # shot-assembly
        elif container_opt.get_scheme_is_sot_asb():
            use_ist = container_opt.use_ist
            if use_ist is True:
                if container_opt.get_data_scheme_is_mtl_mtx():
                    self._set_mtl_mtx_ist_create_(container_opt, element_opt, hou_input, hou_out_paths)
                elif container_opt.get_data_scheme_is_gmt_abc():
                    self._set_gmt_abc_ist_create_(container_opt, element_opt, hou_input, hou_obj_paths)
            else:
                if container_opt.get_data_scheme_is_mtl_mtx():
                    self._set_mtl_mtx_create_(container_opt, element_opt, hou_input, hou_out_paths)
                elif container_opt.get_data_scheme_is_gmt_abc():
                    self._set_gmt_abc_create_(container_opt, element_opt, hou_input, hou_obj_paths)
            if container_opt.get_data_scheme_is_plt_dta():
                self._set_plt_dta_create_(container_opt, element_opt, hou_input, hou_obj_paths)
        # crowd-asset
        elif container_opt.get_scheme_is_sot_crd():
            if container_opt.get_data_scheme_is_crd_abc():
                self._set_crd_abc_create_(container_opt, element_opt, hou_input, hou_out_paths)
            # material-materialx
            elif container_opt.get_data_scheme_is_mtl_mtx():
                self._set_mtl_mtx_create_(container_opt, element_opt, hou_input, hou_out_paths)
        # shot-effect
        elif container_opt.get_scheme_is_sot_efx():
            if container_opt.get_data_scheme_is_hou_dta():
                self._set_hou_dta_create_(container_opt, element_opt, hou_input, hou_out_paths)
        return hou_obj_paths
    @utl_core._debug_
    def _get_shotgun_resolution_(self):
        from lxshotgun import commands
        s = utl_prd_commands.get_current_scene()
        project = s.get_current_project_obj()
        if project is not None:
            return commands.get_project_resolution(project.name)

    def _set_cmr_abc_create_(self, container_opt, element_opt, hou_input, hou_obj_paths):
        container_dcc_type = container_opt.dcc_type
        container_dcc_path = container_opt.dcc_path
        #
        element_name = element_opt.name
        element_dcc_type = element_opt.dcc_type
        element_dcc_path = element_opt.dcc_path
        element_dcc_port = element_opt.dcc_port
        vsn_raw = element_opt.vsn_raw
        #
        dcc_alembic_archive = hou_dcc_objects.AlembicArchive(element_dcc_path)
        element_hou_obj, _ = dcc_alembic_archive.get_dcc_instance(element_dcc_type, element_dcc_path)
        hou_obj_paths.append(element_dcc_path)
        #
        element_hou_obj.setGenericFlag(hou.nodeFlag.Display, False)
        element_hou_obj.setGenericFlag(hou.nodeFlag.Render, False)
        #
        element_hou_obj.parm(element_dcc_port).set(vsn_raw)
        element_hou_obj.parm('buildHierarchy').pressButton()
        #
        resolution = self._get_shotgun_resolution_()
        if resolution is not None:
            dcc_cameras = dcc_alembic_archive.get_cameras()
            for dcc_camera in dcc_cameras:
                dcc_camera.set_resolution(*resolution)
                dcc_camera.get_port('far').set(500000000, expression=True)

    def _set_mtl_mtx_create_(self, container_opt, element_opt, hou_input, hou_obj_paths):
        role_tag_dcc_type = container_opt.role_tag_dcc_type
        role_tag_dcc_path = container_opt.role_tag_dcc_path
        role_tag_dcc_obj = hou_dcc_objects.Node(role_tag_dcc_path)
        role_tag_hou_obj, _ = role_tag_dcc_obj.get_dcc_instance(role_tag_dcc_type, role_tag_dcc_path)
        hou_obj_paths.append(role_tag_dcc_path)
        if hou_input is not None:
            role_tag_hou_obj.setInput(0, hou_input)
        #
        container_dcc_type = container_opt.dcc_type
        container_dcc_path = container_opt.dcc_path
        #
        element_name = element_opt.name
        element_dcc_type = element_opt.dcc_type
        element_dcc_path = element_opt.dcc_path
        element_dcc_port = element_opt.dcc_port
        vsn_raw = element_opt.vsn_raw
        #
        ett_brh = element_opt.entity_branch
        container_variant = element_opt.container_variant
        #
        container_dcc_obj = hou_dcc_objects.Node(container_dcc_path)
        #
        container_hou_obj, _ = container_dcc_obj.get_dcc_instance(element_dcc_type, element_dcc_path)
        container_hou_obj.parm(element_dcc_port).set(vsn_raw)
        #
        container_hou_obj.parm('selection').set('/*')
        container_hou_obj.parm('look').set('default')
        #
        container_hou_obj.setInput(0, role_tag_hou_obj.indirectInputs()[0])

    def _set_mtl_mtx_ist_create_(self, container_opt, element_opt, hou_input, hou_obj_paths):
        self._set_mtl_mtx_create_(container_opt, element_opt, hou_input, hou_obj_paths)

    def _set_gmt_abc_create_(self, container_opt, element_opt, hou_input, hou_obj_paths):
        role_tag_dcc_type = container_opt.role_tag_dcc_type
        role_tag_dcc_path = container_opt.role_tag_dcc_path
        role_tag_dcc_obj = hou_dcc_objects.Node(role_tag_dcc_path)
        role_tag_hou_obj, _ = role_tag_dcc_obj.get_dcc_instance(role_tag_dcc_type, role_tag_dcc_path)
        hou_obj_paths.append(role_tag_dcc_path)
        if hou_input is not None:
            role_tag_hou_obj.setInput(0, hou_input)
        #
        container_namespace_dcc_type = container_opt.namespace_dcc_type
        namespace_dcc_path = container_opt.namespace_dcc_path
        container_namespace_dcc_obj = hou_dcc_objects.Node(namespace_dcc_path)
        container_namespace_hou_obj, _ = container_namespace_dcc_obj.get_dcc_instance(container_namespace_dcc_type, namespace_dcc_path)
        container_namespace_hou_obj.setInput(0, role_tag_hou_obj.indirectInputs()[0])
        #
        container_scheme = container_opt.scheme
        container_dcc_type = container_opt.dcc_type
        container_dcc_path = container_opt.dcc_path
        #
        element_name = element_opt.name
        element_dcc_type = element_opt.dcc_type
        element_dcc_path = element_opt.dcc_path
        element_dcc_port = element_opt.dcc_port
        vsn_raw = element_opt.vsn_raw
        #
        ett_brh = element_opt.entity_branch
        container_variant = element_opt.container_variant
        #
        container_dcc_obj = hou_dcc_objects.Geometry(container_dcc_path)
        #
        container_hou_obj, _ = container_dcc_obj.get_dcc_instance(container_dcc_type, container_dcc_path)
        if container_variant != 'hi':
            container_hou_obj.setGenericFlag(hou.nodeFlag.Display, False)
            container_hou_obj.setGenericFlag(hou.nodeFlag.Render, False)
        #
        container_hou_obj.setInput(0, container_namespace_hou_obj)
        #
        if container_opt.get_scheme_is_sot_asb():
            value = container_opt.value
            if len(value) == 16:
                container_dcc_obj.set_matrix(value)
            else:
                container_dcc_obj.set_transformations(value)
        else:
            pass
        #
        self._set_geo_container_color_(container_opt, container_dcc_obj)
        #
        mtl_mtx_dcc_path = container_opt.get_mtl_mtx_dcc_path()
        mtl_mtx_hou_obj = hou.node(mtl_mtx_dcc_path)
        if mtl_mtx_hou_obj is not None:
            container_hou_obj.parm('ar_operator_graph').set(mtl_mtx_dcc_path)
            container_hou_obj.parm('shop_materialpath').set('')
        else:
            container_hou_obj.parm('shop_materialpath').set(self.DCC_DEFAULT_MATERIAL_PATH)
        #
        port_element_dcc_obj = hou_dcc_objects.Node(element_dcc_path)
        element_hou_obj, element_hou_obj_is_create = port_element_dcc_obj.get_dcc_instance(element_dcc_type, element_dcc_path)
        if ett_brh == 'shot':
            element_hou_obj.setGenericFlag(hou.nodeFlag.Display, True)
            element_hou_obj.setGenericFlag(hou.nodeFlag.Render, True)
        #
        element_hou_obj.parm(element_dcc_port).set(vsn_raw)
        # element_hou_obj.appendComment('{};\n'.format(element_name))
        #
        if container_opt.get_scheme_is_sot_asb():
            if element_hou_obj_is_create is True:
                element_hou_obj.parm('viewportlod').set(2)

    def _set_gmt_abc_ist_create_(self, container_opt, element_opt, hou_input, hou_obj_paths):
        role_tag_dcc_type = container_opt.role_tag_dcc_type
        role_tag_dcc_path = container_opt.role_tag_dcc_path
        role_tag_dcc_obj = hou_dcc_objects.Node(role_tag_dcc_path)
        role_tag_hou_obj, _ = role_tag_dcc_obj.get_dcc_instance(role_tag_dcc_type, role_tag_dcc_path)
        hou_obj_paths.append(role_tag_dcc_path)
        if hou_input is not None:
            role_tag_hou_obj.setInput(0, hou_input)
        #
        container_namespace = container_opt.namespace
        container_namespace_dcc_type = container_opt.namespace_dcc_type
        container_namespace_dcc_path = container_opt.namespace_dcc_path
        #
        container_scheme = container_opt.scheme
        #
        container_ist_opt = container_opt.get_ist_opt()
        container_ist_dcc_type = container_ist_opt.dcc_type
        container_ist_dcc_path = container_ist_opt.dcc_path
        #
        container_ist_dcc_obj = hou_dcc_objects.Geometry(container_ist_dcc_path)
        container_ist_hou_obj, _ = container_ist_dcc_obj.get_dcc_instance(container_ist_dcc_type, container_ist_dcc_path)
        container_ist_hou_obj.setGenericFlag(hou.nodeFlag.Display, False)
        container_ist_hou_obj.setGenericFlag(hou.nodeFlag.Render, False)
        #
        mtl_mtx_dcc_path = container_opt.get_mtl_mtx_dcc_path()
        mtl_mtx_hou_obj = hou.node(mtl_mtx_dcc_path)
        if mtl_mtx_hou_obj is not None:
            container_ist_hou_obj.parm('ar_operator_graph').set(mtl_mtx_dcc_path)
            container_ist_hou_obj.parm('shop_materialpath').set('')
        else:
            container_ist_hou_obj.parm('shop_materialpath').set(self.DCC_DEFAULT_MATERIAL_PATH)
        #
        element_ist_dcc_type = element_opt.ist_dcc_type
        element_ist_dcc_path = element_opt.ist_dcc_path
        element_ist_plf_file_dcc_port_name = element_opt.ist_dcc_port
        vsn_raw = element_opt.vsn_raw
        #
        ett_brh = element_opt.entity_branch
        container_variant = element_opt.container_variant
        #
        element_ist_dcc_obj = hou_dcc_objects.Node(element_ist_dcc_path)
        element_ist_hou_obj, element_ist_hou_obj_is_create = element_ist_dcc_obj.get_dcc_instance(element_ist_dcc_type, element_ist_dcc_path)
        element_ist_hou_obj.parm(element_ist_plf_file_dcc_port_name).set(vsn_raw)
        #
        if container_opt.get_scheme_is_sot_asb():
            if container_variant == 'hi':
                f = utl_dcc_objects.OsFile(vsn_raw)
                display_keys = [
                    'lo',
                    'proxy'
                ]
                for display_key in display_keys:
                    display_plf_file_path = '{}/{}.abc'.format(f.directory.path, display_key)
                    display_plf_file = utl_dcc_objects.OsFile(display_plf_file_path)
                    if display_plf_file.get_is_exists() is True:
                        display_dcc_path = '{}_{}'.format(element_ist_dcc_path, display_key)
                        display_dcc_obj = hou_dcc_objects.Node(display_dcc_path)
                        display_hou_obj, _ = display_dcc_obj.get_dcc_instance(element_ist_dcc_type, display_dcc_path)
                        display_hou_obj.parm(element_ist_plf_file_dcc_port_name).set(display_plf_file_path)
                        #
                        element_ist_hou_obj.setGenericFlag(hou.nodeFlag.Display, False)
                        element_ist_hou_obj.setGenericFlag(hou.nodeFlag.Render, True)
                        #
                        if display_key == 'lo':
                            display_hou_obj.setGenericFlag(hou.nodeFlag.Display, True)
                            display_hou_obj.setGenericFlag(hou.nodeFlag.Render, False)
                        else:
                            display_hou_obj.setGenericFlag(hou.nodeFlag.Display, False)
                            display_hou_obj.setGenericFlag(hou.nodeFlag.Render, False)
            #
            if element_ist_hou_obj_is_create is True:
                element_ist_hou_obj.parm('viewportlod').set(2)
        #
        ist_raw = container_opt.ist_raw
        if ist_raw:
            for i in ist_raw:
                cmp_namespace, value = i
                #
                namespace_dcc_path = container_namespace_dcc_path.replace(container_namespace, cmp_namespace)
                container_ist_cmp_namespace_dcc_obj = hou_dcc_objects.Node(namespace_dcc_path)
                container_ist_cmp_namespace_hou_obj, _ = container_ist_cmp_namespace_dcc_obj.get_dcc_instance(
                    container_namespace_dcc_type, namespace_dcc_path
                )
                container_ist_cmp_namespace_hou_obj.setInput(0, role_tag_hou_obj.indirectInputs()[0])
                #
                container_ist_cmp_dcc_type = container_opt.ist_cmp_dcc_type
                container_ist_cmp_dcc_path = container_opt.ist_cmp_dcc_path.replace(container_namespace, cmp_namespace)
                container_ist_cmp_dcc_port_name = container_opt.ist_cmp_dcc_port_name
                #
                container_ist_cmp_dcc_obj = hou_dcc_objects.Geometry(container_ist_cmp_dcc_path)
                container_ist_cmp_hou_obj, _ = container_ist_cmp_dcc_obj.get_dcc_instance(container_ist_cmp_dcc_type, container_ist_cmp_dcc_path)
                container_ist_cmp_hou_obj.setInput(0, container_ist_cmp_namespace_hou_obj)
                container_ist_cmp_dcc_obj.get_port(container_ist_cmp_dcc_port_name).set(container_ist_dcc_path)
                container_ist_cmp_dcc_obj.get_port('ptinstance').set(2)
                if container_opt.get_scheme_is_sot_asb():
                    if value:
                        if len(value) == 16:
                            container_ist_cmp_dcc_obj.set_matrix(value)
                        else:
                            container_ist_cmp_dcc_obj.set_transformations(value)
                #
                self._set_instance_container_color_(container_opt, container_ist_cmp_dcc_obj)

    def _set_plt_dta_create_(self, container_opt, element_opt, hou_input, hou_obj_paths):
        role_tag_dcc_type = container_opt.role_tag_dcc_type
        role_tag_dcc_path = container_opt.role_tag_dcc_path
        role_tag_dcc_obj = hou_dcc_objects.Node(role_tag_dcc_path)
        role_tag_hou_obj, _ = role_tag_dcc_obj.get_dcc_instance(role_tag_dcc_type, role_tag_dcc_path)
        hou_obj_paths.append(role_tag_dcc_path)
        if hou_input is not None:
            role_tag_hou_obj.setInput(0, hou_input)
        #
        container_namespace_dcc_type = container_opt.namespace_dcc_type
        namespace_dcc_path = container_opt.namespace_dcc_path
        container_namespace_dcc_obj = hou_dcc_objects.Node(namespace_dcc_path)
        container_namespace_hou_obj, _ = container_namespace_dcc_obj.get_dcc_instance(
            container_namespace_dcc_type, namespace_dcc_path
        )
        container_namespace_hou_obj.setInput(0, role_tag_hou_obj.indirectInputs()[0])
        #
        container_scheme = container_opt.scheme
        container_dcc_type = container_opt.dcc_type
        container_dcc_path = container_opt.dcc_path
        container_dcc_obj = hou_dcc_objects.Geometry(container_dcc_path)
        container_hou_obj, _ = container_dcc_obj.get_dcc_instance(container_dcc_type, container_dcc_path)
        container_hou_obj.setInput(0, container_namespace_hou_obj)
        #
        element_name = element_opt.name
        element_dcc_type = element_opt.dcc_type
        element_dcc_path = element_opt.dcc_path
        element_dcc_port = element_opt.dcc_port
        vsn_raw = element_opt.vsn_raw
        #
        ett_brh = element_opt.entity_branch
        container_variant = element_opt.container_variant
        #
        port_element_dcc_obj = hou_dcc_objects.Node(element_dcc_path)
        element_hou_obj, element_hou_obj_is_create = port_element_dcc_obj.get_dcc_instance(element_dcc_type, element_dcc_path)
        if element_hou_obj_is_create:
            element_hou_obj.addControlParmFolder('Pg-build', 'pg_buid')
            p = hou.StringParmTemplate('file_path', 'File-path', 1)
            element_hou_obj.addSpareParmTuple(p, ('Pg-build',))
        element_hou_obj.parm(element_dcc_port).set(vsn_raw)
        #
        vsn_cmp_raws = element_opt.vsn_cmp_raw
        if vsn_cmp_raws:
            for i in vsn_cmp_raws:
                f = utl_dcc_objects.OsFile(i)
                cmp_path = '{}/{}'.format(element_dcc_path, f.base)
                cmp_dcc_obj = hou_dcc_objects.Geometry(cmp_path)
                cmp_hou_obj, _ = cmp_dcc_obj.get_dcc_instance('pntInstance', cmp_path)
                cmp_hou_obj.parm('pntFile').set(i)
                #
                if container_opt.get_scheme_is_sot_asb():
                    value = container_opt.value
                    if value:
                        if len(value) == 16:
                            cmp_dcc_obj.set_matrix(value)
                        else:
                            cmp_dcc_obj.set_transformations(value)

    def _set_har_xgn_create_(self, container_opt, element_opt, hou_input, hou_obj_paths):
        role_tag_dcc_type = container_opt.role_tag_dcc_type
        role_tag_dcc_path = container_opt.role_tag_dcc_path
        role_tag_dcc_obj = hou_dcc_objects.Node(role_tag_dcc_path)
        role_tag_hou_obj, _ = role_tag_dcc_obj.get_dcc_instance(role_tag_dcc_type, role_tag_dcc_path)
        hou_obj_paths.append(role_tag_dcc_path)
        if hou_input is not None:
            role_tag_hou_obj.setInput(0, hou_input)
        #
        container_namespace_dcc_type = container_opt.namespace_dcc_type
        namespace_dcc_path = container_opt.namespace_dcc_path
        container_namespace_dcc_obj = hou_dcc_objects.Node(namespace_dcc_path)
        container_namespace_hou_obj, _ = container_namespace_dcc_obj.get_dcc_instance(container_namespace_dcc_type, namespace_dcc_path)
        #
        element_dcc_type = element_opt.dcc_type
        element_dcc_path = element_opt.dcc_path
        element_dcc_port = element_opt.dcc_port
        vsn_raw = element_opt.vsn_raw
        #
        port_element_dcc_obj = hou_dcc_objects.Node(element_dcc_path)
        element_hou_obj, element_hou_obj_is_create = port_element_dcc_obj.get_dcc_instance(element_dcc_type)
        element_hou_obj.setInput(0, container_namespace_hou_obj)
        #
        if element_hou_obj_is_create is True:
            element_hou_obj.addControlParmFolder('Pg-build', 'pg_buid')
        #
        p = element_hou_obj.parm(element_dcc_port)
        if p is None:
            pt = hou.StringParmTemplate(element_dcc_port, element_dcc_port, 1)
            element_hou_obj.addSpareParmTuple(pt, ('Pg-build',))
        #
        element_hou_obj.parm(element_dcc_port).set(vsn_raw)
        #
        element_cmp_dcc_type = element_opt.cmp_dcc_type
        element_cmp_dcc_path = element_opt.cmp_dcc_path
        element_cmp_dcc_port = element_opt.cmp_dcc_port
        #
        vsn_cmp_raws = element_opt.vsn_cmp_raw
        if vsn_cmp_raws:
            hou_camera_path = None
            cmr_abc_container_dcc_path = container_opt.get_cmr_abc_dcc_path()
            if cmr_abc_container_dcc_path is not None:
                hou_cmr_abc_container = hou_dcc_objects.AlembicArchive(cmr_abc_container_dcc_path)
                if hou_cmr_abc_container.get_is_exists() is True:
                    hou_camera_paths = hou_cmr_abc_container.get_camera_paths()
                    if hou_camera_paths:
                        hou_camera_path = hou_camera_paths[0]
            #
            for i in vsn_cmp_raws:
                if hou_camera_path is not None:
                    f = utl_dcc_objects.OsFile(i)
                    file_name = f.base
                    element_cmp_dcc_path = element_cmp_dcc_path.replace('cmp_var', file_name)
                    #
                    element_cmp_dcc_obj = hou_dcc_objects.Node(element_cmp_dcc_path)
                    element_cmp_hou_obj, _ = element_cmp_dcc_obj.get_dcc_instance(element_cmp_dcc_type)
                    element_cmp_hou_obj.setInput(0, element_hou_obj)
                    element_cmp_hou_obj.parm('camera').set(hou_camera_path)
                    element_cmp_hou_obj.parm(element_cmp_dcc_port).set(i)
                    #
                    if element_cmp_hou_obj.parm('xGenFile').eval() and element_cmp_hou_obj.parm('skinAbcFile').eval() and element_cmp_hou_obj.parm('camera').eval():
                        element_cmp_hou_obj.parm('build').pressButton()
                    #
                    hou_container_instance_path = '{}_Instance'.format(element_cmp_dcc_path)
                    dcc_container_instance = hou_dcc_objects.Node(hou_container_instance_path)
                    if dcc_container_instance.get_is_exists() is True:
                        mtl_mtx_dcc_path = container_opt.get_mtl_mtx_dcc_path()
                        mtl_mtx_hou_obj = hou.node(mtl_mtx_dcc_path)
                        dcc_children = dcc_container_instance.get_children()
                        for dcc_child in dcc_children:
                            if dcc_child.type == 'Object/arnold_procedural':
                                hou_arnold_procedural = dcc_child.hou_obj
                                if mtl_mtx_hou_obj is not None:
                                    hou_arnold_procedural.parm('ar_operator_graph_enable').set(True)
                                    hou_arnold_procedural.parm('ar_operator_graph').set(mtl_mtx_dcc_path)
                                    hou_arnold_procedural.parm('shop_materialpath').set('')
                                else:
                                    hou_arnold_procedural.parm('shop_materialpath').set(self.DCC_DEFAULT_MATERIAL_PATH)

    def _set_crd_abc_create_(self, container_opt, element_opt, hou_input, hou_obj_paths):
        manifest = container_opt.manifest
        role_tag_dcc_type = container_opt.role_tag_dcc_type
        role_tag_dcc_path = container_opt.role_tag_dcc_path
        role_tag_dcc_obj = hou_dcc_objects.Node(role_tag_dcc_path)
        role_tag_hou_obj, role_tag_hou_obj_is_create = role_tag_dcc_obj.get_dcc_instance(role_tag_dcc_type, role_tag_dcc_path)
        hou_obj_paths.append(role_tag_dcc_path)
        if hou_input is not None:
            role_tag_hou_obj.setInput(0, hou_input)

        container_mrg_dcc_type = container_opt.mrg_dcc_type
        container_mrg_dcc_path = container_opt.mrg_dcc_path
        #
        container_mrg_dcc_obj = hou_dcc_objects.Node(container_mrg_dcc_path)
        container_mrg_hou_obj, container_mrg_hou_obj_is_create = container_mrg_dcc_obj.get_dcc_instance(container_mrg_dcc_type, container_mrg_dcc_path)
        container_mrg_hou_obj.parm('shop_materialpath').set(self.DCC_DEFAULT_MATERIAL_PATH)
        container_mrg_hou_obj.setInput(0, role_tag_hou_obj.indirectInputs()[0])
        #
        if container_mrg_hou_obj_is_create is True:
            container_mrg_hou_obj.addControlParmFolder('Pg-build', 'pg_buid')
            p = hou.StringParmTemplate('vsn_key', 'Version-key', 1)
            container_mrg_hou_obj.addSpareParmTuple(p, ('Pg-build',))
            vsn_key = manifest.get_variant('self.manifest.vsn_key')
            container_mrg_hou_obj.parm('vsn_key').set(vsn_key)
            #
            p = hou.StringParmTemplate('vsn_raw', 'Version-raw', 1)
            container_mrg_hou_obj.addSpareParmTuple(p, ('Pg-build',))
            vsn_raw = manifest.get_variant('self.manifest.vsn_raw')
            container_mrg_hou_obj.parm('vsn_raw').set(vsn_raw)
        #
        mtl_mtx_dcc_path = container_opt.get_mtl_mtx_dcc_path()
        mtl_mtx_hou_obj = hou.node(mtl_mtx_dcc_path)
        if mtl_mtx_hou_obj is not None:
            container_mrg_hou_obj.parm('ar_operator_graph').set(mtl_mtx_dcc_path)
            container_mrg_hou_obj.parm('shop_materialpath').set('')
        else:
            container_mrg_hou_obj.parm('shop_materialpath').set(self.DCC_DEFAULT_MATERIAL_PATH)
        #
        self._set_geo_container_color_(container_opt, container_mrg_dcc_obj)
        #
        element_mrg_dcc_type = element_opt.mrg_dcc_type
        element_mrg_dcc_path = element_opt.mrg_dcc_path
        #
        ett_brh = element_opt.entity_branch
        container_variant = element_opt.container_variant
        vsn_cmp_raws = element_opt.vsn_cmp_raw
        if vsn_cmp_raws:
            element_mrg_dcc_obj = hou_dcc_objects.Node(element_mrg_dcc_path)
            element_mrg_hou_obj, element_mrg_hou_obj_is_create = element_mrg_dcc_obj.get_dcc_instance(element_mrg_dcc_type, element_mrg_dcc_path)
            if element_mrg_hou_obj_is_create:
                element_mrg_hou_obj.addControlParmFolder('Pg-build', 'pg_buid')
                p = hou.StringParmTemplate('file_path', 'File-path', 1)
                element_mrg_hou_obj.addSpareParmTuple(p, ('Pg-build',))
            #
            element_mrg_cmp_dcc_type = element_opt.mrg_cmp_dcc_type
            element_mrg_cmp_dcc_path = element_opt.mrg_cmp_dcc_path
            for seq, i in enumerate(vsn_cmp_raws):
                f = utl_dcc_objects.OsFile(i)
                cmp_path = '{}_{}'.format(element_mrg_dcc_path, seq)
                cmp_dcc_obj = hou_dcc_objects.Alembic(cmp_path)
                cmp_hou_obj, cmp_hou_obj_is_create = cmp_dcc_obj.get_dcc_instance(element_mrg_cmp_dcc_type, cmp_path)
                cmp_dcc_obj.get_port('fileName').set(f.path)
                if cmp_hou_obj_is_create is True:
                    cmp_dcc_obj.get_port('viewportlod').set(3)
                #
                element_mrg_hou_obj.setInput(seq, cmp_hou_obj)

    def _set_hou_dta_create_(self, container_opt, element_opt, hou_input, hou_obj_paths):
        role_tag_dcc_type = container_opt.role_tag_dcc_type
        role_tag_dcc_path = container_opt.role_tag_dcc_path
        role_tag_dcc_obj = hou_dcc_objects.Node(role_tag_dcc_path)
        role_tag_hou_obj, _ = role_tag_dcc_obj.get_dcc_instance(role_tag_dcc_type, role_tag_dcc_path)
        hou_obj_paths.append(role_tag_dcc_path)
        if hou_input is not None:
            role_tag_hou_obj.setInput(0, hou_input)

        container_dcc_type = container_opt.dcc_type
        container_dcc_path = container_opt.dcc_path
        #
        element_name = element_opt.name
        element_dcc_type = element_opt.dcc_type
        element_dcc_path = element_opt.dcc_path
        element_dcc_port = element_opt.dcc_port
        vsn_raw = element_opt.vsn_raw
        #
        ett_brh = element_opt.entity_branch
        container_variant = element_opt.container_variant
        #
        container_dcc_obj = hou_dcc_objects.Node(container_dcc_path)
        #
        container_hou_obj, _ = container_dcc_obj.get_dcc_instance(container_dcc_type, container_dcc_path)
        #
        port_element_dcc_obj = hou_dcc_objects.Node(element_dcc_path)
        element_hou_obj, _ = port_element_dcc_obj.get_dcc_instance(element_dcc_type, element_dcc_path)
        element_hou_obj.parm(element_dcc_port).set(vsn_raw)

    def get_crt_plf_file_path(self):
        hou_node = hou.node(self.element_opt.dcc_path)
        if hou_node is not None:
            p = hou_node.parm(self.element_opt.dcc_port)
            if p:
                return p.unexpandedString()

    def get_is_plf_file_path_changed(self):
        pass

    def _set_instance_container_color_(self, container_opt, container_dcc_obj):
        r, g, b = methods.String.to_rgb(container_opt.get_variant('self.asset.plf_name'), maximum=1.0)
        container_dcc_obj.get_port('i_use_dcolor').set(True)
        container_dcc_obj.get_port('i_dcolorr').set(r)
        container_dcc_obj.get_port('i_dcolorg').set(g)
        container_dcc_obj.get_port('i_dcolorb').set(b)

    def _set_geo_container_color_(self, container_opt, container_dcc_obj):
        r, g, b = methods.String.to_rgb(container_opt.get_variant('self.asset.plf_name'), maximum=1.0)
        container_dcc_obj.get_port('use_dcolor').set(True)
        container_dcc_obj.get_port('dcolorr').set(r)
        container_dcc_obj.get_port('dcolorg').set(g)
        container_dcc_obj.get_port('dcolorb').set(b)
