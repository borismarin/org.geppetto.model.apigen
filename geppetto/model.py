from __future__ import print_function
import re
from itertools import count
import json

from toposort import toposort_flatten


class GeppettoModel(object):
    """
    This class is intended to be used by an (generated) "intermediate" module that dynamically
    creates and exports library (json) specific classes - shielding the user from
    directly instantiating this class for a particular lib (json).
    """

    def __init__(self, json_file):
        with open(json_file) as data_file:
            self.data = json.load(data_file)
            self.domain_types = {}
            self.dependency_graph = self.build_dependency_graph()
            self.generate_all_py_types()

    def build_dependency_graph(self):
        deps = {}
        for ty in self.all_types():
            supers = (self.resolve_reference(str(sup['$ref']))['name']
                      for sup in ty.get('superType', []))
            deps[ty['name']] = set(supers)
        return deps

    def all_types(self):
        return (ty for lib in self.data['libraries'] for ty in lib['types'])

    def new_instance(self, iid, iname, itype):
        if 'variables' not in self.data:
            self.data.variables = []
        self.data['variables'].append(self.new_variable(iid, iname, itype))

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
            json.dump(self.data, outfile)

    def get_reference(self, referenced):
        """
            This function generates the reference for a given node inside the JSON
            E.g. {"eClass":"Type"...} -> "//@libraries.1/@types.2"
        """
        pass

    def resolve_reference(self, refstring):
        """
            This function resolves a reference and returns an object inside the JSON data
            E.g. "//@libraries.1/@types.2" -> {"eClass":"Type"...}

            @libraries.0/@types.20/@variables.5/@anonymousTypes.0/@variables.7
            @libraries.1/@types.5
            @tags.1/@tags.5
            @libraries.0/@types.8/@visualGroups.0/@visualGroupElements.1

        """
        def access(dic, key, idx):
            return dic[key][idx]

        ref = self.data
        for k, i in re.findall("([a-zA-Z]*)\.(\d*)", refstring):
            ref = access(ref, k, int(i))

        return ref

    def generate_py_type(self, type_name):
        def init(self, iid=None, name=''):
            if iid is None:
                self.id = type_name + '_' + str(self._ids.next())
            else:
                self.id = iid
            print('New instance of type  [', self.__class__.__name__,
                  tuple(b.__name__ for b in self.__class__.__bases__),
                  '], id:', self.id, 'name:', name)
            #g.new_instance(self.id, self.name, self)
        namespace = {}
        namespace['__init__'] = init
        namespace['_ids'] = count(0)
        namespace['supertypes'] = self.dependency_graph[type_name]
        deps = tuple(self.domain_types[d]
                     for d in self.dependency_graph[type_name])
        supertypes = deps if len(deps) > 0 else (object,)
        return type(type_name, supertypes, namespace)

    def generate_all_py_types(self):
        for t in map(str, toposort_flatten(self.dependency_graph)):
            self.domain_types[t] = self.generate_py_type(t)
