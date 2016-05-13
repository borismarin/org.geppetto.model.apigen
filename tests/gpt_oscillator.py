"""
This module will be generated when the API for a given Geppetto Library is
requested (it will be made avaiable along with the exported lib .json).
It should have the same name as the library.
This shields the user from internals (such as the json file itself), so that
the domain classes are prominent.
"""
from os.path import join, abspath, dirname
from geppetto.model import GeppettoModel

# dynamic classes are added to this modules' globals, so that the library can
# be used via "import lib" or "from lib import *"
_g = GeppettoModel(join(dirname(abspath(__file__)), 'oscillator.json'))
globals().update(_g.libs)
