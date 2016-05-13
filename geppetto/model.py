from __future__ import print_function
import imp
import re
from itertools import count
import json


class GeppettoModel(object):
    """
        This class is intended to be used by an "intermediate" (generated)
        module that dynamically creates and exports library-specific classes,
        shielding users from directly instantiating GeppettoModel('lib.json')
        for a particular lib.
    """

    def __init__(self, json_file):
        with open(json_file) as data_file:
            self.json_data = json.load(data_file)
            self.type_registry = {}
            # self.dependency_graph = self.build_dependency_graph()
            self.libs = self.generate_all_libs()

    def new_instance(self, iid, iname, itype):
        if 'variables' not in self.json_data:
            self.json_data['variables'] = []
        self.json_data['variables'].append(self.new_variable(iid, iname, itype))

    def new_variable(self, vid, name, vtype):
        return {'eClass': 'Variable', 'id': vid, 'name': name, 'type': vtype}

    def delete_instance(self, variable):
        pass

    def new_type(self, id, name, super_types, target_library):
        pass

    def new_library(self, id, name):
        pass

    def dump_to_file(self, filename):
        with open(filename, 'w') as outfile:
            json.dump(self.json_data, outfile)

    def get_reference_to(self, referenced):
        """
            Generates a reference string for a given node inside the
            JSON E.g. {"eClass":"Type"...} -> "//@libraries.1/@types.2"
        """
        def finder(iterable):
            if isinstance(iterable, dict):
                for k, v in iterable.iteritems():
                    if finder(v):
                        return '/@' + str(k) + '.' + finder(v)
            elif isinstance(iterable, list):
                if referenced in iterable:
                    return str(iterable.index(referenced))  # stop recursion
                else:
                    for idx, it in enumerate(iterable):
                        if finder(it):
                            return str(idx) + finder(it)
        return '/' + finder(self.json_data)

    def resolve_reference(self, refstring):
        """
            Resolve geppetto JSON reference syntax into dictionary
            E.g. "//@libraries.1/@types.2" -> {"eClass":"Type"...}
        """
        def access(dic, key, idx):
            return dic[key][idx]

        ref = self.json_data
        for k, i in re.findall('([a-zA-Z]*)\.(\d*)', refstring):
            ref = access(ref, k, int(i))

        return ref

    def supertypes(self, json_type):
        supers = set()
        for super_ref in map(str, json_type.get('superType', [])):
            json_type = self.resolve_reference(super_ref)
            supers.add(self.get_python_type(json_type))
        return tuple(supers) if len(supers) > 0 else (object,)

    def get_python_type(self, json_type):
        type_ref = self.get_reference_to(json_type)
        try:
            ty = self.type_registry[type_ref]
        except KeyError:
            ty = self.json_type_to_py_type(json_type)
            self.type_registry[type_ref] = ty
        return ty

    def json_type_to_py_type(self, json_type):
        type_name = str(json_type['name'])

        def init(selfish, iid=None, name=''):
            if iid is None:
                selfish.id = type_name + '_' + str(selfish._ids.next())
            else:
                selfish.id = iid
            print('New instance of type  [', selfish.__class__.__name__,
                  tuple(b.__name__ for b in selfish.__class__.__bases__),
                  '], id:', selfish.id, 'name:', name)
            # selfish._json_wrapper.new_instance(selfish.id, selfish.name,)
        namespace = {}
        namespace['__init__'] = init
        namespace['_ids'] = count(0)
        # namespace['_json_wrapper'] = self
        # namespace.update(self.type_properties(json_type))
        return type(type_name, self.supertypes(json_type), namespace)

    def types_in_library(self, lib):
        return (self.get_python_type(ty) for ty in lib['types'])

    def generate_lib(self, lib):
        module = imp.new_module(lib['id'])
        for ty in self.types_in_library(lib):
            setattr(module, ty.__name__, ty)
        return module

    def generate_all_libs(self):
        return {str(lib['id']): self.generate_lib(lib)
                for lib in self.json_data['libraries']}
