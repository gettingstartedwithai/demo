import os
os.environ["OPENAI_API_KEY"] = 'YOUR-OPEN-AI-KEY'

from pathlib import Path
from llama_index import VectorStoreIndex, download_loader

PDFReader = download_loader("PDFReader")

loader = PDFReader()
documents = loader.load_data(file=Path('dominos.pdf'))

index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()
response = query_engine.query("What is this document about?")

print(response)