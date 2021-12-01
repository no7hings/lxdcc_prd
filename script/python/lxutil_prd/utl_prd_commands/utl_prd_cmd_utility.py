# coding:utf-8
from ..utl_prd_objects import _utl_prd_obj_scene, _utl_prd_obj_callback


def get_scene():
    return _utl_prd_obj_scene.Scene()


def set_scene_load_from_scene(file_path):
    scene = _utl_prd_obj_scene.Scene()
    scene.set_load_by_scene_file_path(file_path)
    _utl_prd_obj_callback.__dict__['SCENE'] = scene
    return scene


def get_current_scene():
    return _utl_prd_obj_callback.__dict__['SCENE']


def set_current_scene(scene):
    _utl_prd_obj_callback.__dict__['SCENE'] = scene
