import gpt_oscillator as lib

def test_dynamic_types():
    assert(type(lib.oscillator) is type)
    osc = lib.oscillator("o_id","o_name")
    assert(osc.id == 'o_id')

def test_default_ids():
    o2 = lib.oscillator()
    o3 = lib.oscillator()
    assert(o2.id == 'oscillator_0')
    assert(o3.id == 'oscillator_1')

def test_type_inheritance():
    so = lib.aSpecialOcillator()
    assert(isinstance(so, lib.oscillator))
