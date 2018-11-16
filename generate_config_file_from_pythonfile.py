import collections
import logging
import re
import sys
from pprint import pprint

from ast import parse
import _ast

def get_first_string(line):
    chunks = [x.strip() for x in line.split(',')]
    args = []
    kwargs = []
    for item in chunks:
        s = item.split("=")
        if len(s) == 2:
            kwargs.append(tuple(s))
        else:
            args.append(s[0])
    first_arg = args[0]
    return first_arg.strip('\'').strip('\"'), kwargs


def flatten(d, parent_key='', sep='_'):
    """from https://stackoverflow.com/questions/6027558/flatten-nested-python-dictionaries-compressing-keys"""
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def make_everything_a_string(a_dict):
    new_dict = []
    for key, value in a_dict.items():
        print(value)
        new_dict.append((key, str(value)))
    return dict(new_dict)


def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


def ast_parse(configuration):
    a = parse(configuration)

    parsed_settings = {}
    for row in a.body:
        if isinstance(row, _ast.FunctionDef):
            for item in row.body:
                try:
                    setting = item.value.args[0].s
                except IndexError:
                    continue
                arguments = {}
                for p in item.value.keywords:
                    try:
                        keyname = p.arg
                        if isinstance(p.value, _ast.Name):
                            value = p.value.id
                        elif isinstance(p.value, _ast.List):
                            value = [x.s for x in p.value.elts]
                        elif isinstance(p.value, _ast.Tuple):
                            value = [x.s for x in p.value.elts]
                        elif isinstance(p.value, _ast.Num):
                            value = p.value.n
                        else:
                            print(p.value)
                        arguments.update({keyname: value})
                    except IndexError:
                        pass
                parsed_settings.update({setting: arguments})
    return [(x, list(y.items())) for x, y in parsed_settings.items()]

verbose = 0
go = True

if len(sys.argv) > 1:
    if sys.argv[1] == '-v':
        verbose += 1
    if sys.argv[1] == 'h' or sys.argv[1] == '--help':
        go = False
        print("Generator script for configuration of fuga-exporter."
              " takes the configuration.py and parses"
              " its settings and defaults. Then it stores it in"
              " 'gen_configuration.yaml'")
if go:
    try:
        import yaml
        from collections import OrderedDict
        with open('exporter/settings.py', 'r') as f:
            configuration = f.read()

        all_the_settings = ast_parse(configuration)

        master_dict = {}
        for item in all_the_settings:
            keys = item[0].split('.')
            kwargs = dict(item[1])
            for i, x in enumerate(reversed(keys)):
                if i == 0:
                    default = kwargs.get('default')
                    _type = kwargs.get('_type')
                    if _type == 'list':
                        tmp = {x: default or []}
                    elif default is not None:
                        tmp = {x: default}
                    else:
                        tmp = {x: ""}
                else:
                    tmp = {x: tmp}

            dict_merge(master_dict, tmp)
        filename = 'gen_configuration.yaml'
        filename_values_yaml =  "gen_values.yaml"
        with open(filename, 'w') as f:
            yaml.dump(master_dict, stream=f, default_flow_style=False)
            print('Saved config to {filename}'.format(filename=filename))

        values_yaml = {'env': make_everything_a_string(flatten(master_dict, sep="-"))}
        with open(filename_values_yaml, 'w') as f:
            yaml.dump(values_yaml, stream=f, default_flow_style=False)
            print('Saved values to {filename}'.format(filename=filename_values_yaml))

        if verbose>0:
            pprint(master_dict)

    except (KeyError, IndexError):
        print("Error!! probably the configuration.py is malformed")
    except FileNotFoundError as e:
        print("Error!! there is no file {}".format(e.filename))
