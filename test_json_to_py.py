from geppetto.model import GeppettoModel
from mock import Mock

at0 = {'name': 'anontype1'}
at1 = {'name': 'anontype2'}
var0 = {'name': 'var1_type1_lib_1'}
var1 = {'name': 'var2_type1_lib1', 'anonymousTypes': [at0, at1]}
lib0_type0 = {'name': 'type1_lib1', 'variables': [var0, var1]}
lib0_type1 = {'name': 'type2_lib1'}
lib0 = {'name': 'lib1', 'types': [lib0_type0, lib0_type1]}
lib1_type0 = {'name': 'type1_lib2'}
lib1_type1 = {'name': 'type2_lib2'}
lib1 = {'types': [lib1_type0, lib1_type1], 'name': 'lib2'}

refs_types = {
    '//@libraries.0/@types.0': lib0_type0,
    '//@libraries.0/@types.1': lib0_type1,
    '//@libraries.0/@types.0/@variables.1/@anonymousTypes.0': at0,
    '//@libraries.0/@types.0/@variables.1/@anonymousTypes.1': at1,
}

m = Mock(GeppettoModel)
m.json_data = {'name': 'toplevel',
               'libraries': [lib0, lib1],
               'otherList': ['a', 'b', 'c']}


def round_ref(obj):
    ref = GeppettoModel.get_reference_to(m, obj)
    return GeppettoModel.resolve_reference(m, ref)


def round_ref2(ref):
    obj = GeppettoModel.resolve_reference(m, ref)
    return GeppettoModel.get_reference_to(m, obj)


def test_referencing():
    for obj in refs_types.values():
        assert round_ref(obj) == obj
    for ref in refs_types:
        assert round_ref2(ref) == ref
