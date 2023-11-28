__import__('pysqlite3')
import os, sys, pytest, time
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from lib.lanchain_utils.lanchain_simple_pipeline import LangchainSimplePipeline

@pytest.fixture
def langchain_simple_pipeline():
    file_uri = "https://compliancereportszania.blob.core.windows.net/soc2-reports/safebase-short.json"  # Replace with your file URI
    file_type = "json" 
    langchain_simple_pipeline = LangchainSimplePipeline(file_uri, file_type)
    return langchain_simple_pipeline

def test_download_file(langchain_simple_pipeline):
    time.sleep(60)
    assert langchain_simple_pipeline.temp_file_path is not None
    assert os.path.exists(langchain_simple_pipeline.temp_file_path)

def test_load_data(langchain_simple_pipeline):
    time.sleep(60)
    data = langchain_simple_pipeline.load_data()
    assert isinstance(data, list)
    assert len(data) > 0

def test_split_data(langchain_simple_pipeline):
    time.sleep(60)
    ai_data = langchain_simple_pipeline.load_data()
    splits = langchain_simple_pipeline.split_data(ai_data)
    assert isinstance(splits, list )
    assert len(splits) > 0

def test_ask(langchain_simple_pipeline):
    time.sleep(60)
    question = "What are the controls in place?"
    response = langchain_simple_pipeline.ask(question)
    assert isinstance(response, str)
    assert len(response) > 0