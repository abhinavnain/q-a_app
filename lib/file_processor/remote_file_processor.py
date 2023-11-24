import urllib.parse, importlib, requests, logging

class RemoteFileProcessor:
    def __init__(self, file_uri, ext = None) -> None:
        self.file_uri = urllib.parse.urlparse(file_uri)
        if not ext:
            self.ext = self.file_uri.path.split(".")[-1].lower()
        else:
            self.ext = ext
        self.attach_reader()

    @property
    def _file_data(self):
        return self.reader.read(self._raw_data_request_object.content)
    
    def attach_reader(self):
        self.reader = getattr(importlib.import_module(f".{self.ext}_reader", package = __name__), 'Reader')()

    def get_file(self):
        logging.info(f"File Loaded! - {self.file_uri.geturl()}")
        self._raw_data_request_object = requests.get(self.file_uri.geturl())