# coding:utf-8
import re

import os

import fnmatch

import glob

import collections

from lxutil import utl_core, methods


def _var__set_convert_(variant, format_dict):
    if variant is not None:
        re_pattern = re.compile(r'[{](.*?)[}]', re.S)
        #
        keys = re.findall(re_pattern, variant)
        s = variant
        if keys:
            for key in keys:
                if key in format_dict:
                    v = format_dict[key]
                    if v is not None:
                        s = s.replace('{{{}}}'.format(key), format_dict[key])
        return s
    return variant


def _var__get_glob_pattern_(variant):
    if variant is not None:
        re_pattern = re.compile(r'[{](.*?)[}]', re.S)
        #
        keys = re.findall(re_pattern, variant)
        s = variant
        if keys:
            for key in keys:
                s = s.replace('{{{}}}'.format(key), '*')
        return s
    return variant


def _plf_path__get_glob_(plf_path, trim=None):
    glob_pattern = _var__get_glob_pattern_(plf_path)
    results = glob.glob(glob_pattern) or []
    if results:
        results.sort(key=lambda x: methods.String.to_number_embedded_raw(x))
        if trim is not None:
            results = results[trim[0]:trim[1]]
        # fix windows path
        if utl_core._plf__get_is_windows_():
            results = [i.replace('\\', '/') for i in results]
    return results


def _plf_path__get_sequence_(plf_file_path):
    plf_name = os.path.basename(plf_file_path)
    pattern = r'.*?(\d+.*?)[\.]'
    re_pattern = re.compile(pattern, re.IGNORECASE)
    results = re.findall(re_pattern, plf_name) or []
    if results:
        return results[-1]


def _obj_type__get_variants_(obj):
    dic_ = {}
    for port_query in obj.get_port_queries('variants:self.*'):
        dic_[port_query.port_path] = port_query.get()
    lis = dic_.keys()
    lis.sort()
    dic = collections.OrderedDict()
    for i in lis:
        dic[i] = dic_[i]
    return dic


def _obj__get_format_dict_(obj):
    dic_ = {}
    for port in obj.get_ports('variants:self.*'):
        dic_[port.port_path] = port.get()
    #
    lis = dic_.keys()
    lis.sort()
    dic = collections.OrderedDict()
    for i in lis:
        dic[i] = dic_[i]
    return dic


def _dict__set_filter_(input_dict, regex=None):
    dic = collections.OrderedDict()
    keys = fnmatch.filter(input_dict.keys(), regex) or []
    if keys:
        keys.sort()
        for key in keys:
            dic[key] = input_dict[key]
    return dic
