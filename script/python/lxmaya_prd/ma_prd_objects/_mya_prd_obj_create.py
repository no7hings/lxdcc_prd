# coding:utf-8
from lxutil import utl_core

from lxutil_prd import utl_prd_configure, utl_prd_abstract, utl_prd_commands

from lxutil_prd.utl_prd_objects import _utl_prd_obj_utility

import lxmaya.dcc.dcc_objects as ma_dcc_objects


class ElementCreator(utl_prd_abstract.AbsElementCreator):
    CONTAINER_OPT_CLASS = _utl_prd_obj_utility.ContainerOpt
    DCC_OBJ_CLASS = ma_dcc_objects.Node
    def __init__(self, element_opt, **kwargs):
        self._kwargs = kwargs
        super(ElementCreator, self).__init__(element_opt)

    def set_create(self):
        element_opt = self._element_opt
        container_opt = self.container_opt
        # shot-camera
        if container_opt.get_scheme_is_sot_cmr():
            if container_opt.get_data_scheme_is_cmr_abc():
                self._set_cmr_abc_create_(container_opt, element_opt)
        # shot-geometry
        elif container_opt.get_scheme_is_sot_anm():
            # geometry-alembic
            if container_opt.get_data_scheme_is_gmt_abc():
                self._set_gmt_abc_create_(container_opt, element_opt)
            # material-materialx
            elif container_opt.get_data_scheme_is_mtl_mtx():
                self._set_mtl_mtx_create_(container_opt, element_opt)
        elif container_opt.get_scheme_is_sot_har():
            if container_opt.get_data_scheme_is_har_xgn():
                self._set_har_xgn_create_(container_opt, element_opt)
            elif container_opt.get_data_scheme_is_xgn_glo_abc():
                self._set_har_xgn_create_(container_opt, element_opt)
        # shot-assembly
        elif container_opt.get_scheme_is_sot_asb():
            use_ist = container_opt.use_ist
            if use_ist is True:
                if container_opt.get_data_scheme_is_mtl_mtx():
                    self._set_mtl_mtx_ist_create_(container_opt, element_opt)
                elif container_opt.get_data_scheme_is_gmt_abc():
                    self._set_gmt_abc_ist_create_(container_opt, element_opt)
            else:
                if container_opt.get_data_scheme_is_mtl_mtx():
                    self._set_mtl_mtx_create_(container_opt, element_opt)
                elif container_opt.get_data_scheme_is_gmt_abc():
                    self._set_gmt_abc_create_(container_opt, element_opt)
        # crowd-asset
        elif container_opt.get_scheme_is_sot_crd():
            if container_opt.get_data_scheme_is_crd_abc():
                self._set_crd_abc_create_(container_opt, element_opt)
            # material-materialx
            elif container_opt.get_data_scheme_is_mtl_mtx():
                self._set_mtl_mtx_create_(container_opt, element_opt)
        elif container_opt.get_scheme_is_sot_efx():
            if container_opt.get_data_scheme_is_hou_dta():
                self._set_hou_dta_create_(container_opt, element_opt)
    @utl_core._debug_
    def _get_shotgun_resolution_(self):
        from lxshotgun import commands
        s = utl_prd_commands.get_current_scene()
        project = s.get_current_project_obj()
        if project is not None:
            return commands.get_project_resolution(project.name)

    def _set_cmr_abc_create_(self, container_opt, element_opt):
        container_dcc_type = container_opt.dcc_type
        container_dcc_path = container_opt.dcc_path
        container_dcc_obj = ma_dcc_objects.Node(container_dcc_path)
        container_dcc_obj.set_ancestors_create()
        container_dcc_obj.get_dcc_instance(container_dcc_type, container_dcc_path)
        #
        element_name = element_opt.name
        element_dcc_type = element_opt.dcc_type
        element_dcc_path = element_opt.dcc_path
        element_dcc_namespace = element_opt.dcc_namespace
        element_dcc_port = element_opt.dcc_port
        vsn_raw = element_opt.vsn_raw
        #
        port_element_dcc_obj = ma_dcc_objects.Reference(element_dcc_path)
        port_element_dcc_obj.set_load_from_file(vsn_raw, element_dcc_namespace)
        root_paths = port_element_dcc_obj.get_content_root_paths()
        for i in root_paths:
            dcc_root_obj = ma_dcc_objects.Node(i)
            dcc_root_obj.set_parent_path(container_dcc_path)
            dcc_root_obj.set_display_enable(False)

    def _set_gmt_abc_create_(self, container_opt, element_opt):
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
        port_element_dcc_obj = ma_dcc_objects.Node(element_dcc_path)
        port_element_dcc_obj.set_ancestors_create()
        #
        dcc_element_shape_dcc_path, _ = port_element_dcc_obj.get_dcc_instance(element_dcc_type, element_dcc_path, compose=True)
        dcc_element_shape_dcc_obj = ma_dcc_objects.Shape(dcc_element_shape_dcc_path)
        if dcc_element_shape_dcc_obj.get_is_exists() is True:
            port_element_dcc_obj = dcc_element_shape_dcc_obj.transform
            dcc_element_shape_dcc_obj.get_port(element_dcc_port).set(vsn_raw)
            #
            ignore_display = self._kwargs.get('ignore_display', False)
            if ignore_display is False:
                if container_opt.get_scheme_is_sot_anm():
                    if ett_brh in [utl_prd_configure.ObjType.ASSET]:
                        port_element_dcc_obj.set_display_enable(False)
                #
                if container_opt.get_scheme_is_sot_asb():
                    value = container_opt.value
                    if len(value) == 16:
                        port_element_dcc_obj.set_matrix(value)
                    else:
                        port_element_dcc_obj.set_transformations(value)
                #
                if container_variant not in ['hi']:
                    container_dcc_obj = ma_dcc_objects.Node(container_dcc_path)
                    container_dcc_obj.set_display_enable(False)
            #
            mtl_mtx_dcc_path = container_opt.get_mtl_mtx_dcc_path()
            dcc_mtl_mtx = ma_dcc_objects.AndMaterialx(mtl_mtx_dcc_path)
            if dcc_mtl_mtx.get_is_exists() is True:
                dcc_mtl_mtx.get_port('out').set_target(dcc_element_shape_dcc_obj.get_port('operators[0]'))
            else:
                pass

    def _set_gmt_abc_ist_create_(self, container_opt, element_opt):
        container_ist_opt = container_opt.get_ist_opt()
        container_ist_dcc_type = container_ist_opt.dcc_type
        container_ist_dcc_path = container_ist_opt.dcc_path
        #
        container_namespace = container_opt.namespace
        #
        element_ist_dcc_type = element_opt.ist_dcc_type
        element_ist_dcc_path = element_opt.ist_dcc_path
        element_ist_plf_file_dcc_port_name = element_opt.ist_dcc_port
        vsn_raw = element_opt.vsn_raw
        #
        element_ist_dcc_obj = ma_dcc_objects.Node(element_ist_dcc_path)
        element_ist_dcc_obj.set_ancestors_create()
        #
        dcc_element_ist_shape_dcc_path, _ = element_ist_dcc_obj.get_dcc_instance(element_ist_dcc_type, element_ist_dcc_path, compose=True)
        dcc_element_ist_shape_dcc_obj = ma_dcc_objects.Shape(dcc_element_ist_shape_dcc_path)
        if dcc_element_ist_shape_dcc_obj.get_is_exists() is True:
            dcc_element_ist_shape_dcc_obj.get_port(element_ist_plf_file_dcc_port_name).set(vsn_raw)
            #
            dcc_element_ist_shape_dcc_obj.transform.set_display_enable(False)
            #
            mtl_mtx_dcc_path = container_opt.get_mtl_mtx_dcc_path()
            dcc_mtl_mtx = ma_dcc_objects.AndMaterialx(mtl_mtx_dcc_path)
            if dcc_mtl_mtx.get_is_exists() is True:
                dcc_mtl_mtx.get_port('out').set_target(dcc_element_ist_shape_dcc_obj.get_port('operators[0]'))
            else:
                pass
        if element_ist_dcc_obj.get_is_exists() is True:
            ist_raw = container_opt.ist_raw
            if ist_raw:
                for i in ist_raw:
                    cmp_namespace, value = i
                    #
                    element_ist_cmp_dcc_path = element_opt.ist_cmp_dcc_path.replace(container_namespace, cmp_namespace)
                    element_ist_cmp_dcc_obj = ma_dcc_objects.Transform(element_ist_cmp_dcc_path)
                    element_ist_dcc_obj.set_instance_to(element_ist_cmp_dcc_path)
                    if element_ist_cmp_dcc_obj.get_is_exists() is True:
                        element_ist_cmp_dcc_obj.set_display_enable(True)
                        #
                        if container_opt.get_scheme_is_sot_asb():
                            if len(value) == 16:
                                element_ist_cmp_dcc_obj.set_matrix(value)
                            else:
                                element_ist_cmp_dcc_obj.set_transformations(value)

    def _set_har_xgn_create_(self, container_opt, element_opt):
        pass

    def _set_mtl_mtx_create_(self, container_opt, element_opt):
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
        port_element_dcc_obj = ma_dcc_objects.AndMaterialx(element_dcc_path)
        port_element_dcc_obj.get_dcc_instance(element_dcc_type, element_dcc_path)
        if port_element_dcc_obj.get_is_exists() is True:
            port_element_dcc_obj.get_port(element_dcc_port).set(vsn_raw)
            port_element_dcc_obj.get_port('selection').set('/*')
            port_element_dcc_obj.get_port('look').set('default')
            #
            port_element_dcc_obj.get_port('inputs[0]').set_source(
                ma_dcc_objects.AndStringReplace(utl_prd_configure.Name.AR_PATH_CONVERT).get_port('out')
            )

    def _set_mtl_mtx_ist_create_(self, container_opt, element_opt):
        self._set_mtl_mtx_create_(container_opt, element_opt)

    def _set_crd_abc_create_(self, container_opt, element_opt):
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
        port_element_dcc_obj = ma_dcc_objects.Node(element_dcc_path)
        port_element_dcc_obj.set_ancestors_create()
        #
        dcc_element_shape_dcc_path, _ = port_element_dcc_obj.get_dcc_instance(element_dcc_type, element_dcc_path, compose=True)
        dcc_element_shape_dcc_obj = ma_dcc_objects.Shape(dcc_element_shape_dcc_path)
        if dcc_element_shape_dcc_obj.get_is_exists() is True:
            dcc_element_shape_dcc_obj.get_port(element_dcc_port).set(vsn_raw)
            #
            mtl_mtx_dcc_path = container_opt.get_mtl_mtx_dcc_path()
            dcc_mtl_mtx = ma_dcc_objects.AndMaterialx(mtl_mtx_dcc_path)
            if dcc_mtl_mtx.get_is_exists() is True:
                dcc_mtl_mtx.get_port('out').set_target(dcc_element_shape_dcc_obj.get_port('operators[0]'))
            else:
                pass

    def _set_hou_dta_create_(self, container_opt, element_opt):
        pass

    def get_crt_plf_file_path(self):
        pass

    def get_is_plf_file_path_changed(self):
        pass
