import json

class Reader:
    def read(self, bytes_like):
        str_data = bytes_like.decode('utf-8')
        return json.loads(str_data)
