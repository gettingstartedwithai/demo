import os
os.environ["OPENAI_API_KEY"] = 'YOUR-OPEN-AI-KEY'

from pathlib import Path
from llama_index import VectorStoreIndex, StorageContext, GPTVectorStoreIndex, load_index_from_storage, download_loader

if os.path.exists("storage"):
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context) 
else:
    PDFReader = download_loader("PDFReader")
    
    loader = PDFReader()
    
    documents = loader.load_data(file=Path('dominos.pdf'))
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist()

query_engine = index.as_query_engine()
response = query_engine.query("What is this document about?")

print(response)