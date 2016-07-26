import ipywidgets as widgets
from ipywidgets.widgets import EventfulDict
from traitlets import Unicode, Instance
from IPython.display import display, Javascript
class PyPopupWidget(widgets.DOMWidget):
    _view_name = Unicode('PyPopupView').tag(sync=True)
    _view_module = Unicode('PyPopup').tag(sync=True)
    id = Unicode('newJupyterWidget').tag(sync=True)
    name = Unicode('newJupyterWidget').tag(sync=True)
    
    def __init__(self, **kwargs):
        """Constructor"""
        widgets.DOMWidget.__init__(self, **kwargs) # Call the base.
               
    @property   
    def subscribe(self):        
        display(Javascript('window.parent.GEPPETTO.WidgetFactory.pyPopupsController.subscribe()'))
        
    
    #value = Unicode('Hello World!').tag(sync=True)
    #taka = Unicode('takeer').tag(sync=True)
    #value2 = Instance('Hello World!').tag(sync=True)
    #value3 = EventfulDict().tag(sync=True)  
    
class GeppettoController():
    def addWidget(widgetId):
        display(Javascript('window.parent.G.addWidget(%d)'%widgetId))
        
