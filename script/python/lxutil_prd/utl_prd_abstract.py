# coding:utf-8
import json

import parse

import copy

import string

from lxscheme import scm_objects

from lxobj import obj_configure

from lxutil import utl_configure, utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxutil_prd import utl_prd_configure, utl_prd_core


class AbsObjScene(object):
    UNIVERSE_CLASS = None
    APPLICATION_NAME = None
    def __init__(self):
        self._universe = None
        #
        self._search_categories = [
            utl_prd_configure.ObjCategory.PROJECT,
            utl_prd_configure.ObjCategory.STAGE,
            utl_prd_configure.ObjCategory.ENTITIES,
            utl_prd_configure.ObjCategory.TAG,
            utl_prd_configure.ObjCategory.ENTITY,
            utl_prd_configure.ObjCategory.STEP
        ]
        #
        self._current_obj = None
        self._current_project_obj = None
        self._current_stage_obj = None
        self._current_entity_obj = None
        self._current_step_obj = None
        #
        self._universe = self.UNIVERSE_CLASS()
        #
        self._scene_format_dict = {}
        # platform
        if utl_core._plf__get_is_windows_():
            for k, v in {
                'self.root.plf_root': 'l:'
            }.items():
                self._scene_format_dict[k] = v
        elif utl_core._plf__get_is_linux_():
            for k, v in {
                'self.root.plf_root': '/l'
            }.items():
                self._scene_format_dict[k] = v
        else:
            for k, v in {
                'self.root.plf_root': '/l'
            }.items():
                self._scene_format_dict[k] = v
        # application
        if utl_core._app__get_is_maya_():
            for k, v in {
                'self.application.name': 'maya',
                'self.application.pathsep': '|'
            }.items():
                self._scene_format_dict[k] = v
        elif utl_core._app__get_is_houdini_():
            for k, v in {
                'self.application.name': 'houdini',
                'self.application.pathsep': '/'
            }.items():
                self._scene_format_dict[k] = v
        else:
            # for k, v in {
            #     'self.application.name': 'maya',
            #     'self.application.pathsep': '|'
            # }.items():
            #     self._scene_format_dict[k] = v
            for k, v in {
                'self.application.name': 'houdini',
                'self.application.pathsep': '/'
            }.items():
                self._scene_format_dict[k] = v

        self._set_types_build_()
    @property
    def universe(self):
        return self._universe
    @classmethod
    def _set_plf_path_convert_(cls, file_path):
        if utl_core._plf__get_is_windows_():
            if file_path.startswith('/'):
                return 'l:{}'.format(file_path)
            return file_path
        elif utl_core._plf__get_is_linux_():
            if ':' in file_path:
                file_path = file_path.split(':')[-1]
                return file_path
            return file_path
    @classmethod
    def _set_root_convert_(cls, file_path):
        if utl_core._plf__get_is_linux_():
            if file_path.startswith('/prod'):
                file_path = '/l{}'.format(file_path)
            return file_path
        return file_path

    def set_load_by_scene_file_path(self, file_path):
        if file_path:
            os_file = utl_dcc_objects.OsFile(self._set_root_convert_(file_path))
            self._set_thread_build_(os_file.path)
            self._set_obj_types_variant_update_()

    def set_load_by_reference_file_paths(self, file_paths):
        entity_objs = self.get_entity_objs()
        if entity_objs:
            for file_path, namespace in file_paths:
                index = 0
                reference_args = namespace, index
                self._set_reference_build_(self._set_root_convert_(file_path), reference_args)

    def set_load_by_container_file_paths(self, file_paths):
        pass
    @classmethod
    def _set_variant_convert_(cls, variant, format_dict):
        return utl_prd_core._var__set_convert_(variant, format_dict)
    @classmethod
    def _get_obj_format_dict_(cls, obj):
        return utl_prd_core._obj__get_format_dict_(obj)

    def _set_types_build_(self):
        self._type_configures_scheme = utl_prd_configure.Scheme.UTILITY_TYPES
        application_name = self._scene_format_dict['self.application.name']
        if application_name == utl_configure.App.HOUDINI:
            self._type_configures_scheme.set_layer_load(utl_prd_configure.Scheme.HOUDINI_TYPES)
        elif application_name == utl_configure.App.MAYA:
            self._type_configures_scheme.set_layer_load(utl_prd_configure.Scheme.MAYA_TYPES)
        # category and type
        for category_name, type_name in obj_configure.Type.ALL:
            self.universe._get_type_force_(category_name, type_name)
        # obj category
        for obj_category_name in utl_prd_configure.ObjCategory.ALL:
            obj_category = self.universe._get_obj_category_force_(obj_category_name)
            obj_category_scheme_key = obj_category.path.replace(obj_category.pathsep, '/')
            obj_category_scheme = self._type_configures_scheme.get_content(obj_category_scheme_key)
            obj_category_raw = obj_category_scheme.value
            if obj_category_raw is not None:
                obj_category._set_port_queries_build_(obj_category_raw, self._type_configures_scheme.set_variant_convert)
        # obj type
        for obj_category_name, obj_type_name in utl_prd_configure.ObjType.ALL:
            obj_type = self.universe._get_obj_type_force_(obj_category_name, obj_type_name)
            obj_type_scheme_key = obj_type.path.replace(obj_type.pathsep, '/')
            obj_type_scheme = self._type_configures_scheme.get_content(obj_type_scheme_key)
            obj_type_raw = obj_type_scheme.value
            if obj_type_raw is not None:
                obj_type._set_port_queries_build_(
                    obj_type_raw, self._type_configures_scheme.set_variant_convert
                )
    #
    def _set_obj_types_variant_update_(self):
        current_obj = self._current_obj
        if current_obj is not None:
            format_dict = copy.deepcopy(self._scene_format_dict)
            for obj_type in self.universe.get_obj_types():
                self._set_obj_type_variant_update_(obj_type, format_dict)
    # noinspection PyMethodMayBeStatic
    def _set_obj_type_variant_update_(self, obj_type, format_dict):
        platform_formats = [
            'plf_name',
            'plf_path'
        ]
        ett_brhs = obj_type.get_variant('ett_brhs')
        port_paths = []
        if ett_brhs:
            for branch in ett_brhs:
                for key_format in platform_formats:
                    port_paths.append('{}.{}'.format(branch, key_format))
        else:
            for key_format in platform_formats:
                port_paths.append(key_format)
        #
        application_names = [
            'maya',
            'houdini',
            'shotgun'
        ]
        dcc_formats = [
            'dcc_name',
            'dcc_path'
        ]
        for application_name in application_names:
            if ett_brhs:
                for branch_key in ett_brhs:
                    for key_format in dcc_formats:
                        port_paths.append('{}.{}.{}'.format(branch_key, application_name, key_format))
            else:
                for key_format in dcc_formats:
                    port_paths.append('{}.{}'.format(application_name, key_format))

        for port_path in port_paths:
            raw_format = obj_type.get_variant(port_path)
            if raw_format is not None:
                raw = self._set_variant_convert_(raw_format, format_dict)
                key = 'self.type.{}'.format(port_path)
                obj_type._set_port_query_build_(key, raw)

    def _get_dcc_name_key_(self, branch_key, is_reference, format_dict):
        port_path = self._set_variant_convert_(
            '{self.application.name}.dcc_name', format_dict
        )
        if branch_key is not None:
            port_path = '{}.{}'.format(branch_key, port_path)
        if is_reference is True:
            port_path = '{}.{}'.format('reference', port_path)
        return port_path

    def _get_dcc_path_key_(self, branch_key, is_reference, format_dict):
        port_path = self._set_variant_convert_(
            '{self.application.name}.dcc_path', format_dict
        )
        if branch_key is not None:
            port_path = '{}.{}'.format(branch_key, port_path)
        if is_reference is True:
            port_path = '{}.{}'.format('reference', port_path)
        return port_path

    def _set_obj_extra_update_(self, obj_type, format_dict):
        if obj_type.category.name == utl_prd_configure.ObjCategory.STEP:
            self._set_step_extra_update_(obj_type, format_dict)

    def _set_dcc_group_paths_build_(self, obj_type, branch_key, format_dict):
        port_path = self._set_variant_convert_(
            '{self.application.name}.dcc_group_paths', format_dict
        )
        if branch_key is not None:
            port_path = '{}.{}'.format(branch_key, port_path)
        port_query = obj_type.get_variant_port_query(port_path)
        if port_query:
            raw = port_query.get()
            if raw:
                pathsep = format_dict['self.application.pathsep']
                variant = [
                    self._set_variant_convert_(
                        i,
                        format_dict
                    ).replace('/', pathsep)
                    for i in raw
                ]
                format_dict['self.dcc_group_paths'] = variant
                format_dict['self.{}.dcc_group_paths'.format(obj_type.category.name)] = variant

    def _set_dependents_build_(self, obj_type, format_dict, branch_key):
        if branch_key is None:
            port_path_format = 'dependents'
        else:
            port_path_format = '{}.dependents'.format(branch_key)
        #
        port_query = obj_type.get_variant_port_query(
            self._set_variant_convert_(
                port_path_format,
                format_dict
            )
        )
        if port_query:
            raw = port_query.get()
            lis = []
            if raw:
                for i in raw:
                    obj_type = self.universe.get_obj_type(i)
                    obj = self._set_obj_create_(
                        obj_type, format_dict, branch_key
                    )
                    lis.append(obj.path)
            format_dict['self.dependents'] = lis

    def _set_thread_build_(self, file_path):
        obj = None
        branch_key = None
        format_dict = copy.deepcopy(self._scene_format_dict)
        for obj_category_name in self._search_categories:
            obj_category = self.universe.get_obj_category(obj_category_name)
            obj, branch_key, format_dict = self._get_obj_(obj_category, obj, file_path, format_dict, branch_key)
            if obj is None:
                break
            #
            if obj_category_name == utl_prd_configure.ObjCategory.PROJECT:
                self._current_project_obj = obj
            elif obj_category_name == utl_prd_configure.ObjCategory.STAGE:
                self._current_stage_obj = obj
            elif obj_category_name == utl_prd_configure.ObjCategory.ENTITY:
                self._current_entity_obj = obj
            elif obj_category_name == utl_prd_configure.ObjCategory.STEP:
                self._current_step_obj = obj
            #
            self._current_obj = obj
    # noinspection PyMethodMayBeStatic
    def _set_obj_branch_update_(self, pre_obj, format_dict):
        branch_category = pre_obj.category.name
        branch_key = pre_obj.type.name
        format_dict['self.{}.type'.format(branch_category)] = branch_key
    # noinspection PyMethodMayBeStatic
    def _set_obj_reference_update_(self, reference_type, reference_namespace, format_dict):
        format_dict['self.reference.key'] = reference_type
        format_dict['self.reference.namespace'] = reference_namespace
    #
    def _set_obj_type_reference_update_(self, obj_type, format_dict, reference_args):
        is_reference = False
        if reference_args is not None:
            reference_namespace, index = reference_args
            container_type_port_query = obj_type.get_variant_port_query('reference.key')
            if container_type_port_query:
                reference_type = container_type_port_query.get()
                if reference_type:
                    self._set_obj_reference_update_(reference_type, reference_namespace, format_dict)
                is_reference = True
        return is_reference
    @classmethod
    def _get_obj_type_is_branch_(cls, obj_type):
        raw = obj_type.get_variant('branch')
        if raw is True:
            return True
        return False
    @classmethod
    def _get_obj_type_branch_key_(cls, obj_type):
        raw = obj_type.get_variant('branch')
        if raw is True:
            return obj_type.name
        return None
    # noinspection PyMethodMayBeStatic
    def _set_obj_type_update_(self, obj_type, format_dict):
        port_path = 'self.{}.type'.format(obj_type.category.name)
        format_dict[port_path] = obj_type.name
    # source key
    @classmethod
    def _get_obj_type_branch_source_key_(cls, obj_type, variant_key, branch_key):
        if branch_key is not None:
            source_key = '{}.{}'.format(branch_key, variant_key)
        else:
            source_key = variant_key
        return source_key
    @classmethod
    def _get_obj_type_reference_branch_source_key_(cls, obj_type, variant_key, branch_key):
        if branch_key is not None:
            source_key = 'reference.{}.{}'.format(branch_key, variant_key)
        else:
            source_key = 'reference.{}'.format(variant_key)
        return source_key
    #
    def _set_obj_variant_update_(self, obj_type, format_dict, variant_key, branch_key, is_reference):
        source_key = self._get_obj_type_branch_source_key_(obj_type, variant_key, branch_key)
        #
        raw_format = obj_type.get_variant(source_key)
        if raw_format:
            format_dict['self.{}@format'.format(variant_key)] = raw_format
            raw = self._set_variant_convert_(
                raw_format,
                format_dict
            )
        else:
            raw = None
        #
        category_key = obj_type.category.name
        if obj_type.get_variant('category') is not None:
            category_key = obj_type.get_variant('category')
        #
        format_dict['self.{}'.format(variant_key)] = raw
        format_dict['self.{}.{}'.format(category_key, variant_key)] = raw
        #
        if self._get_obj_type_is_branch_(obj_type) is True:
            format_dict['self.{}.{}'.format(obj_type.name, variant_key)] = raw

        if is_reference is True:
            source_key = self._get_obj_type_reference_branch_source_key_(obj_type, variant_key, branch_key)
            raw_format = obj_type.get_variant(source_key)
            if raw_format is not None:
                format_dict['self.reference.{}@format'.format(variant_key)] = raw_format
                raw = self._set_variant_convert_(
                    raw_format,
                    format_dict
                )
            else:
                raw = None
            format_dict['self.reference.{}'.format(variant_key)] = raw
            format_dict['self.reference.{}.{}'.format(category_key, variant_key)] = raw
            #
            if self._get_obj_type_is_branch_(obj_type) is True:
                format_dict['self.reference.{}.{}'.format(obj_type.name, variant_key)] = raw
    # dcc source key
    @classmethod
    def _get_obj_type_dcc_branch_source_key_(cls, obj_type, variant_key, branch_key, dcc_key):
        if branch_key is not None:
            source_key = '{}.{}.{}'.format(branch_key, dcc_key, variant_key)
        else:
            source_key = '{}.{}'.format(dcc_key, variant_key)
        return source_key
    @classmethod
    def _get_obj_type_dcc_reference_branch_source_key_(cls, obj_type, variant_key, branch_key, dcc_key):
        if branch_key is not None:
            source_key = 'reference.{}.{}.{}'.format(branch_key, dcc_key, variant_key)
        else:
            source_key = 'reference.{}.{}'.format(dcc_key, variant_key)
        return source_key
    #
    def _get_obj_(self, obj_category, pre_obj, file_path, format_dict, branch_key, reference_args=None):
        obj = None
        obj_types = obj_category.get_types()
        for obj_type in obj_types:
            # branch
            if branch_key is not None:
                self._set_obj_branch_update_(pre_obj, format_dict)
            #
            is_reference = self._set_obj_type_reference_update_(obj_type, format_dict, reference_args)
            #
            plf_path_key = self._get_obj_type_branch_source_key_(obj_type, 'plf_path', branch_key)
            plf_path_format = obj_type.get_variant(plf_path_key)
            if plf_path_format is None:
                continue
            #
            obj_plf_path_search_key = '{}/{{parse_extra}}'.format(
                self._set_variant_convert_(
                    plf_path_format,
                    format_dict
                )
            )
            p = parse.parse(
                obj_plf_path_search_key,
                file_path
            )
            if p is None:
                continue
            #
            p_result = p.named
            # update format dict
            for k, v in p_result.items():
                format_dict[k] = v
            #
            obj = self._set_obj_create_(
                obj_type, format_dict, branch_key, is_reference
            )
            branch_key = self._get_obj_type_branch_key_(obj_type)
        return obj, branch_key, format_dict
    #
    def _set_obj_dcc_variant_update_(self, obj_type, format_dict, variant_key, branch_key, is_reference, dcc_key, pathsep):
        source_key = self._get_obj_type_dcc_branch_source_key_(obj_type, variant_key, branch_key, dcc_key)
        #
        raw_format = obj_type.get_variant(source_key)
        if raw_format:
            raw = self._set_variant_convert_(
                raw_format,
                format_dict
            ).replace('/', pathsep)
        else:
            raw = None
        #
        category_key = obj_type.category.name
        if obj_type.get_variant('category') is not None:
            category_key = obj_type.get_variant('category')
        #
        format_dict['self.{}'.format(variant_key)] = raw
        format_dict['self.{}.{}'.format(category_key, variant_key)] = raw
        #
        if self._get_obj_type_is_branch_(obj_type) is True:
            format_dict['self.{}.{}'.format(obj_type.name, variant_key)] = raw

        if is_reference is True:
            source_key = self._get_obj_type_dcc_reference_branch_source_key_(obj_type, variant_key, branch_key, dcc_key)
            raw_format = obj_type.get_variant(source_key)
            if raw_format is not None:
                raw = self._set_variant_convert_(
                    raw_format,
                    format_dict
                ).replace('/', pathsep)
            else:
                raw = None
            format_dict['self.reference.{}'.format(variant_key)] = raw
            format_dict['self.reference.{}.{}'.format(category_key, variant_key)] = raw
            #
            if self._get_obj_type_is_branch_(obj_type) is True:
                format_dict['self.reference.{}.{}'.format(obj_type.name, variant_key)] = raw
    #
    def _set_obj_reference_variant_update_(self):
        pass
    @classmethod
    def _get_obj_type_port_query_key_(cls, variant_key, branch_key, is_reference):
        port_query_key = variant_key
        if branch_key is not None:
            port_query_key = '{}.{}'.format(branch_key, port_query_key)
        if is_reference is True:
            port_query_key = '{}.{}'.format('reference', port_query_key)
        return port_query_key
    # platform
    def _set_obj_plf_name_update_(self, obj_type, format_dict, branch_key, is_reference):
        variant_key = 'plf_name'
        self._set_obj_variant_update_(obj_type, format_dict, variant_key, branch_key, is_reference)
    #
    def _set_obj_plf_path_update_(self, obj_type, format_dict, branch_key, is_reference):
        variant_key = 'plf_path'
        self._set_obj_variant_update_(obj_type, format_dict, variant_key, branch_key, is_reference)
    # main
    def _set_obj_name_update_(self, obj_type, format_dict, branch_key, is_reference):
        variant_key = 'name'
        self._set_obj_variant_update_(obj_type, format_dict, variant_key, branch_key, is_reference)

    def _set_obj_path_update_(self, obj_type, format_dict, branch_key, is_reference):
        variant_key = 'path'
        self._set_obj_variant_update_(obj_type, format_dict, variant_key, branch_key, is_reference)
    # dcc
    def _set_obj_dcc_name_update_(self, obj_type, format_dict, branch_key, is_reference, dcc_key, pathsep):
        variant_key = 'dcc_name'
        self._set_obj_dcc_variant_update_(obj_type, format_dict, variant_key, branch_key, is_reference, dcc_key, pathsep)

    def _set_obj_dcc_path_update_(self, obj_type, format_dict, branch_key, is_reference, dcc_key, pathsep):
        variant_key = 'dcc_path'
        self._set_obj_dcc_variant_update_(obj_type, format_dict, variant_key, branch_key, is_reference, dcc_key, pathsep)

    def _set_obj_container_update_(self, obj_type, format_dict):
        pass

    def _set_obj_create_(self, obj_type, format_dict, branch_key, is_reference=False):
        if is_reference is False:
            self._set_dependents_build_(obj_type, format_dict, branch_key)
        #
        self._set_dcc_group_paths_build_(obj_type, branch_key, format_dict)
        # platform
        self._set_obj_plf_name_update_(obj_type, format_dict, branch_key, is_reference)
        self._set_obj_plf_path_update_(obj_type, format_dict, branch_key, is_reference)
        # extra
        self._set_obj_extra_update_(obj_type, format_dict)
        # main
        self._set_obj_name_update_(obj_type, format_dict, branch_key, is_reference)
        self._set_obj_path_update_(obj_type, format_dict, branch_key, is_reference)
        #
        self._set_obj_type_update_(obj_type, format_dict)
        # dcc
        dcc_key = format_dict['self.application.name']
        pathsep = format_dict['self.application.pathsep']
        self._set_obj_dcc_name_update_(obj_type, format_dict, branch_key, is_reference, dcc_key, pathsep)
        self._set_obj_dcc_path_update_(obj_type, format_dict, branch_key, is_reference, dcc_key, pathsep)
        #
        obj_path_ = format_dict['self.path']
        if is_reference is True:
            obj_path_ = format_dict['self.reference.path']
        # create obj
        obj = obj_type.set_obj_create(obj_path_)
        [obj._set_port_build_(k, v) for k, v in format_dict.items()]
        return obj

    def _set_reference_build_(self, file_path, reference_args):
        obj = None
        branch_key = None
        format_dict = copy.deepcopy(self._scene_format_dict)
        # current_step = self._current_step_obj
        # format_dict = utl_prd_core._obj__get_format_dict_(current_step)
        for obj_category_name in self._search_categories:
            obj_category = self.universe.get_obj_category(obj_category_name)
            obj, branch_key, format_dict = self._get_obj_(obj_category, obj, file_path, format_dict, branch_key, reference_args)
            if obj is None:
                break

    def get_project_objs(self):
        obj_category = self.universe.get_obj_category(
            utl_prd_configure.ObjCategory.PROJECT
        )
        return obj_category.get_objs()

    def get_entity_objs(self):
        obj_category = self.universe.get_obj_category(
            utl_prd_configure.ObjCategory.ENTITY
        )
        return obj_category.get_objs()

    def get_step_objs(self):
        obj_category = self.universe.get_obj_category(
            utl_prd_configure.ObjCategory.STEP
        )
        return obj_category.get_objs()

    def get_objs(self):
        return self._universe.get_objs()

    def get_current_obj(self):
        return self._current_obj

    def get_current_project_obj(self):
        project_type = self.universe.get_obj_type(utl_prd_configure.ObjType.MOVIE)
        projects = project_type.get_objs()
        if projects:
            return projects[-1]

    def get_current_stage_obj(self):
        return self._current_stage_obj

    def get_current_entity_obj(self):
        return self._current_entity_obj

    def get_current_step_obj(self):
        return self._current_step_obj

    def _set_step_extra_update_(self, obj_type, format_dict):
        self._set_step_extra_variant_update_(obj_type, format_dict)
        #
        rlt_plf_file_path = format_dict['parse_extra']
        port_path_format = '{self.stage.type}.{self.entity.type}.{self.application.name}.rlt_plf_file_paths'
        port_path = self._set_variant_convert_(port_path_format, format_dict)
        raw = obj_type.get_variant(
            port_path
        )
        if raw:
            for key, value in raw.items():
                rlt_plf_file_path_raws = []
                if isinstance(value, (str, unicode)):
                    rlt_plf_file_path_raws = [value]
                elif isinstance(value, (tuple, list)):
                    rlt_plf_file_path_raws = value
                for rlt_plf_file_path_raw in rlt_plf_file_path_raws:
                    rlt_plf_file_path_format = self._type_configures_scheme.set_variant_convert(rlt_plf_file_path_raw)
                    plf_rlt_file_path_search_key = self._set_variant_convert_(rlt_plf_file_path_format, format_dict)
                    p = parse.parse(
                        plf_rlt_file_path_search_key, rlt_plf_file_path
                    )
                    if not p:
                        continue
                    if p:
                        p_result = p.named
                        for k, v in p_result.items():
                            if k != 'parse_extra':
                                format_dict[k] = v

    def _set_step_extra_variant_update_(self, obj_type, format_dict):
        stage_category = self.universe.get_obj_category(utl_prd_configure.ObjCategory.STAGE)
        stage_types = stage_category.get_types()
        stage_type_names = [i.name for i in stage_types]
        format_keys = [
            ('rlt_plf_path', '{self.stage.type}/{self.entity.type}/{self.application.name}/rlt_plf_paths'),
            ('rlt_plf_file_path', '{self.stage.type}/{self.entity.type}/{self.application.name}/rlt_plf_file_paths')
        ]
        for stage_type_name in stage_type_names:
            for key, format_key in format_keys:
                format_dict_ = copy.deepcopy(format_dict)
                format_dict_['self.stage.type'] = stage_type_name
                port_query_path = self._set_variant_convert_(format_key, format_dict_)
                raw = obj_type.get_variant(port_query_path)
                if raw:
                    for k, v in raw.items():
                        variant_key = 'self.{}.{}.{}@format'.format(key, k, stage_type_name)
                        variant = self._type_configures_scheme.set_variant_convert(v)
                        obj_type._set_port_query_build_(variant_key, variant)

    def get_task_objs(self):
        pass

    def _test(self):
        pass
    @property
    def format_dict(self):
        return self._scene_format_dict


class AbsObjTypeOp(object):
    def __init__(self, obj_type):
        self._obj_type = obj_type
        self._format_dict = {}
        #
        self._format_dict = utl_prd_core._obj_type__get_variants_(self.obj_type)
    @property
    def obj_type(self):
        return self._obj_type
    @classmethod
    def _set_variant_convert_(cls, variant, format_dict):
        return utl_prd_core._var__set_convert_(variant, format_dict)

    def get_format_dict(self, regex=None):
        if regex is not None:
            return utl_prd_core._dict__set_filter_(self._format_dict, regex)
        return self._format_dict

    def get_variant(self, key, branch=None):
        if branch is not None:
            ett_brhs = self.obj_type.get_variant('ett_brhs')
            if branch in ett_brhs:
                key = '{}.{}'.format(branch, key)
                return self.obj_type.get_variant(key)
            return None
        key = '{}'.format(key)
        return self.obj_type.get_variant(key)

    def set_format_dict(self, format_dict):
        self._format_dict = format_dict

    def __str__(self):
        return json.dumps(
            self.get_format_dict(),
            indent=4
        )


class AbsObjOptDef(object):
    OBJ_TYPE_OP_CLASS = None
    def _set_obj_opt_def_init_(self, obj):
        self._obj = obj
        self._format_dict = utl_prd_core._obj__get_format_dict_(self.obj)
    @property
    def universe(self):
        return self.obj.universe
    @property
    def obj(self):
        return self._obj
    @property
    def type(self):
        return self.obj.type.name
    @property
    def name(self):
        return self.obj.name
    @property
    def path(self):
        return self.obj.path
    @property
    def icon(self):
        port = self.obj.get_variant_port('icon')
        if port:
            icon_name = port.get()
            return utl_core.Icon.get(icon_name)
        return utl_core.Icon.get('tag')
    #
    def get_format_dict(self, regex=None):
        if regex is not None:
            pass
        return self._format_dict

    def get_variant(self, key):
        return self._get_obj_variant_(key)
    @classmethod
    def _get_obj_format_dict_(cls, obj):
        return utl_prd_core._obj__get_format_dict_(obj)
    @classmethod
    def _set_variant_convert_(cls, variant, format_dict):
        if isinstance(variant, (str, unicode)):
            return utl_prd_core._var__set_convert_(variant, format_dict)
        return variant
    @classmethod
    def _set_variant_inherit_(cls, format_dict):
        return copy.deepcopy(format_dict)
    @classmethod
    def _get_match_plf_paths_(cls, plf_path_format, trim=(-5, None)):
        return utl_prd_core._plf_path__get_glob_(plf_path_format, trim=trim)
    @classmethod
    def _get_plf_path_sequence_number_(cls, plf_path):
        return utl_prd_core._plf_path__get_sequence_(plf_path)
    @classmethod
    def _set_main_variant_update_(cls, obj_type, obj_format_dict, scheme_key, variant_key, format_dict_override=None):
        if scheme_key is None:
            variant_format = obj_type.get_variant(variant_key)
        else:
            variant_format = obj_type.get_variant('{}.{}'.format(scheme_key, variant_key))
        if variant_format is not None:
            if format_dict_override is not None:
                variant = cls._set_variant_convert_(variant_format, format_dict_override)
            else:
                variant = cls._set_variant_convert_(variant_format, obj_format_dict)
            #
            category_key = obj_type.category.name
            if obj_type.get_variant('category') is not None:
                category_key = obj_type.get_variant('category')
            #
            obj_format_dict['self.{}.{}'.format(category_key, variant_key)] = variant
            obj_format_dict['self.{}'.format(variant_key)] = variant
            return variant
    @classmethod
    def _set_dcc_main_variant_update_(cls, obj_type, obj_format_dict, variant_key):
        application_name = obj_format_dict['self.application.name']
        pathsep = obj_format_dict['self.application.pathsep']
        #
        variant_format = obj_type.get_variant('{}.{}'.format(application_name, variant_key))
        variant = cls._set_variant_convert_(variant_format, obj_format_dict)
        variant = variant.replace('/', pathsep)
        category_key = obj_type.category.name
        if obj_type.get_variant('category') is not None:
            category_key = obj_type.get_variant('category')
        #
        obj_format_dict['self.{}.{}'.format(category_key, variant_key)] = variant
        obj_format_dict['self.{}'.format(variant_key)] = variant
        return variant
    @classmethod
    def _set_dcc_scheme_variant_update_(cls, obj_type, obj_format_dict, scheme_key, variant_key):
        application_name = obj_format_dict['self.application.name']
        pathsep = obj_format_dict['self.application.pathsep']
        #
        variant_format = obj_type.get_variant('{}.{}.{}'.format(scheme_key, application_name, variant_key))
        if variant_format is not None:
            if isinstance(variant_format, (str, unicode)):
                variant = cls._set_variant_convert_(variant_format, obj_format_dict)
                variant = variant.replace('/', pathsep)
            else:
                variant = variant_format
            #
            category_key = obj_type.category.name
            if obj_type.get_variant('category') is not None:
                category_key = obj_type.get_variant('category')
            #
            obj_format_dict['self.{}.{}'.format(category_key, variant_key)] = variant
            obj_format_dict['self.{}'.format(variant_key)] = variant
            return variant
    @classmethod
    def _set_dcc_sub_variant_update_(cls, obj_type, obj_format_dict, sub_key, variant_key):
        application_name = obj_format_dict['self.application.name']
        pathsep = obj_format_dict['self.application.pathsep']
        #
        variant_format = obj_type.get_variant('{}.{}.{}'.format(sub_key, application_name, variant_key))
        if isinstance(variant_key, (str, unicode)):
            variant = cls._set_variant_convert_(variant_format, obj_format_dict)
            variant = variant.replace('/', pathsep)
        else:
            variant = variant_format
        category_key = obj_type.category.name
        if obj_type.get_variant('category') is not None:
            category_key = obj_type.get_variant('category')
        #
        obj_format_dict['self.{}.{}.{}'.format(category_key, sub_key, variant_key)] = variant
        # obj_format_dict['self.{}.{}'.format(sub_key, variant_key)] = variant
        return variant
    @classmethod
    def _set_dcc_main_port_name_variant_update_(cls, obj_type, obj_format_dict, branch_name, data_scheme, variant_key):
        application_name = obj_format_dict['self.application.name']
        pathsep = obj_format_dict['self.application.pathsep']
        #
        branch = obj_type.get_variant('{}.{}.branch'.format(data_scheme, application_name)) or False
        if branch is True:
            variant_format = obj_type.get_variant(
                '{}.{}.{}.{}.dcc_port_name'.format(data_scheme, branch_name, application_name, variant_key)
            )
        else:
            variant_format = obj_type.get_variant(
                '{}.{}.{}.dcc_port_name'.format(data_scheme, application_name, variant_key)
            )
        #
        if variant_format is not None:
            variant = cls._set_variant_convert_(variant_format, obj_format_dict)
            if isinstance(variant, (str, unicode)):
                variant = variant.replace('/', pathsep)
            #
            category_key = obj_type.category.name
            if obj_type.get_variant('category') is not None:
                category_key = obj_type.get_variant('category')
            #
            obj_format_dict['self.{}.{}.dcc_port_name'.format(category_key, variant_key)] = variant
            obj_format_dict['self.{}.dcc_port_name'.format(variant_key)] = variant
            return variant
    #
    def set_variant_print(self):
        print json.dumps(self.get_format_dict(), indent=4)

    def _get_obj_variant_(self, key):
        return self.obj.get_variant(key)

    def __str__(self):
        return '{}(path={})'.format(
            self.__class__.__name__,
            self.path
        )

    def __repr__(self):
        return self.__str__()


class AbsObjOp(AbsObjOptDef):
    def __init__(self, obj):
        self._set_obj_opt_def_init_(obj)
    # platform
    @property
    def plf_name(self):
        return self._get_obj_variant_('self.plf_name')
    @property
    def plf_path(self):
        return self._get_obj_variant_('self.plf_path')
    # dcc
    @property
    def dcc_name(self):
        return self._obj.get_variant('self.dcc_name')
    @property
    def dcc_path(self):
        return self._obj.get_variant('self.dcc_path')
    # reference
    @property
    def reference_key(self):
        return self._obj.get_variant('self.reference.key') or ''
    @property
    def version(self):
        if self._obj.category.name == utl_prd_configure.ObjCategory.STEP:
            return self._obj.get_variant('self.version.plf_name') or ''
        return ''
    @property
    def label(self):
        if self._obj.category.name == utl_prd_configure.ObjCategory.STEP:
            return self._obj.get_variant('self.dta_ctg.plf_name') or ''
        return ''

    def get_dcc_group_paths(self):
        port = self._obj.get_variant_port('self.dcc_group_paths')
        if port:
            return port.get() or []
        return []

    def _test(self):
        pass

    def __str__(self):
        return json.dumps(self.get_format_dict(), indent=4)


class AbsObjReferenceOp(AbsObjOptDef):
    def __init__(self, obj):
        self._set_obj_opt_def_init_(obj)
    # main
    @property
    def path(self):
        return self._get_obj_variant_('self.reference.path')
    @property
    def name(self):
        return self._get_obj_variant_('self.reference.name')
    # platform
    @property
    def plf_name(self):
        return self._get_obj_variant_('self.reference.plf_name')
    @property
    def plf_path(self):
        return self._get_obj_variant_('self.reference.plf_path')
    # dcc
    @property
    def dcc_name(self):
        return self._obj.get_variant('self.reference.dcc_name')
    @property
    def dcc_path(self):
        return self._obj.get_variant('self.reference.dcc_path')
    # reference
    @property
    def reference_key(self):
        return self._obj.get_variant('self.reference.key') or ''

    @property
    def version(self):
        if self._obj.category.name == utl_prd_configure.ObjCategory.STEP:
            return self._obj.get_variant('self.version.plf_name') or ''
        return ''
    @property
    def label(self):
        if self._obj.category.name == utl_prd_configure.ObjCategory.STEP:
            return self._obj.get_variant('self.dta_ctg.plf_name') or ''
        return ''


class AbsObjStorageOp(AbsObjOptDef):
    def __init__(self, obj):
        self._set_obj_opt_def_init_(obj)

    def _get_root_(self, stage_type_name):
        format_dict = copy.deepcopy(self._format_dict)
        stage_type = self.universe.get_obj_type(stage_type_name)
        plf_name = stage_type.get_variant('self.plf_name')
        format_dict['self.stage.plf_name'] = plf_name
        plt_path_format = format_dict.get(
            'self.plf_path@format'
        )
        if plt_path_format:
            return utl_prd_core._var__set_convert_(plt_path_format, format_dict)

    def _get_path_variant_(self, root, path_format):
        relative_plf_path = self._set_variant_convert_(path_format, self._format_dict)
        return '{}/{}'.format(root, relative_plf_path)

    def _get_path_(self, root, key, stage_type_name):
        raw = self.get_variant('self.rlt_plf_path.{}.{}@format'.format(key, stage_type_name))
        if raw is not None:
            if isinstance(raw, (str, unicode)):
                return self._get_path_variant_(root, raw)
            elif isinstance(raw, (tuple, list)):
                return [self._get_path_variant_(root, i) for i in raw]

    def _get_file_path_(self, root, key, stage_type_name):
        raw = self.get_variant('self.rlt_plf_file_path.{}.{}@format'.format(key, stage_type_name))
        if raw is not None:
            if isinstance(raw, (str, unicode)):
                return self._get_path_variant_(root, raw)
            elif isinstance(raw, (tuple, list)):
                return [self._get_path_variant_(root, i) for i in raw]
    # source
    def get_src_root(self):
        return self._get_root_(utl_prd_configure.ObjType.SOURCE)

    def get_src_path(self, key):
        return self._get_path_(self.get_src_root(), key, utl_prd_configure.ObjType.SOURCE)

    def get_src_file_path(self, key):
        return self._get_file_path_(self.get_src_root(), key, utl_prd_configure.ObjType.SOURCE)
    # product
    def get_prd_root(self):
        return self._get_root_(utl_prd_configure.ObjType.PRODUCT)

    def get_prd_path(self, key):
        return self._get_path_(self.get_prd_root(), key, utl_prd_configure.ObjType.PRODUCT)

    def get_prd_file_path(self, key):
        return self._get_file_path_(self.get_prd_root(), key, utl_prd_configure.ObjType.PRODUCT)

    def get_prd_last_version(self):
        pass
    # temporary
    def get_tmp_root(self):
        return self._get_root_(utl_prd_configure.ObjType.TEMPORARY)

    def get_tmp_path(self, key):
        return self._get_path_(self.get_tmp_root(), key, utl_prd_configure.ObjType.TEMPORARY)

    def get_tmp_file_path(self, key):
        return self._get_file_path_(self.get_tmp_root(), key, utl_prd_configure.ObjType.TEMPORARY)


class AbsEntitiesOptDef(object):
    SCENE_CLASS = None
    KWARG_KEYS = {
        'project': 'self.project.plf_name',
        'stage': 'self.stage.plf_name'
    }
    def __init__(self, **kwargs):
        self._scene = self.SCENE_CLASS()
        self._format_dict = self._set_variant_inherit_(self._scene.format_dict)
        for k, v in kwargs.items():
            if k in self.KWARG_KEYS:
                k = self.KWARG_KEYS[k]
            self._format_dict[k] = v
        #
        self._set_project_build_()
    @property
    def scene(self):
        return self._scene
    @property
    def universe(self):
        return self._scene.universe

    def _set_project_build_(self):
        if 'self.project.plf_name' in self._format_dict:
            universe = self._scene.universe
            project_format_dict = self._set_variant_inherit_(self._format_dict)
            project_type = universe.get_obj_type(utl_prd_configure.ObjType.MOVIE)
            name, path = [
                self._set_main_variant_update_(project_type, project_format_dict, variant_key)
                for variant_key in ['name', 'path']
            ]
            obj = project_type.set_obj_create(path)
            [obj._set_port_build_(k, v) for k, v in project_format_dict.items()]
    @classmethod
    def _set_variant_convert_(cls, variant, format_dict):
        return utl_prd_core._var__set_convert_(variant, format_dict)
    @classmethod
    def _set_variant_inherit_(cls, format_dict):
        return copy.deepcopy(format_dict)
    @classmethod
    def _get_match_plf_paths_(cls, plf_path_format, trim=(-5, None)):
        return utl_prd_core._plf_path__get_glob_(plf_path_format, trim=trim)
    @classmethod
    def _set_main_variant_update_(cls, obj_type, obj_format_dict, variant_key, format_dict_override=None):
        variant_format = obj_type.get_variant('{}'.format(variant_key))
        if variant_format is not None:
            if format_dict_override is not None:
                variant = cls._set_variant_convert_(variant_format, format_dict_override)
            else:
                variant = cls._set_variant_convert_(variant_format, obj_format_dict)
            category_key = obj_type.category.name
            if obj_type.get_variant('category') is not None:
                category_key = obj_type.get_variant('category')
            #
            obj_format_dict['self.{}.{}'.format(category_key, variant_key)] = variant
            obj_format_dict['self.{}'.format(variant_key)] = variant
            return variant

    def _set_rsv_file_create_(self, entity_type, entity_format_dict):
        name, path = [
            self._set_main_variant_update_(
                entity_type, entity_format_dict,
                variant_key
            )
            for variant_key in ['name', 'path']
        ]
        if path is not None:
            exists_obj = self.universe.get_obj(path)
            if exists_obj is None:
                for stage_key in ['prd', 'tmp']:
                    for variant_key in ['{}.plf_name'.format(stage_key), '{}.plf_path'.format(stage_key)]:
                        self._set_main_variant_update_(
                            entity_type, entity_format_dict,
                            variant_key
                        )
                #
                obj, is_create = entity_type.set_obj_create(path), True
                [obj._set_port_build_(k, v) for k, v in entity_format_dict.items()]
            else:
                obj, is_create = exists_obj, False
        else:
            obj, is_create = None, None
        return obj, is_create


class AbsSceneOpt(AbsEntitiesOptDef):
    SHOT_OPT_CLASS = None
    def __init__(self, **kwargs):
        super(AbsSceneOpt, self).__init__(**kwargs)
    @property
    def format_dict(self):
        return self._format_dict
    # shot
    def set_shots_build(self):
        universe = self._scene.universe
        shot_type = universe.get_obj_type(utl_prd_configure.ObjType.SHOT)
        shot_format_dict = self._set_variant_inherit_(self.format_dict)
        #
        plf_path_format = shot_type.get_variant('plf_path')
        plf_path_format = self._set_variant_convert_(plf_path_format, shot_format_dict)
        results = self._get_match_plf_paths_(plf_path_format, trim=None)
        for result in results:
            p = parse.parse(
                plf_path_format, result
            )
            if p:
                extra = p.named
                shot_format_dict.update(extra)
                self._set_rsv_file_create_(shot_type, shot_format_dict)

    def get_shots(self):
        universe = self._scene.universe
        return universe.get_obj_type(utl_prd_configure.ObjType.SHOT).get_objs()

    def get_shot_opts(self):
        return [self.SHOT_OPT_CLASS(i) for i in self.get_shots()]


class AbsEntityOpt(AbsObjOptDef):
    ENTITY_TYPE_NAME = None
    def __init__(self, obj):
        self._set_obj_opt_def_init_(obj)
    @property
    def prd_plf_path(self):
        return self._get_obj_variant_('self.entity.prd.plf_path')
    @property
    def tmp_plf_path(self):
        return self._get_obj_variant_('self.entity.tmp.plf_path')

    def get_vsn_all(self, dta_scm, stp_brh=None, stg_brh='prd'):
        vsn_all = []
        ett_brh = self.ENTITY_TYPE_NAME
        step_category = self.universe.get_obj_category(utl_prd_configure.ObjCategory.STEP)
        format_dict = self.get_format_dict()
        if stp_brh is not None:
            if isinstance(stp_brh, (str, unicode)):
                stp_brhs = [stp_brh]
            elif isinstance(stp_brh, (tuple, list)):
                stp_brhs = stp_brh
            else:
                raise TypeError()
        else:
            stp_brhs = step_category.get_variant('{}.{}.stp_brhs'.format(dta_scm, ett_brh))
        #
        use_mtp = step_category.get_variant(
            '{}.use_mtp'.format(dta_scm)
        ) or False
        use_cmp = step_category.get_variant(
            '{}.use_cmp'.format(dta_scm)
        ) or False
        use_mrg = step_category.get_variant(
            '{}.use_mrg'.format(dta_scm)
        ) or False
        for stp_brh in stp_brhs:
            vsn_format_dict = self._set_variant_inherit_(format_dict)
            step_type = self.universe.get_obj_type(stp_brh)
            dta_ctg = step_type.get_variant('{}.dta_ctg'.format(dta_scm))
            step_plf_path_format = step_type.get_variant('{}.{}.plf_path'.format(ett_brh, stg_brh))
            step_plf_path = self._set_variant_convert_(step_plf_path_format, vsn_format_dict)
            step_plf_name = step_type.get_variant('{}.plf_name'.format(ett_brh))
            vsn_format_dict['self.step.plf_name'] = step_plf_name
            #
            rlt_plf_file_path_key = 'product.{}.rlt_plf_file_path.{}.{}.vsn_dnm'.format(
                ett_brh, dta_ctg, dta_scm
            )
            rlt_plf_file_path_format = step_type.get_variant(
                rlt_plf_file_path_key
            )
            if rlt_plf_file_path_format is not None:
                rlt_plf_file_path = self._set_variant_convert_(rlt_plf_file_path_format, vsn_format_dict)
                #
                element_plf_file_path = '{}/{}'.format(step_plf_path, rlt_plf_file_path)
                results = self._get_match_plf_paths_(element_plf_file_path)
                if results:
                    for result in results:
                        p = parse.parse(
                            element_plf_file_path, result
                        )
                        if p:
                            extra = p.named
                            vsn_format_dict.update(extra)
                            #
                            vsn_raw, vsn_cmp_raw, vsn_mrg_raw = None, [], []
                            if use_mtp is True:
                                os_directory = utl_dcc_objects.OsDirectory_(result)
                                os_file_paths = os_directory.get_child_file_paths()
                                if os_file_paths:
                                    if len(os_file_paths) == 1:
                                        vsn_raw = os_file_paths[0]
                                    elif len(os_file_paths) > 1:
                                        os_multiply_file = utl_dcc_objects.OsMultiplyFile(os_file_paths[0])
                                        vsn_raw = os_multiply_file.set_file_path_convert_to_hou_seq()
                            elif use_cmp is True:
                                comp_rlt_plf_file_path_key = 'product.{}.rlt_plf_file_path.{}.{}.cmp'.format(
                                    ett_brh, dta_ctg, dta_scm
                                )
                                element_cmp_rlt_plf_file_path_format = step_type.get_variant(
                                    comp_rlt_plf_file_path_key
                                )
                                element_cmp_rlt_plf_file_path = self._set_variant_convert_(
                                    element_cmp_rlt_plf_file_path_format,
                                    vsn_format_dict
                                )
                                element_cmp_plf_file_path = '{}/{}'.format(result, element_cmp_rlt_plf_file_path)
                                cmp_results = self._get_match_plf_paths_(element_cmp_plf_file_path, trim=None)
                                if cmp_results:
                                    vsn_raw = result
                                    vsn_cmp_raw = cmp_results
                            elif use_mrg is True:
                                mrg_rlt_plf_file_path_key = 'product.{}.rlt_plf_file_path.{}.{}.vsn_dnm'.format(
                                    ett_brh, dta_ctg, dta_scm
                                )
                                element_mrg_rlt_plf_file_path_format = step_type.get_variant(
                                    mrg_rlt_plf_file_path_key
                                )
                                mrg_format_dict = self._set_variant_inherit_(vsn_format_dict)
                                mrg_format_dict['self.container.index'] = '*'
                                element_mrg_rlt_plf_file_path = self._set_variant_convert_(
                                    element_mrg_rlt_plf_file_path_format,
                                    mrg_format_dict
                                )
                                element_mrg_plf_file_path = '{}/{}'.format(step_plf_path, element_mrg_rlt_plf_file_path)
                                cmp_results = self._get_match_plf_paths_(element_mrg_plf_file_path)
                                if cmp_results:
                                    vsn_raw = result
                                    vsn_cmp_raw = cmp_results
                            else:
                                vsn_raw = result
                            #
                            if vsn_raw is not None:
                                vsn_name_format = step_type.get_variant('{}.vsn_key'.format(ett_brh))
                                vsn_key = self._set_variant_convert_(vsn_name_format, vsn_format_dict)
                                #
                                vsn_all.append(
                                    (vsn_key, vsn_raw, vsn_cmp_raw)
                                )

        return vsn_all

    def get_stp_plf_path(self, stp_brh, stg_brh='prd'):
        ett_brh = self.ENTITY_TYPE_NAME
        format_dict = self.get_format_dict()
        step_format_dict = self._set_variant_inherit_(format_dict)
        step_type = self.universe.get_obj_type(stp_brh)
        step_plf_path_format = step_type.get_variant('{}.{}.plf_path'.format(ett_brh, stg_brh))
        step_plf_path = self._set_variant_convert_(step_plf_path_format, step_format_dict)
        return step_plf_path


class AbsShotOpt(AbsEntityOpt):
    MANIFEST_OPT_CLASS = None
    def __init__(self, obj):
        super(AbsShotOpt, self).__init__(obj)
    @property
    def sequence(self):
        return self.obj.get_variant('self.sequence.plf_name')

    def set_manifests_build(self):
        shot_format_dict = self.get_format_dict()
        manifest_type = self.universe.get_obj_type(utl_prd_configure.ObjType.MANIFEST)
        manifest_schemes = manifest_type.get_variant('schemes') or []
        for manifest_dta_scm in manifest_schemes:
            manifest_format_dict = self._set_variant_inherit_(shot_format_dict)
            manifest_format_dict['self.manifest.scheme'] = manifest_dta_scm
            self._get_manifest_per_step_(
                manifest_type, manifest_dta_scm, manifest_format_dict
            )

    def _get_manifest_per_step_(self, manifest_type, manifest_dta_scm, manifest_format_dict):
        ett_brh = self.obj.type.name
        task_include = manifest_type.get_variant('{}.{}.task_include'.format(manifest_dta_scm, ett_brh)) or []
        task_exclude = manifest_type.get_variant('{}.{}.task_exclude'.format(manifest_dta_scm, ett_brh)) or []
        stage_type = self.universe.get_obj_type(utl_prd_configure.ObjType.PRODUCT)
        raws = []
        #
        stp_brhs = manifest_type.get_variant('{}.{}.stp_brhs'.format(manifest_dta_scm, ett_brh)) or []
        vsn_all = []
        for stp_brh in stp_brhs:
            vsn_format_dict = self._set_variant_inherit_(manifest_format_dict)
            # stage to product
            vsn_format_dict['self.stage.plf_name'] = stage_type.get_variant('plf_name')
            #
            step_type_path = obj_configure.ObjType.PATHSEP.join([utl_prd_configure.ObjCategory.STEP, stp_brh])
            step_type = self.universe.get_obj_type(step_type_path)
            dta_ctg = step_type.get_variant('{}.dta_ctg'.format(manifest_dta_scm))
            step_plf_name = step_type.get_variant('{}.plf_name'.format(ett_brh))
            vsn_format_dict['self.step.plf_name'] = step_plf_name
            step_plf_path_format = step_type.get_variant(
                '{}.plf_path'.format(ett_brh)
            )
            rlt_plf_file_path_format = step_type.get_variant(
                'product.{}.rlt_plf_file_path.{}.{}.vsn_dnm'.format(ett_brh, dta_ctg, manifest_dta_scm)
            )
            plf_file_path_format = '{}/{}'.format(
                step_plf_path_format, rlt_plf_file_path_format
            )
            plf_file_path = self._set_variant_convert_(
                plf_file_path_format, vsn_format_dict
            )
            results = self._get_match_plf_paths_(plf_file_path)
            # guess
            if not results:
                if manifest_dta_scm == 'anm_scm':
                    plf_file_path = plf_file_path.replace('.yml', '.guess.yml')
                    results = self._get_match_plf_paths_(plf_file_path)
            #
            if results:
                for result in results:
                    p = parse.parse(
                        plf_file_path, result
                    )
                    if p:
                        extra = p.named
                        vsn_format_dict.update(extra)
                        #
                        task_name = vsn_format_dict['self.task.plf_name']
                        if task_include:
                            if task_name not in task_include:
                                continue
                        if task_exclude:
                            if task_name in task_exclude:
                                continue
                        #
                        vsn_name_format = step_type.get_variant('{}.vsn_key'.format(ett_brh))
                        vsn_key = self._set_variant_convert_(vsn_name_format, vsn_format_dict)
                        #
                        vsn_all.append(
                            (vsn_key, result)
                        )
        #
        manifest_format_dict['self.manifest.vsn_all'] = vsn_all
        if vsn_all:
            vsn = vsn_all[-1]
            vsn_key, vsn_raw = vsn
            manifest_format_dict['self.manifest.vsn'] = vsn
            manifest_format_dict['self.manifest.vsn_lst'] = vsn
            #
            manifest_format_dict['self.manifest.vsn_key'] = vsn_key
            manifest_format_dict['self.manifest.vsn_key_lst'] = vsn_key
            manifest_format_dict['self.manifest.vsn_raw'] = vsn_raw
            manifest_format_dict['self.manifest.vsn_raw_lst'] = vsn_raw
            #
            obj = self._set_manifest_obj_create_(manifest_type, manifest_format_dict, manifest_dta_scm)
            raws.append(obj.path)
        #
        self.obj._set_port_build_('self.manifest.{}'.format(manifest_dta_scm), raws)

    def _set_manifest_obj_create_(self, manifest_type, manifest_format_dict, manifest_dta_scm):
        name, path = [
            self._set_main_variant_update_(
                manifest_type, manifest_format_dict,
                manifest_dta_scm, variant_key
            )
            for variant_key in ['name', 'path']
        ]
        #
        obj = manifest_type.set_obj_create(path)
        [obj._set_port_build_(k, v) for k, v in manifest_format_dict.items()]
        return obj

    def get_manifest_paths(self, scheme):
        key = 'self.manifest.{}'.format(scheme)
        return self._get_obj_variant_(key) or []

    def get_manifests(self, scheme):
        return [self.universe.get_obj(i) for i in self.get_manifest_paths(scheme)]

    def get_manifest_opts(self, scheme):
        return [self.MANIFEST_OPT_CLASS(i) for i in self.get_manifests(scheme)]

    def _get_anm_scm_manifest_paths_(self):
        return self._get_obj_variant_('self.manifest.anm_scm') or []

    def get_anm_scm_manifests(self):
        return [self.universe.get_obj(i) for i in self._get_anm_scm_manifest_paths_()]

    def _get_crd_scm_manifest_paths_(self):
        return self._get_obj_variant_('self.manifest.crd_scm') or []

    def get_crd_scm_manifests(self):
        return [self.universe.get_obj(i) for i in self._get_crd_scm_manifest_paths_()]

    def get_manifest_op(self, manifest_path):
        manifest = self.universe.get_obj(manifest_path)
        if manifest is not None:
            return self.MANIFEST_OPT_CLASS(manifest)


class AbsAssetQuery(AbsEntityOpt):
    def __init__(self, obj):
        super(AbsAssetQuery, self).__init__(obj)


class AbsManifestOpt(AbsObjOptDef):
    CONTAINER_OPT_CLASS = None
    def __init__(self, obj):
        self._set_obj_opt_def_init_(obj)
    @property
    def vsn_key(self):
        return self.get_variant('self.manifest.vsn_key')
    @property
    def vsn_raw(self):
        return self.get_variant('self.manifest.vsn_raw')
    @property
    def plf_file_path(self):
        return self.get_variant('self.manifest.vsn_raw')
    @utl_core._print_time_
    def set_containers_build(self, progress_bar=None):
        manifest = self.obj
        manifest_path = manifest.get_variant('self.path')
        manifest_dta_scm = manifest.get_variant('self.manifest.scheme')
        manifest_vsn = manifest.get_variant('self.manifest.vsn')
        if manifest_vsn:
            manifest_vsn_key, manifest_vsn_raw = manifest_vsn
            if manifest_vsn_raw:
                manifest_type = self.universe.get_obj_type(utl_prd_configure.ObjType.MANIFEST)
                container_type = self.universe.get_obj_type(utl_prd_configure.ObjType.CONTAINER)
                instance_type = self.universe.get_obj_type(utl_prd_configure.ObjType.INSTANCE)
                #
                origin_path_dict = self.universe.get_gui_attribute('origin_path')
                if origin_path_dict is None:
                    origin_path_dict = {}
                    self.universe.set_gui_attribute('origin_path', origin_path_dict)
                manifest_format_dict = self._get_obj_format_dict_(manifest)
                container_build_raws = []
                if manifest_dta_scm == 'anm_scm':
                    self._manifest_scheme_loader = scm_objects.FileScheme(manifest_vsn_raw)
                    container_build_raws = self._get_variant_raws_by_scd_yml_(
                        manifest_type, container_type,
                        manifest_vsn_raw, manifest_dta_scm
                    )
                elif manifest_dta_scm == 'asb_scm':
                    self._manifest_scheme_loader = scm_objects.FileScheme(manifest_vsn_raw)
                    container_build_raws = self._get_variant_raws_by_scd_yml_(
                        manifest_type, container_type,
                        manifest_vsn_raw, manifest_dta_scm
                    )
                elif manifest_dta_scm == 'crd_scm':
                    container_build_raws = self._get_variant_raws_by_crd_scm_(
                        manifest_type, container_type,
                        manifest_vsn_raw, manifest_dta_scm, manifest_format_dict
                    )
                elif manifest_dta_scm == 'efx_scm':
                    container_build_raws = self._get_variant_raws_by_efx_scm_(
                        manifest_type, container_type,
                        manifest_vsn_raw, manifest_dta_scm, manifest_format_dict
                    )
                #
                if container_build_raws:
                    #
                    if progress_bar is not None:
                        p = progress_bar.set_progress_create(len(container_build_raws))
                    else:
                        p = None
                    #
                    for container_build_raw in container_build_raws:
                        if p is not None:
                            p.set_update()
                        #
                        container_format_dict = self._set_variant_inherit_(manifest_format_dict)
                        container_format_dict.update(container_build_raw)
                        #
                        container_format_dict['self.container.manifest'] = manifest_path
                        #
                        container_scheme = container_format_dict['self.container.scheme']
                        self._get_container_per_var_(
                            container_type, instance_type,
                            manifest_vsn,
                            container_scheme, container_format_dict, origin_path_dict
                        )
                    if p is not None:
                        p.set_stop()

    def get_container_opts(self):
        lis = []
        container_type = self.universe.get_obj_type(utl_prd_configure.ObjType.CONTAINER)
        vsn_key, vsn_raw = self.vsn_key, self.vsn_raw
        containers = container_type.get_objs()
        if containers:
            for container in containers:
                container_opt = self.CONTAINER_OPT_CLASS(container)
                vsn_keys, vsn_raws = container_opt.manifest_vsn_keys, container_opt.manifest_vsn_raws
                if vsn_key in vsn_keys and vsn_raw in vsn_raws:
                    lis.append(container_opt)
        return lis
    #
    def _get_asset_role_(self, container_namespace, format_dict):
        asset_format_dict = self._set_variant_inherit_(format_dict)
        asset_name = str(container_namespace).rstrip(string.digits)
        asset_format_dict['self.asset.plf_name'] = asset_name
        asset_type = self.universe.get_obj_type(utl_prd_configure.ObjType.ASSET)
        plf_path_format = asset_type.get_variant('plf_path')
        plf_path = self._set_variant_convert_(plf_path_format, asset_format_dict)
        results = self._get_match_plf_paths_(
            plf_path
        )
        if results:
            result = results[0]
            p = parse.parse(plf_path, result)
            if p:
                return p.named['self.role.plf_name']
    # noinspection PyMethodMayBeStatic
    @utl_core._print_time_
    def _get_variant_raws_by_scd_yml_(self, manifest_type, container_type, manifest_plf_file_path, manifest_dta_scm):
        lis = []
        #
        container_ist_raw_dict = {}
        manifest_scheme_loader = scm_objects.FileScheme(manifest_plf_file_path)
        container_schemes = manifest_type.get_variant('{}.container.schemes'.format(manifest_dta_scm)) or []
        for container_scheme in container_schemes:
            role_include = manifest_type.get_variant('container.{}.role_include'.format(container_scheme)) or []
            search_key_path_format = manifest_type.get_variant('container.{}.scheme_key'.format(container_scheme))
            if search_key_path_format is None:
                continue
            search_key_path_pattern = utl_prd_core._var__get_glob_pattern_(search_key_path_format).replace('/', '.')
            search_key_paths = manifest_scheme_loader.get_keys(regex=search_key_path_pattern)
            for search_key_path in search_key_paths:
                value = manifest_scheme_loader.get(search_key_path)
                p = parse.parse(
                    search_key_path_format, search_key_path.replace('.', '/')
                )
                if p:
                    format_dict = {}
                    extra = p.named
                    format_dict.update(extra)
                    #
                    container_role_name = format_dict['self.container.role']
                    if role_include:
                        if container_role_name not in role_include:
                            continue
                    #
                    format_dict['self.container.value'] = value
                    #
                    container_namespace = format_dict['self.container.namespace']
                    container_asset_name = format_dict['self.container.asset_name']
                    #
                    container_ist = container_namespace, value
                    if container_asset_name in container_ist_raw_dict:
                        container_ist_raw_list = container_ist_raw_dict[container_asset_name]
                    else:
                        container_ist_raw_list = []
                        container_ist_raw_dict[container_asset_name] = container_ist_raw_list
                    #
                    if container_ist not in container_ist_raw_list:
                        container_ist_raw_list.append(container_ist)
                    #
                    format_dict['self.container.ist_raw'] = container_ist_raw_list
                    #
                    format_dict['self.container.role_tag'] = container_role_name
                    #
                    format_dict['self.role.plf_name'] = container_role_name
                    format_dict['self.asset.plf_name'] = container_asset_name
                    #
                    format_dict['self.container.scheme'] = container_scheme
                    #
                    lis.append(format_dict)
        return lis
    @utl_core._print_time_
    def _get_variant_raws_by_cfx_har_scm_(self, manifest_type, container_type, manifest_plf_file_path, manifest_dta_scm, manifest_format_dict):
        lis = []
        container_schemes = manifest_type.get_variant('{}.container.schemes'.format(manifest_dta_scm)) or []
        for container_scheme in container_schemes:
            container_data_schemes = container_type.get_variant('{}.data_schemes'.format(container_scheme)) or []
            for container_data_scheme in container_data_schemes:
                rlt_plf_file_name_format = manifest_type.get_variant(
                    'container.{}.{}.rlt_plf_file_name'.format(container_scheme, container_data_scheme)
                )
                if rlt_plf_file_name_format is None:
                    continue
                container_plf_file_name = self._set_variant_convert_(rlt_plf_file_name_format, manifest_format_dict)
                container_plf_file_path = '{}/{}'.format(manifest_plf_file_path, container_plf_file_name)
                results = self._get_match_plf_paths_(container_plf_file_path, trim=None)
                if results:
                    use_mtp = container_type.get_variant(
                        '{}.{}.use_mtp'.format(container_scheme, container_data_scheme)
                    ) or False
                    for result in results:
                        if use_mtp is True:
                            os_dir = utl_dcc_objects.OsDirectory_(result)
                            if os_dir.get_child_file_paths():
                                enable = True
                            else:
                                enable = False
                        else:
                            enable = True
                        if enable is True:
                            p = parse.parse(
                                container_plf_file_path, result
                            )
                            if p:
                                format_dict = {}
                                extra = p.named
                                format_dict.update(extra)
                                #
                                format_dict['self.container.scheme'] = container_scheme
                                container_namespace = format_dict['self.container.namespace']
                                role = self._get_asset_role_(container_namespace, manifest_format_dict)
                                #
                                format_dict['self.container.role_tag'] = role
                                #
                                lis.append(format_dict)
        return lis
    @utl_core._print_time_
    def _get_variant_raws_by_crd_scm_(self, manifest_type, container_type, manifest_plf_file_path, manifest_dta_scm, manifest_format_dict):
        lis = []
        #
        container_indices_dict = {}
        role_tag = container_type.universe.get_obj_type(utl_prd_configure.ObjType.CRD).get_variant('plf_name')
        container_schemes = manifest_type.get_variant('{}.container.schemes'.format(manifest_dta_scm)) or []
        for container_scheme in container_schemes:
            container_data_schemes = container_type.get_variant('{}.data_schemes'.format(container_scheme)) or []
            for container_data_scheme in container_data_schemes:
                rlt_plf_file_name_format = manifest_type.get_variant(
                    'container.{}.{}.rlt_plf_file_name'.format(container_scheme, container_data_scheme)
                )
                #
                if rlt_plf_file_name_format is None:
                    continue
                #
                container_plf_file_name = self._set_variant_convert_(rlt_plf_file_name_format, manifest_format_dict)
                container_plf_file_path = '{}/{}'.format(manifest_plf_file_path, container_plf_file_name)
                results = self._get_match_plf_paths_(container_plf_file_path, trim=None)
                for result in results:
                    p = parse.parse(
                        container_plf_file_path, result
                    )
                    if p:
                        format_dict = {}
                        extra = p.named
                        format_dict.update(extra)
                        #
                        format_dict['self.container.scheme'] = container_scheme
                        format_dict['self.container.role_tag'] = role_tag
                        #
                        container_asset_name = format_dict['self.container.asset_name']
                        container_index = format_dict['self.container.index']
                        if container_asset_name in container_indices_dict:
                            container_indices = container_indices_dict[container_asset_name]
                        else:
                            container_indices = []
                            container_indices_dict[container_asset_name] = container_indices
                        #
                        if container_index not in container_indices:
                            container_indices.append(container_index)
                        #
                        format_dict['self.container.idx_all'] = container_indices
                        #
                        format_dict['self.asset.plf_name'] = container_asset_name
                        container_indices_dict.setdefault(container_asset_name, []).append(container_index)
                        #
                        container_namespace_format = container_type.get_variant('format.{}.namespace'.format(container_scheme))
                        container_namespace = self._set_variant_convert_(container_namespace_format, format_dict)
                        #
                        role = self._get_asset_role_(container_namespace, manifest_format_dict)
                        #
                        format_dict['self.container.role'] = role
                        format_dict['self.container.namespace'] = container_namespace
                        #
                        lis.append(format_dict)
        return lis
    @utl_core._print_time_
    def _get_variant_raws_by_efx_scm_(self, manifest_type, container_type, manifest_plf_file_path, manifest_dta_scm, manifest_format_dict):
        lis = []
        role_tag = container_type.universe.get_obj_type(utl_prd_configure.ObjType.EFX).get_variant('plf_name')
        container_schemes = manifest_type.get_variant('{}.container.schemes'.format(manifest_dta_scm)) or []
        for container_scheme in container_schemes:
            container_data_schemes = container_type.get_variant('{}.data_schemes'.format(container_scheme)) or []
            for container_data_scheme in container_data_schemes:
                rlt_plf_file_name_format = manifest_type.get_variant(
                    'container.{}.{}.rlt_plf_file_name'.format(container_scheme, container_data_scheme)
                )
                if rlt_plf_file_name_format is None:
                    continue
                container_plf_file_name = self._set_variant_convert_(rlt_plf_file_name_format, manifest_format_dict)
                container_plf_file_path = '{}/{}'.format(manifest_plf_file_path, container_plf_file_name)
                results = self._get_match_plf_paths_(container_plf_file_path, trim=None)
                if results:
                    use_mtp = container_type.get_variant(
                        '{}.{}.use_mtp'.format(container_scheme, container_data_scheme)
                    ) or False
                    for result in results:
                        if use_mtp is True:
                            os_dir = utl_dcc_objects.OsDirectory_(result)
                            if os_dir.get_child_file_paths():
                                enable = True
                            else:
                                enable = False
                        else:
                            enable = True
                        if enable is True:
                            p = parse.parse(
                                container_plf_file_path, result
                            )
                            if p:
                                format_dict = {}
                                extra = p.named
                                format_dict.update(extra)
                                # filter crowd
                                container_namespace = format_dict['self.container.namespace']
                                if container_namespace == 'crowd':
                                    continue
                                format_dict['self.container.scheme'] = container_scheme
                                format_dict['self.container.role_tag'] = role_tag
                                #
                                lis.append(format_dict)
        return lis

    def _get_container_per_var_(self, container_type, instance_type, manifest_vsn, container_scheme, container_format_dict, origin_path_dict):
        container_data_schemes = container_type.get_variant('{}.data_schemes'.format(container_scheme)) or []
        for container_data_scheme in container_data_schemes:
            # use instance
            use_ist = container_type.get_variant(
                '{}.{}.use_ist'.format(container_scheme, container_data_scheme)
            ) or False
            container_format_dict['self.container.use_ist'] = use_ist
            # use compose
            use_cmp = container_type.get_variant(
                '{}.{}.use_cmp'.format(container_scheme, container_data_scheme)
            ) or False
            container_format_dict['self.container.use_cmp'] = use_cmp
            # use multiply
            use_mtp = container_type.get_variant(
                '{}.{}.use_mtp'.format(container_scheme, container_data_scheme)
            ) or False
            container_format_dict['self.container.use_mtp'] = use_mtp
            # use merge
            use_mrg = container_type.get_variant(
                '{}.{}.use_mrg'.format(container_scheme, container_data_scheme)
            ) or False
            container_format_dict['self.container.use_mrg'] = use_mrg
            #
            container_format_dict['self.container.data_scheme'] = container_data_scheme
            #
            container_variants = container_type.get_variant('{}.{}.variants'.format(container_scheme, container_data_scheme)) or []
            ett_brhs = container_type.get_variant('element.{}.{}.ett_brhs'.format(container_scheme, container_data_scheme)) or []
            container_format_dict['self.container.ett_brhs'] = ett_brhs
            for container_variant in container_variants:
                container_format_dict['self.container.variant'] = container_variant
                #
                container_path, container_is_create = self._set_container_create_(
                    container_type, instance_type,
                    container_scheme, container_data_scheme,
                    manifest_vsn, container_format_dict
                )
                for ett_brh in ett_brhs:
                    # orig container
                    if container_is_create is True:
                        element_format_dict = self._set_variant_inherit_(container_format_dict)
                        #
                        container_origin_path_format = container_type.get_variant(
                            '{}.org_path'.format(ett_brh)
                        )
                        # get is exists
                        container_origin_path = self._set_variant_convert_(container_origin_path_format, container_format_dict)
                        if container_origin_path not in origin_path_dict:
                            origin_path_dict[container_origin_path] = container_path
                        #
                        element_format_dict['self.element.entity_branch'] = ett_brh
                        self._get_element_per_step_(
                            container_type,
                            container_scheme, container_data_scheme,
                            ett_brh,
                            element_format_dict
                        )

    def _set_container_create_(self, container_type, instance_type, container_scheme, container_data_scheme, manifest_vsn, container_format_dict):
        scheme_path = '{}.{}'.format(container_scheme, container_data_scheme)
        name, path = [
            self._set_main_variant_update_(
                container_type, container_format_dict,
                scheme_path, variant_key
            )
            for variant_key in ['name', 'path']
        ]
        if path is not None:
            manifest_vsn_key, manifest_vsn_raw = manifest_vsn
            #
            use_ist = container_format_dict['self.container.use_ist']
            use_mrg = container_format_dict['self.container.use_mrg']
            #
            ist_name, ist_path = [
                self._set_main_variant_update_(
                    container_type, container_format_dict,
                    scheme_path, variant_key
                )
                for variant_key in ['ist.name', 'ist.path']
            ]
            mrg_name, mrg_path = [
                self._set_main_variant_update_(
                    container_type, container_format_dict,
                    scheme_path, variant_key
                )
                for variant_key in ['mrg.name', 'mrg.path']
            ]
            if use_mrg is True:
                name, path = mrg_name, mrg_path
            if use_ist is True:
                name, path = ist_name, ist_path
            #
            application_name = container_format_dict['self.application.name']
            #
            hou_opt_dcc_path = container_type.get_variant(
                '{}.{}.hou_opt.dcc_path'.format(container_data_scheme, application_name)
            )
            container_format_dict['self.container.hou_opt.dcc_path'] = hou_opt_dcc_path
            exists_obj = self.universe.get_obj(path)
            if exists_obj:
                is_create = False
                #
                manifest_vsn_keys = exists_obj.get_variant('self.container.manifest.vsn_keys')
                if manifest_vsn_key not in manifest_vsn_keys:
                    manifest_vsn_keys.append(manifest_vsn_key)
                manifest_vsn_raws = exists_obj.get_variant('self.container.manifest.vsn_raws')
                if manifest_vsn_raw not in manifest_vsn_raws:
                    manifest_vsn_raws.append(manifest_vsn_raw)
            else:
                container_format_dict['self.container.manifest.vsn_keys'] = [manifest_vsn_key]
                container_format_dict['self.container.manifest.vsn_raws'] = [manifest_vsn_raw]
                #
                for variant_key in ['use_ign']:
                    self._set_main_variant_update_(
                        container_type, container_format_dict,
                        container_data_scheme,
                        variant_key
                    )
                # dcc
                for sub_key in ['entities', 'role', 'namespace', 'role_tag']:
                    for variant_key in ['{}.dcc_type'.format(sub_key), '{}.dcc_name'.format(sub_key), '{}.dcc_path'.format(sub_key)]:
                        self._set_dcc_main_variant_update_(
                            container_type, container_format_dict,
                            variant_key
                        )
                #
                for variant_key in [
                    'use_brh',
                    'dcc_type', 'dcc_name', 'dcc_path', 'dcc_port'
                ]:
                    self._set_dcc_scheme_variant_update_(
                        container_type, container_format_dict,
                        container_data_scheme,
                        variant_key
                    )
                #
                for i in ['ist', 'cmp', 'ist_cmp', 'mrg']:
                    for variant_key in [
                        '{}.dcc_type'.format(i), '{}.dcc_name'.format(i), '{}.dcc_path'.format(i), '{}.dcc_port'.format(i)
                    ]:
                        self._set_dcc_scheme_variant_update_(
                            container_type, container_format_dict,
                            container_data_scheme,
                            variant_key
                        )
                #
                obj = container_type.set_obj_create(path)
                [obj._set_port_build_(k, v) for k, v in container_format_dict.items()]
                #
                is_create = True
        else:
            is_create, ist_is_create = None, None
            utl_core.Log.set_warning_trace(
                'obj-type: "{}", container-scheme: "{}", element-scheme: "{}" path is Non-configure'.format(
                    container_type.path,
                    container_scheme,
                    container_data_scheme
                )

            )
        return path, is_create

    def _get_element_per_step_(self, container_type, container_scheme, container_data_scheme, ett_brh, element_format_dict):
        use_ist = element_format_dict['self.container.use_ist']
        element_format_dict['self.element.use_ist'] = use_ist
        #
        use_mtp = element_format_dict['self.container.use_mtp']
        use_cmp = element_format_dict['self.container.use_cmp']
        #
        use_mrg = element_format_dict['self.container.use_mrg']
        element_format_dict['self.element.use_mrg'] = use_mrg
        #
        element_steps = container_type.get_variant(
            'element.{}.{}.{}.stp_brhs'.format(container_scheme, container_data_scheme, ett_brh)
        ) or []
        #
        element_type = self.universe.get_obj_type(utl_prd_configure.ObjType.ELEMENT)
        #
        vsn_all = []
        for element_step in element_steps:
            vsn_format_dict = self._set_variant_inherit_(element_format_dict)
            stage_type = self.universe.get_obj_type(utl_prd_configure.ObjType.PRODUCT)
            vsn_format_dict['self.stage.plf_name'] = stage_type.get_variant('plf_name')
            #
            step_type_path = obj_configure.ObjType.PATHSEP.join([utl_prd_configure.ObjCategory.STEP, element_step])
            step_type = self.universe.get_obj_type(step_type_path)
            dta_ctg = step_type.get_variant('{}.dta_ctg'.format(container_data_scheme))
            step_plf_path_format = step_type.get_variant('{}.plf_path'.format(ett_brh))
            step_plf_path = self._set_variant_convert_(step_plf_path_format, vsn_format_dict)
            step_plf_name = step_type.get_variant('{}.plf_name'.format(ett_brh))
            vsn_format_dict['self.step.plf_name'] = step_plf_name
            #
            rlt_plf_file_path_key = 'product.{}.rlt_plf_file_path.{}.{}.vsn_dnm'.format(
                ett_brh, dta_ctg, container_data_scheme
            )
            element_rlt_plf_file_path_format = step_type.get_variant(
                rlt_plf_file_path_key
            )
            if element_rlt_plf_file_path_format is not None:
                element_rlt_plf_file_path = self._set_variant_convert_(element_rlt_plf_file_path_format, vsn_format_dict)
                #
                element_plf_file_path = '{}/{}'.format(step_plf_path, element_rlt_plf_file_path)
                results = self._get_match_plf_paths_(element_plf_file_path)
                if results:
                    for result in results:
                        p = parse.parse(
                            element_plf_file_path, result
                        )
                        if p:
                            extra = p.named
                            vsn_format_dict.update(extra)
                            #
                            vsn_raw, vsn_cmp_raw, vsn_mrg_raw = None, [], []
                            if use_mtp is True:
                                os_directory = utl_dcc_objects.OsDirectory_(result)
                                os_file_paths = os_directory.get_child_file_paths()
                                if os_file_paths:
                                    if len(os_file_paths) == 1:
                                        vsn_raw = os_file_paths[0]
                                    elif len(os_file_paths) > 1:
                                        os_multiply_file = utl_dcc_objects.OsMultiplyFile(os_file_paths[0])
                                        vsn_raw = os_multiply_file.set_file_path_convert_to_hou_seq()
                            elif use_cmp is True:
                                comp_rlt_plf_file_path_key = 'product.{}.rlt_plf_file_path.{}.{}.cmp'.format(
                                    ett_brh, dta_ctg, container_data_scheme
                                )
                                element_cmp_rlt_plf_file_path_format = step_type.get_variant(
                                    comp_rlt_plf_file_path_key
                                )
                                element_cmp_rlt_plf_file_path = self._set_variant_convert_(
                                    element_cmp_rlt_plf_file_path_format,
                                    vsn_format_dict
                                )
                                element_cmp_plf_file_path = '{}/{}'.format(result, element_cmp_rlt_plf_file_path)
                                cmp_results = self._get_match_plf_paths_(element_cmp_plf_file_path, trim=None)
                                if cmp_results:
                                    vsn_raw = result
                                    vsn_cmp_raw = cmp_results
                            elif use_mrg is True:
                                mrg_rlt_plf_file_path_key = 'product.{}.rlt_plf_file_path.{}.{}.vsn_dnm'.format(
                                    ett_brh, dta_ctg, container_data_scheme
                                )
                                element_mrg_rlt_plf_file_path_format = step_type.get_variant(
                                    mrg_rlt_plf_file_path_key
                                )
                                mrg_format_dict = self._set_variant_inherit_(vsn_format_dict)
                                mrg_format_dict['self.container.index'] = '*'
                                element_mrg_rlt_plf_file_path = self._set_variant_convert_(
                                    element_mrg_rlt_plf_file_path_format,
                                    mrg_format_dict
                                )
                                element_mrg_plf_file_path = '{}/{}'.format(step_plf_path, element_mrg_rlt_plf_file_path)
                                cmp_results = self._get_match_plf_paths_(element_mrg_plf_file_path)
                                if cmp_results:
                                    vsn_raw = result
                                    vsn_cmp_raw = cmp_results
                            else:
                                vsn_raw = result
                            #
                            if vsn_raw is not None:
                                vsn_name_format = step_type.get_variant('{}.vsn_key'.format(ett_brh))
                                vsn_key = self._set_variant_convert_(vsn_name_format, vsn_format_dict)
                                #
                                vsn_all.append(
                                    (vsn_key, vsn_raw, vsn_cmp_raw)
                                )
        #
        if vsn_all:
            vsn_format_dict = {}
            #
            vsn = vsn_all[-1]
            #
            vsn_key, vsn_raw, vsn_cmp_raw = vsn
            vsn_format_dict['self.element.vsn_all'] = vsn_all
            #
            vsn_format_dict['self.element.vsn'] = vsn
            vsn_format_dict['self.element.vsn_lst'] = vsn
            #
            vsn_format_dict['self.element.vsn_key'] = vsn_key
            vsn_format_dict['self.element.vsn_key_lst'] = vsn_key
            vsn_format_dict['self.element.vsn_raw'] = vsn_raw
            vsn_format_dict['self.element.vsn_raw_lst'] = vsn_raw
            #
            vsn_format_dict['self.element.vsn_cmp_raw'] = vsn_cmp_raw
            vsn_format_dict['self.element.vsn_cmp_raw_lst'] = vsn_cmp_raw
            #
            element_format_dict.update(vsn_format_dict)
            #
            element_obj, element_is_create = self._set_element_obj_create_(
                element_type,
                container_data_scheme, ett_brh,
                element_format_dict
            )
            if element_is_create is False:
                [element_obj._set_port_build_(k, v) for k, v in vsn_format_dict.items()]

    def _set_element_obj_create_(self, element_type, container_data_scheme, ett_brh, element_format_dict):
        #
        scheme_path = container_data_scheme
        name, path = [
            self._set_main_variant_update_(
                element_type, element_format_dict,
                scheme_path, variant_key
            )
            for variant_key in ['name', 'path']
        ]
        #
        if path is not None:
            use_mrg = element_format_dict['self.container.use_mrg']
            use_ist = element_format_dict['self.container.use_ist']
            #
            ist_name, ist_path = [
                self._set_main_variant_update_(
                    element_type, element_format_dict,
                    scheme_path, variant_key
                )
                for variant_key in ['ist.name', 'ist.path']
            ]
            mrg_name, mrg_path = [
                self._set_main_variant_update_(
                    element_type, element_format_dict,
                    scheme_path, variant_key
                )
                for variant_key in ['mrg.name', 'mrg.path']
            ]
            #
            if use_mrg is True:
                name, path = mrg_name, mrg_path
            if use_ist is True:
                name, path = ist_name, ist_path
            #
            exists_obj = self.universe.get_obj(path)
            if exists_obj is not None:
                is_create = False
            else:
                is_create = True
                #
                for variant_key in [
                    'use_brh',
                    'dcc_type', 'dcc_name', 'dcc_path',
                    'dcc_namespace',
                    'dcc_port', '{}.dcc_port'.format(ett_brh)
                ]:
                    self._set_dcc_scheme_variant_update_(
                        element_type, element_format_dict,
                        container_data_scheme,
                        variant_key
                    )
                #
                for i in ['ist', 'ist_cmp', 'cmp', 'mrg', 'mrg_cmp']:
                    for variant_key in [
                        '{}.dcc_type'.format(i), '{}.dcc_name'.format(i), '{}.dcc_path'.format(i),
                        '{}.dcc_port'.format(i), '{}.{}.dcc_port'.format(ett_brh, i)
                    ]:
                        self._set_dcc_scheme_variant_update_(
                            element_type, element_format_dict,
                            container_data_scheme, variant_key
                        )
                #
                obj = element_type.set_obj_create(path)
                [obj._set_port_build_(k, v) for k, v in element_format_dict.items()]
        else:
            exists_obj, is_create, ist_is_create = None, None, None
            #
            utl_core.Log.set_warning_trace(
                'obj-type: "{}" element-scheme: "{}" path is Non-configure'.format(
                    element_type.path,
                    container_data_scheme
                )
            )
        return exists_obj, is_create

    def _set_ist_obj_create_(self, obj_type, instance_type, obj_format_dict):
        ist_path = obj_format_dict['self.{}.ist.path'.format(obj_type.name)]
        if ist_path is not None:
            exists_obj = self.universe.get_obj(ist_path)
            if exists_obj is None:
                is_create = True
                obj = instance_type.set_obj_create(ist_path)
                [obj._set_port_build_(k, v) for k, v in obj_format_dict.items()]
            else:
                is_create = False
        else:
            is_create = None
        return is_create


class AbsIstDef(AbsObjOptDef):
    IST_OPT_CLASS = None
    def _set_ist_def_init_(self, ist_key):
        self._ist_key = ist_key
        self._dcc_use_ist = False
    @property
    def use_ist(self):
        return self.get_variant('self.{}.use_ist'.format(self._ist_key))
    @property
    def ist(self):
        path = self.get_variant('self.{}.ist.path'.format(self._ist_key))
        if path:
            return self.universe.get_obj(path)
    #
    def get_ist_opt(self):
        instance = self.ist
        if instance is not None:
            obj_opt = self.IST_OPT_CLASS(instance)
            obj_opt._key = self._obj.type.name
            return obj_opt
    @property
    def dcc_type(self):
        return self._get_obj_variant_('self.{}.dcc_type'.format(self._ist_key))
    @property
    def dcc_name(self):
        return self._get_obj_variant_('self.{}.dcc_name'.format(self._ist_key))
    @property
    def dcc_path(self):
        return self._get_obj_variant_('self.{}.dcc_path'.format(self._ist_key))


class AbsIstOpt(AbsObjOptDef):
    def __init__(self, obj):
        self._set_obj_opt_def_init_(obj)
        self._key = None
    @property
    def dcc_type(self):
        return self._get_obj_variant_('self.{}.ist.dcc_type'.format(self._key))
    @property
    def dcc_name(self):
        return self._get_obj_variant_('self.{}.ist.dcc_name'.format(self._key))
    @property
    def dcc_path(self):
        return self._get_obj_variant_('self.{}.ist.dcc_path'.format(self._key))


class AbsContainerOpt(AbsIstDef):
    ELEMENT_OPT_CLASS = None
    IST_OPT_CLASS = None
    def __init__(self, obj):
        self._set_obj_opt_def_init_(obj)
        self._set_ist_def_init_(obj.type.name)
    @property
    def manifest(self):
        path = self._get_obj_variant_('self.container.manifest')
        return self.universe.get_obj(path)
    @property
    def manifest_vsn_keys(self):
        return self._get_obj_variant_('self.container.manifest.vsn_keys') or []
    @property
    def manifest_vsn_raws(self):
        return self._get_obj_variant_('self.container.manifest.vsn_raws') or []
    @property
    def scheme(self):
        return self._get_obj_variant_('self.container.scheme')
    #
    def get_scheme_is_sot_cmr(self):
        return self.scheme == 'sot_cmr'

    def get_scheme_is_sot_anm(self):
        return self.scheme == 'sot_anm'

    def get_scheme_is_sot_abs(self):
        return self.scheme == 'sot_asb'

    def get_scheme_is_sot_har(self):
        return self.scheme == 'sot_har'

    def get_scheme_is_sot_asb(self):
        return self.scheme == 'sot_asb'

    def get_scheme_is_sot_crd(self):
        return self.scheme == 'sot_crd'

    def get_scheme_is_sot_efx(self):
        return self.scheme == 'sot_efx'
    # entities
    @property
    def entities(self):
        return self._get_obj_variant_('self.container.role')
    @property
    def entities_dcc_type(self):
        return self._get_obj_variant_('self.container.entities.dcc_type')
    @property
    def entities_dcc_name(self):
        return self._get_obj_variant_('self.container.entities.dcc_name')
    @property
    def entities_dcc_path(self):
        return self._get_obj_variant_('self.container.entities.dcc_path')
    # role
    @property
    def role(self):
        return self._get_obj_variant_('self.container.role')
    @property
    def role_dcc_type(self):
        return self._get_obj_variant_('self.container.role.dcc_type')
    @property
    def role_dcc_name(self):
        return self._get_obj_variant_('self.container.role.dcc_name')
    @property
    def role_dcc_path(self):
        return self._get_obj_variant_('self.container.role.dcc_path')
    # namespace
    @property
    def asset_name(self):
        return self._get_obj_variant_('self.container.asset_name')
    @property
    def namespace(self):
        return self._get_obj_variant_('self.container.namespace')
    @property
    def namespace_dcc_type(self):
        return self._get_obj_variant_('self.container.namespace.dcc_type')
    @property
    def namespace_dcc_name(self):
        return self._get_obj_variant_('self.container.namespace.dcc_name')
    @property
    def namespace_dcc_path(self):
        return self._get_obj_variant_('self.container.namespace.dcc_path')
    @property
    def role_tag_dcc_type(self):
        return self._get_obj_variant_('self.container.role_tag.dcc_type')
    @property
    def role_tag_dcc_name(self):
        return self._get_obj_variant_('self.container.role_tag.dcc_name')
    @property
    def role_tag_dcc_path(self):
        return self._get_obj_variant_('self.container.role_tag.dcc_path')
    @property
    def hou_opt_dcc_path(self):
        return self._get_obj_variant_('self.container.hou_opt.dcc_path')
    #
    @property
    def use_ign(self):
        return self._get_obj_variant_('self.container.use_ign') or False
    #
    @property
    def dcc_type(self):
        if self.use_mrg is True:
            return self.mrg_dcc_type
        elif self.use_ist is True:
            return self.ist_dcc_type
        return self._get_obj_variant_('self.container.dcc_type')
    @property
    def dcc_name(self):
        if self.use_mrg is True:
            return self.mrg_dcc_name
        elif self.use_ist is True:
            return self.ist_dcc_name
        return self._get_obj_variant_('self.container.dcc_name')
    @property
    def dcc_path(self):
        if self.use_mrg is True:
            return self.mrg_dcc_path
        elif self.use_ist is True:
            return self.ist_dcc_path
        return self._get_obj_variant_('self.container.dcc_path')
    # instance
    @property
    def use_ist(self):
        return self.obj.get_variant('self.container.use_ist') or False
    @property
    def ist_raw(self):
        return self.obj.get_variant('self.container.ist_raw') or False
    #
    @property
    def ist_dcc_type(self):
        return self.obj.get_variant('self.container.ist.dcc_type')
    @property
    def ist_dcc_name(self):
        return self.obj.get_variant('self.container.ist.dcc_name')
    @property
    def ist_dcc_path(self):
        return self.obj.get_variant('self.container.ist.dcc_path')
    @property
    def ist_cmp_dcc_type(self):
        return self.obj.get_variant('self.container.ist_cmp.dcc_type')
    @property
    def ist_cmp_dcc_name(self):
        return self.obj.get_variant('self.container.ist_cmp.dcc_name')
    @property
    def ist_cmp_dcc_path(self):
        return self.obj.get_variant('self.container.ist_cmp.dcc_path')
    @property
    def ist_cmp_dcc_port_name(self):
        return self.obj.get_variant('self.container.ist_cmp.dcc_port')
    #
    @property
    def use_mrg(self):
        return self.obj.get_variant('self.container.use_mrg') or False
    # merge
    @property
    def mrg_dcc_type(self):
        return self.obj.get_variant('self.container.mrg.dcc_type')
    @property
    def mrg_dcc_name(self):
        return self.obj.get_variant('self.container.mrg.dcc_name')
    @property
    def mrg_dcc_path(self):
        return self.obj.get_variant('self.container.mrg.dcc_path')
    #
    @property
    def variant(self):
        return self._get_obj_variant_('self.container.variant')
    @property
    def data_scheme(self):
        return self._get_obj_variant_('self.container.data_scheme')
    @property
    def role_tag(self):
        return self.get_variant('self.container.role_tag')
    @property
    def data_tag(self):
        return self.get_variant('self.container.data_tag')
    @property
    def value(self):
        return self.obj.get_variant('self.container.value')
    #
    def get_data_scheme_is_cmr_abc(self):
        return self.data_scheme == 'cmr_abc'

    def get_data_scheme_is_mtl_mtx(self):
        return self.data_scheme == 'mtl_mtx'

    def get_data_scheme_is_gmt_abc(self):
        return self.data_scheme == 'gmt_abc'

    def get_data_scheme_is_plt_dta(self):
        return self.data_scheme == 'plt_dta'

    def get_data_scheme_is_har_xgn(self):
        return self.data_scheme == 'har_xgn'

    def get_data_scheme_is_xgn_glo_abc(self):
        return self.data_scheme == 'xgn_glo_abc'

    def get_data_scheme_is_crd_abc(self):
        return self.data_scheme == 'crd_abc'

    def get_data_scheme_is_hou_dta(self):
        return self.data_scheme == 'hou_dta'

    def get_element_entity_branches(self):
        return self.get_variant('self.container.ett_brhs')
    #
    def get_elements(self, ett_brh=None):
        lis = []
        children = self.obj.get_children()
        for child in children:
            if ett_brh is not None:
                if child.get_variant('self.element.entity_branch') != ett_brh:
                    continue
            lis.append(child)
        return lis

    def get_element_opts(self, ett_brh=None):
        lis = []
        elements = self.get_elements(ett_brh)
        for element in elements:
            element_opt = self.ELEMENT_OPT_CLASS(element)
            lis.append(element_opt)
        return lis
    #
    def get_mtl_mtx_dcc_path(self):
        parent_path = self.obj.get_parent_path()
        if parent_path:
            pathsep = self.obj.pathsep
            mtl_mtx_container_path = '{}{}{}'.format(parent_path,  pathsep, 'mtl_mtx')
            mtl_mtx_instance = self.obj.universe.get_obj(mtl_mtx_container_path)
            if mtl_mtx_instance is not None:
                mtl_mtx_container_op = self.__class__(mtl_mtx_instance)
                return mtl_mtx_container_op.dcc_path
    #
    def get_cmr_abc_dcc_path(self):
        shot_name = self.get_variant('self.shot.plf_name')
        shot = self.universe.get_obj(shot_name)
        for obj in shot.get_descendants():
            if obj.type.name == utl_prd_configure.ObjType.CONTAINER:
                if obj.get_variant('self.container.scheme') == 'sot_cmr':
                    return obj.get_variant('self.container.dcc_path')


class AbsElementOpt(AbsIstDef):
    def __init__(self, obj):
        self._set_obj_opt_def_init_(obj)
        self._set_ist_def_init_(obj.type.name)
        self._dcc_use_ist = True
    @property
    def container(self):
        return self.obj.get_parent()
    @property
    def entity_branch(self):
        return self._get_obj_variant_('self.element.entity_branch')
    @property
    def container_scheme(self):
        return self._get_obj_variant_('self.container.data_scheme')
    @property
    def container_data_scheme(self):
        return self._get_obj_variant_('self.container.data_scheme')
    @property
    def container_variant(self):
        return self._get_obj_variant_('self.container.variant')

    def get_container_use_ist(self):
        return self._get_obj_variant_('self.container.use_ist')
    # dcc maya / houdini
    @property
    def use_brh(self):
        return self._get_obj_variant_('self.element.use_brh') or False
    @property
    def dcc_type(self):
        return self._get_obj_variant_('self.element.dcc_type')
    @property
    def dcc_name(self):
        return self._get_obj_variant_('self.element.dcc_name')
    @property
    def dcc_path(self):
        return self._get_obj_variant_('self.element.dcc_path')
    @property
    def dcc_port(self):
        if self.use_brh is True:
            _ = self._get_obj_variant_('self.element.{}.dcc_port'.format(self.entity_branch))
            if _ is not None:
                return _
        return self._get_obj_variant_('self.element.dcc_port')
    #
    @property
    def cmp_dcc_type(self):
        return self._get_obj_variant_('self.element.cmp.dcc_type')
    @property
    def cmp_dcc_name(self):
        return self._get_obj_variant_('self.element.cmp.dcc_name')
    @property
    def cmp_dcc_path(self):
        return self._get_obj_variant_('self.element.cmp.dcc_path')
    @property
    def cmp_dcc_port(self):
        if self.use_brh is True:
            _ = self._get_obj_variant_('self.element.{}.cmp.dcc_port'.format(self.entity_branch))
            if _ is not None:
                return _
        return self._get_obj_variant_('self.element.cmp.dcc_port')
    #
    @property
    def dcc_namespace(self):
        return self._get_obj_variant_('self.element.dcc_namespace')
    # platform
    @property
    def plf_file_path(self):
        return self.get_variant('self.element.vsn_raw')
    @property
    def vsn_key(self):
        return self.get_variant('self.element.vsn_key')
    @property
    def vsn_raw(self):
        return self.get_variant('self.element.vsn_raw')
    @property
    def vsn_cmp_raw(self):
        return self.get_variant('self.element.vsn_cmp_raw')
    # instance
    @property
    def ist_dcc_type(self):
        return self.obj.get_variant('self.element.ist.dcc_type')
    @property
    def ist_dcc_name(self):
        return self.obj.get_variant('self.element.ist.dcc_name')
    @property
    def ist_dcc_path(self):
        return self.obj.get_variant('self.element.ist.dcc_path')
    @property
    def ist_dcc_port(self):
        return self._get_obj_variant_('self.element.ist.dcc_port')
    #
    @property
    def ist_cmp_dcc_type(self):
        return self.obj.get_variant('self.element.ist_cmp.dcc_type')
    @property
    def ist_cmp_dcc_name(self):
        return self.obj.get_variant('self.element.ist_cmp.dcc_name')
    @property
    def ist_cmp_dcc_path(self):
        return self.obj.get_variant('self.element.ist_cmp.dcc_path')
    #
    @property
    def use_mrg(self):
        return self.obj.get_variant('self.element.use_mrg')
    # merge
    @property
    def mrg_dcc_type(self):
        return self.obj.get_variant('self.element.mrg.dcc_type')
    @property
    def mrg_dcc_name(self):
        return self.obj.get_variant('self.element.mrg.dcc_name')
    @property
    def mrg_dcc_path(self):
        return self.obj.get_variant('self.element.mrg.dcc_path')
    # merge compose
    @property
    def mrg_cmp_dcc_type(self):
        return self.obj.get_variant('self.element.mrg_cmp.dcc_type')
    @property
    def mrg_cmp_dcc_name(self):
        return self.obj.get_variant('self.element.mrg_cmp.dcc_name')
    @property
    def mrg_cmp_dcc_path(self):
        return self.obj.get_variant('self.element.mrg_cmp.dcc_path')
    #
    @property
    def manifest_vsn_name(self):
        return self._get_obj_variant_('self.element.manifest.vsn_key')

    def __str__(self):
        return '{}(path={})'.format(
            self.__class__.__name__,
            self.path
        )

    def __repr__(self):
        return self.__str__()


class AbsElementCreator(object):
    CONTAINER_OPT_CLASS = None
    DCC_OBJ_CLASS = None
    def __init__(self, element_opt):
        self._element_opt = element_opt
    @property
    def element_opt(self):
        return self._element_opt
    @property
    def container_opt(self):
        container_obj = self.element_opt.container
        return self.CONTAINER_OPT_CLASS(container_obj)

    def set_create(self):
        raise NotImplementedError()


class AbsEntitiesOpt(AbsEntitiesOptDef):
    ENTITY_TYPE_NAME = None
    #
    SCENE_CLASS = None
    ENTITY_OPT_CLASS = None
    def __init__(self, **kwargs):
        super(AbsEntitiesOpt, self).__init__(**kwargs)

    def set_load_by_plf_path(self, plf_path):
        entity_type = self.universe.get_obj_type(self.ENTITY_TYPE_NAME)
        entity_format_dict = self._set_variant_inherit_(self._format_dict)
        plf_path_format = entity_type.get_variant('plf_path')
        _plf_path = self._set_variant_convert_(plf_path_format, entity_format_dict)
        _plf_path += '/{extra_0}'
        p = parse.parse(_plf_path, plf_path)
        if p:
            entity_format_dict.update(p.named)
            _obj, _is_create = self._set_rsv_file_create_(entity_type, entity_format_dict)
            return _obj, _is_create

    def get_entities(self):
        entity_type = self.universe.get_obj_type(self.ENTITY_TYPE_NAME)
        return entity_type.get_objs()

    def get_entity_opts(self):
        return [self.ENTITY_OPT_CLASS(i) for i in self.get_entities()]


class AbsAssetsOpt(AbsEntitiesOpt):
    def __init__(self, **kwargs):
        super(AbsAssetsOpt, self).__init__(**kwargs)
