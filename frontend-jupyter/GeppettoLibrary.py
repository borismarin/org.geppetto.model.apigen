import ipywidgets as widgets
from traitlets import (Unicode, Instance, List)

class ComponentWidget(widgets.Widget):
    _view_name = Unicode('ComponentView').tag(sync=True)
    _view_module = Unicode('geppettoWidgets').tag(sync=True)
    
    widget_id = Unicode('').tag(sync=True)
    component_name = Unicode('').tag(sync=True)
    
    def __init__(self, **kwargs):
        super(ComponentWidget, self).__init__(**kwargs)
        self._click_handlers = widgets.CallbackDispatcher()
        self.on_msg(self._handle_button_msg)
        
    def on_click(self, callback, remove=False):
        """Register a callback to execute when the button is clicked.

        The callback will be called with one argument, the clicked button
        widget instance.

        Parameters
        ----------
        remove: bool (optional)
            Set to true to remove the callback from the list of callbacks.
        """
        self._click_handlers.register_callback(callback, remove=remove)

    def _handle_button_msg(self, _, content, buffers):
        """Handle a msg from the front-end.

        Parameters
        ----------
        content: dict
            Content of the msg.
        """
        if content.get('event', '') == 'click':
            self._click_handlers(self, content)

class PanelWidget(widgets.Widget):
    _view_name = Unicode('PanelView').tag(sync=True)
    _view_module = Unicode('geppettoWidgets').tag(sync=True)
    _model_name = Unicode('PanelModel').tag(sync=True)
    _model_module = Unicode('geppettoWidgets').tag(sync=True)
        
    items = List(Instance(ComponentWidget)).tag(sync=True, **widgets.widget_serialization)    
    
    def __init__(self, **kwargs):
        super(PanelWidget, self).__init__(**kwargs)
        self._click_handlers = widgets.CallbackDispatcher()
        self.on_msg(self._handle_income_msg)
        
    def on_click(self, callback, remove=False):
        """Register a callback to execute when the button is clicked.

        The callback will be called with one argument, the clicked button
        widget instance.

        Parameters
        ----------
        remove: bool (optional)
            Set to true to remove the callback from the list of callbacks.
        """
        self._click_handlers.register_callback(callback, remove=remove)

    def _handle_income_msg(self, _, content, buffers):
        """Handle a msg from the front-end.

        Parameters
        ----------
        content: dict
            Content of the msg.
        """
        if content.get('event', '') == 'click':
            self._click_handlers(self)
    
    def addChild(self, child):
        self.items = [i for i in self.items] + [child]
