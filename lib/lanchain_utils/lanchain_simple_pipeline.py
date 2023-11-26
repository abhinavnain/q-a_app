import importlib, urllib, requests, os, logging, datetime, time
from .json_processor import JSONProcessor

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

from langchain import hub
from langchain.chat_models import ChatOpenAI

from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

"""

    This Class follows the RAG Pattern described in - https://python.langchain.com/docs/use_cases/question_answering/
    There are 5 basic Steps to the process- 
    1. Load
    2. Split
    3. Store
    4. Retrieve
    5. Generate

"""
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

class LangchainSimplePipeline:
    LOADERS = {"json": "CSVLoader", "pdf": "PyPDFLoader"}
    def __init__(self,file_uri, file_type) -> None:
        self.file_uri = urllib.parse.urlparse(file_uri)
        self.file_type = file_type
        self.last_ask = None
        self.download_file()
        self.attach_loader()
        self.setup_llm()
    """
        STEP 1.1 -- Load: Download the requested FILE and preprocess it for loading
    """
    def download_file(self):
        file_content = requests.get(self.file_uri.geturl()).content
        self.temp_file_path = os.path.join("/","tmp",self.file_uri.path.split("/")[-1])
        if self.file_type == 'json':
            self.temp_file_path = JSONProcessor(file_content, ['content', 'answer', 'comment']).file_path
        else:
            with open(self.temp_file_path, "wb") as temp_file:
                temp_file.write(file_content)

    """
        STEP 1.2 -- Load: Attach the required loader - Based on different Format for now its configured only for JSON and PDF.
            Please Note that JSONs are converted to CSV for proper ingestion.
    """
    def attach_loader(self):
        self.loader = getattr(importlib.import_module("langchain.document_loaders", package = __name__), self.LOADERS[self.file_type])

    """
        STEP 1.3 -- Load: Final Step to load the Data into an instance variable
    """
    def load_data(self):
        loader = self.loader(self.temp_file_path)
        return loader.load()

    """
        STEP 2 -- Split: Basic Document Splitting
    """
    def split_data(self, data):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return text_splitter.split_documents(data)
    
    """
        STEP 3,4 & 5 -- Store: Store Data in Vector DB with OpenAIEmbeddings
        Setup Retriever Object
        Setup Prompt
    """
    def setup_llm(self):
        ai_data = self.load_data()
        splits = self.split_data(ai_data)
        vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
        retriever = vectorstore.as_retriever()
        prompt = hub.pull("rlm/rag-prompt")
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        self.rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )    
    def ask(self,question):
        self.rate_limitter()
        return self.rag_chain.invoke(question)
    def rate_limitter(self, wait_time = 20):
        current_time = datetime.datetime.now()
        if self.last_ask:
            seconds_so_far = (current_time - self.last_ask).seconds
            if seconds_so_far < wait_time:
                time.sleep(wait_time - seconds_so_far)
        self.last_ask = datetime.datetime.now()
        
