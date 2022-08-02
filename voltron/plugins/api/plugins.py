import voltron
import voltron.api
from voltron.api import *

from scruffy.plugin import Plugin


class APIPluginsRequest(APIRequest):
    """
    API plugins request.

    {
        "type":         "request",
        "request":      "plugins"
    }
    """
    @server_side
    def dispatch(self):
        return APIPluginsResponse()


class APIPluginsResponse(APISuccessResponse):
    """
    API plugins response.

    {
        "type":         "response",
        "status":       "success",
        "data": {
            "plugins": {
                "api": {
                    "version": ["api_version", "host_version", "capabilities"]
                    ...
                },
                "debugger": {
                    ...
                },
                ...
            }
        }
    }
    """
    _fields = {
        'plugins': True
    }

    def __init__(self, *args, **kwargs):
        super(APIPluginsResponse, self).__init__(*args, **kwargs)
        self.plugins = {
            'api': {
                n: {
                    'request': p.request_class._fields,
                    'response': p.response_class._fields,
                }
                for (n, p) in voltron.plugin.pm.api_plugins.iteritems()
            },
            'debugger': list(voltron.plugin.pm.debugger_plugins),
            'view': list(voltron.plugin.pm.view_plugins),
            'command': list(voltron.plugin.pm.command_plugins),
            'web': list(voltron.plugin.pm.web_plugins),
        }


class APIPluginsPlugin(APIPlugin):
    request = 'plugins'
    request_class = APIPluginsRequest
    response_class = APIPluginsResponse
