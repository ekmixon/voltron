from .core import Client


class REPLClient(Client):
    """
    A Voltron client for use in the Python REPL (e.g. Calculon).
    """
    def __getattr__(self, key):
        try:
            res = self.perform_request('registers', registers=[key])
            if res.is_success:
                return res.registers[key]
            else:
                print(f"Error getting register: {res.message}")
        except Exception as e:
            print(f"Exception getting register: {repr(e)}")

    def __getitem__(self, key):
        try:
            d = {}
            if isinstance(key, slice):
                d['address'] = key.start
                d['length'] = key.stop - key.start
            else:
                d['address'] = key
                d['length'] = 1

            res = self.perform_request('memory', **d)

            if res.is_success:
                return res.memory
            else:
                print(f"Error reading memory: {res.message}")
        except Exception as e:
            print(f"Exception reading memory: {repr(e)}")

    def __setitem__(self, key, value):
        try:
            d = {}
            if isinstance(key, slice):
                d['address'] = key.start
                d['value'] = ((key.stop - key.start) * value)[:key.stop - key.start]
            else:
                d['address'] = key
                d['value'] = value

            res = self.perform_request('write_memory', **d)

            if res.is_success:
                return None
            else:
                print(f"Error writing memory: {res.message}")
        except Exception as e:
            print(f"Exception writing memory: {repr(e)}")

    def __call__(self, command):
        try:
            res = self.perform_request('command', command=command)
            if res.is_success:
                return res.output
            else:
                print(f"Error executing command: {res.message}")
        except Exception as e:
            print(f"Exception executing command: {repr(e)}")


V = REPLClient()
