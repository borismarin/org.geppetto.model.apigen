from websocket import create_connection

class QDSockets(object):

    msgs = {
        'CLIENT_ID': 'client_id',
        'RELOAD_CANVAS': 'reload_canvas',
        'ERROR_LOADING_SIM': 'error_loading_simulation',
        'ERROR_LOADING_PROJECT': 'error_loading_project',
        'ERROR_DOWNLOADING_MODEL': 'error_downloading_model',
        'ERROR_DOWNLOADING_RESULT': 'error_downloading_results',
        'ERROR': 'generic_error',
        'INFO_MESSAGE': 'info_message',
        'GEPPETTO_VERSION': 'geppetto_version',
        'OBSERVER_MODE': 'observer_mode_alert',
        'READ_URL_PARAMS': 'read_url_parameters',
        'SCRIPT_FETCHED': 'script_fetched',
        'SERVER_AVAILABLE': 'server_available',
        'SERVER_UNAVAILABLE': 'server_unavailable'
    }

    def __init__(self, host):
        self.host = host

    def _send(self, payload):
        return self.ws.send(payload)

    def _receive(self):
        return self.ws.recv()

    def __enter__(self):
        self.ws = create_connection(self.host)
        self._send('hello')

        print 'Received "%s"' % self._receive()  # expectin 'ping'
        print 'reading again: %s' % self._receive()

    def __exit__(self, exc_type, exc_value, traceback):
        print 'closing socket'
        self.ws.close()


if __name__ == '__main__':
    host = 'ws://localhost:8080/org.geppetto.frontend/GeppettoServlet'
    with QDSockets(host) as sock:
        pass
