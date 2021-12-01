# coding:utf-8
import os

from lxscheme.scm_objects import _scm_obj_utility

from lxutil import utl_configure


class ObjCategory(object):
    SEQUENCE = 'sequence'
    #
    SCENES = 'scenes'
    #
    PROJECTS = 'projects'
    PROJECT = 'project'
    ENTITIES = 'entities'
    ENTITY = 'entity'
    #
    TAG = 'tag'
    #
    STAGE = 'stage'
    #
    STEP = 'step'
    TASK = 'task'
    EXTRA = 'extra'
    #
    ALL = [
        PROJECT,
        SEQUENCE,
        SCENES,
        PROJECTS,
        ENTITIES,
        ENTITY,
        TAG,
        STAGE,
        STEP,
        EXTRA
    ]
    #
    PORT_QUERY_RAW = {
        # gui
        'icon': {
            'type': 'constant/raw',
            'assign': 'variants',
            'raw': None
        },
        # main
        'name': {
            'type': 'constant/raw',
            'assign': 'variants',
            'raw': None
        },
        'path': {
            'type': 'constant/raw',
            'assign': 'variants',
            'raw': None
        },
        # platform
        'plf_name': {
            'type': 'constant/raw',
            'assign': 'variants',
            'raw': None
        },
        'plf_path': {
            'type': 'constant/raw',
            'assign': 'variants',
            'raw': None
        },
        # dcc
        'dcc_name': {
            'type': 'constant/raw',
            'assign': 'variants',
            'raw': None
        },
        'dcc_path': {
            'type': 'constant/raw',
            'assign': 'variants',
            'raw': None
        },
        'format_dict': {
            'type': 'constant/raw',
            'assign': 'variants',
            'raw': None
        }
    }


class ObjType(object):
    MOVIES = 'movies'
    PROJECTS_PROJECTS = ObjCategory.PROJECTS, MOVIES
    ASSETS = 'assets'
    ENTITIES_ASSETS = ObjCategory.ENTITIES, ASSETS
    SHOTS = 'shots'
    ENTITIES_SHOTS = ObjCategory.ENTITIES, SHOTS
    SETS = 'sets'
    ENTITIES_SETS = ObjCategory.ENTITIES, SETS
    #
    MOVIE = 'movie'
    PROJECT_MOVIE = ObjCategory.PROJECT, MOVIE
    #
    SEQUENCE = 'sequence'
    TAG_SEQUENCE = ObjCategory.TAG, SEQUENCE
    # camera
    CAMERA = 'camera'
    TAG_CAMERA = ObjCategory.TAG, CAMERA
    #
    CHARACTER = 'character'
    TAG_CHARACTER = ObjCategory.TAG, CHARACTER
    PROP = 'prop'
    TAG_PROP = ObjCategory.TAG, PROP
    EFX = 'efx'
    TAG_EFX = ObjCategory.TAG, EFX
    ENVIRONMENT = 'environment'
    TAG_ENVIRONMENT = ObjCategory.TAG, ENVIRONMENT
    CRD = 'crd'
    TAG_CRD = ObjCategory.TAG, CRD
    #
    ASSEMBLY = 'assembly'
    TAG_ASSEMBLY = ObjCategory.TAG, ASSEMBLY
    SCENERY = 'scenery'
    TAG_SCENERY = ObjCategory.TAG, SCENERY
    #
    ASSET = 'asset'
    ENTITY_ASSET = ObjCategory.ENTITY, ASSET
    SET = 'set'
    ENTITY_SET = ObjCategory.ENTITY, SET
    SHOT = 'shot'
    ENTITY_SHOT = ObjCategory.ENTITY, SHOT
    #
    SOURCE = 'source'
    STAGE_SOURCE = ObjCategory.STAGE, SOURCE
    PRODUCT = 'product'
    STAGE_PRODUCT = ObjCategory.STAGE, PRODUCT
    TEMPORARY = 'temporary'
    STAGE_TEMPORARY = ObjCategory.STAGE, TEMPORARY
    #
    MODEL = 'model'
    STEP_MODEL = ObjCategory.STEP, MODEL
    PLANT = 'plant'
    STEP_PLANT = ObjCategory.STEP, PLANT
    RIG = 'rig'
    STEP_RIG = ObjCategory.STEP, RIG,
    GROOM = 'groom'
    STEP_GROOM = ObjCategory.STEP, GROOM
    CHARACTER_EFFECT = 'character_effect'
    STEP_CHARACTER_EFFECT = ObjCategory.STEP, CHARACTER_EFFECT
    SURFACE = 'surface'
    STEP_SURFACE = ObjCategory.STEP, SURFACE
    #
    SET_DRESS = 'set_dress'
    STEP_SET_DRESS = ObjCategory.STEP, SET_DRESS
    #
    LAYOUT = 'layout'
    STEP_LAYOUT = ObjCategory.STEP, LAYOUT
    ANIMATION = 'animation'
    STEP_ANIMATION = ObjCategory.STEP, ANIMATION
    SIMULATION = 'simulation'
    STEP_SIMULATION = ObjCategory.STEP, SIMULATION
    POLISH = 'polish'
    STEP_POLISH = ObjCategory.STEP, POLISH
    LIGHT = 'light'
    STEP_LIGHT = ObjCategory.STEP, LIGHT
    #
    EFFECT = 'effect'
    STEP_EFFECT = ObjCategory.STEP, EFFECT
    #
    RENDER = 'render'
    STEP_RENDER = ObjCategory.STEP, RENDER
    COMPOSE = 'compose'
    STEP_COMPOSE = ObjCategory.STEP, COMPOSE
    #
    TASK = 'task'
    EXTRA_TASK = ObjCategory.EXTRA, TASK
    VARIANT = 'variant'
    EXTRA_VARIANT = ObjCategory.EXTRA, VARIANT
    VERSION = 'version'
    EXTRA_VERSION = ObjCategory.EXTRA, VERSION
    # data
    DTA_CTG = 'dta_ctg'
    EXTRA_DTA_CTG = ObjCategory.EXTRA, DTA_CTG
    DTA_TYP = 'dta_typ'
    EXTRA_DTA_TYP = ObjCategory.EXTRA, DTA_TYP
    #
    MANIFEST = 'manifest'
    EXTRA_MANIFEST = ObjCategory.EXTRA, MANIFEST
    SCENE = 'scene'
    EXTRA_SCENE = ObjCategory.EXTRA, SCENE
    #
    REFERENCE = 'reference'
    EXTRA_REFERENCE = ObjCategory.EXTRA, REFERENCE
    #
    INSTANCE = 'instance'
    EXTRA_INSTANCE = ObjCategory.EXTRA, INSTANCE
    #
    CONTAINER = 'container'
    EXTRA_CONTAINER = ObjCategory.EXTRA, CONTAINER
    #
    ELEMENT = 'element'
    EXTRA_ELEMENT = ObjCategory.EXTRA, ELEMENT
    #
    ALL = [
        # group
        PROJECTS_PROJECTS,
        PROJECT_MOVIE,
        #
        ENTITIES_ASSETS,
        ENTITIES_SHOTS,
        ENTITIES_SETS,
        #
        TAG_CAMERA,
        #
        TAG_CHARACTER,
        TAG_PROP,
        TAG_ENVIRONMENT,
        TAG_EFX,
        TAG_CRD,
        #
        TAG_SEQUENCE,
        #
        TAG_ASSEMBLY,
        TAG_SCENERY,
        # entity
        ENTITY_ASSET,
        # ENTITY_SET,
        ENTITY_SHOT,
        #
        STAGE_SOURCE,
        STAGE_PRODUCT,
        STAGE_TEMPORARY,
        # step
        STEP_MODEL,
        STEP_PLANT,
        STEP_RIG,
        STEP_GROOM,
        STEP_CHARACTER_EFFECT,
        STEP_EFFECT,
        STEP_SURFACE,
        #
        STEP_SET_DRESS,
        #
        STEP_LAYOUT,
        STEP_ANIMATION,
        STEP_SIMULATION,
        STEP_POLISH,
        STEP_LIGHT,
        #
        STEP_RENDER,
        STEP_COMPOSE,
        # extra
        EXTRA_TASK,
        EXTRA_VARIANT,
        EXTRA_VERSION,
        #
        EXTRA_DTA_CTG,
        EXTRA_DTA_TYP,
        #
        EXTRA_MANIFEST,
        EXTRA_SCENE,
        #
        EXTRA_REFERENCE,
        EXTRA_INSTANCE,
        EXTRA_CONTAINER,
        EXTRA_ELEMENT
    ]


class Root(object):
    main = '/'.join(
        os.path.dirname(__file__.replace('\\', '/')).split('/')
    )
    icon = '{}/.icon'.format(main)
    data = '{}/.data'.format(main)
    doc = '{}/.doc'.format(main)


class Doc(object):
    SCENE_BUILD = '{}/scene_build_help.md'.format(Root.doc)


class Scheme(object):
    UTILITY_TYPES = _scm_obj_utility.FileScheme(
        '{}/utility/product/type_configures_test.yml'.format(utl_configure.Root.DATA)
    )
    HOUDINI_TYPES = _scm_obj_utility.FileScheme(
        '{}/houdini/product/type_configures.yml'.format(utl_configure.Root.DATA)
    )
    MAYA_TYPES = _scm_obj_utility.FileScheme(
        '{}/maya/product/type_configures.yml'.format(utl_configure.Root.DATA)
    )


class Name(object):
    AR_PATH_CONVERT = 'arnold_path_convert_default'
