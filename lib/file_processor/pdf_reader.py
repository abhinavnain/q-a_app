import io
from PyPDF2 import PdfReader

class Reader:
    def read(self, bytes_like):
        with io.BytesIO(bytes_like) as open_pdf_file:
            reader = PdfReader(open_pdf_file)
            text = ""
            for page in reader.pages:
                text += "\n" + page.extract_text()
            return text