'''#1. Basic fixed-sized chunking
from langchain_text_splitters import CharacterTextSplitter

raw_text = """
LangChain is a framework for developing applications powered by language models.
It provides tools for chunking, embeddings, vector stores, and chains.
Chunking helps split large text into smaller pieces for efficient processing.
"""
text_splitter = CharacterTextSplitter(chunk_size=50, chunk_overlap=10, separator="")
docs = text_splitter.create_documents([raw_text])

for doc in docs:
    print(doc.page_content)
'''

'''#2.Recursive character chunking
from langchain_text_splitters import RecursiveCharacterTextSplitter
raw_text = """
LangChain is a framework for developing applications powered by language models.
It provides tools for chunking, embeddings, vector stores, and chains.
Chunking helps split large text into smaller pieces for efficient processing.
"""
text_splitter = RecursiveCharacterTextSplitter(chunk_size=10, chunk_overlap=5,
                                               separators=["\n\n", "\n"," ", ""])
docs = text_splitter.create_documents([raw_text])

for doc in docs:
    print(doc.page_content)'''

'''#3.Token-based chunking
from langchain_text_splitters import TokenTextSplitter
raw_text = """
LangChain is a framework for developing applications powered by language models.
It provides tools for chunking, embeddings, vector stores, and chains.
Chunking helps split large text into smaller pieces for efficient processing.
"""
text_splitter = TokenTextSplitter(chunk_size=20, chunk_overlap=10)
docs = text_splitter.create_documents([raw_text])

for doc in docs:
    print(doc.page_content)'''

'''#4.Markdown-aware chunking
from langchain_text_splitters import MarkdownHeaderTextSplitter

markdown_text = """
# LangChain

LangChain is a framework for developing applications powered by language models.

## Features

- Chunking
- Embeddings
- Vector Stores
- Chains

## Use Cases

### RAG
Retrieval-Augmented Generation uses external knowledge.

### Agents
Agents can use tools to perform tasks.
"""
headers_to_split_on = [("#", "Header 1"),("##", "Header 2"),("###", "Header 3")]
text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
docs = text_splitter.split_text(markdown_text)
for doc in docs:
    print(doc.page_content)'''

'''#5. Code-Aware chunking
from langchain_text_splitters import RecursiveCharacterTextSplitter

code_text = """
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

print(add(2, 3))
print(multiply(4, 5))
"""
code_splitter = RecursiveCharacterTextSplitter.from_language(language="python",chunk_size=70,chunk_overlap=50)
docs = code_splitter.create_documents([code_text])
for doc in docs:
    print(doc.page_content)
'''

#6.sentence-based chunking(NLP-style)
from langchain_text_splitters import SentenceTransformersTokenTextSplitter
text_splitter = SentenceTransformersTokenTextSplitter(chunk_size=256, chunk_overlap=20)
docs = text_splitter.create_documents([raw_text])
