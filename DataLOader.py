from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import Docx2txtLoader
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
import docx

OPENAI_API_KEY = "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"
PINECONE_API_KEY = "5bbf89ec-5a64-4c98-a9bc-a91e8ffcada6"
PINECONE_API_ENV = "gcp-starter"

document_path = "Input\FTR-FAQ.docx"



text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1200,
    chunk_overlap=200
)
data = Docx2txtLoader(document_path).load()
docs_chunk = text_splitter.split_documents(data)

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)



pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_API_ENV
)

index_name = "python-index"
pinecone.create_index("python-index",dimension=1536,metric="cosine")

docsearch = Pinecone.from_texts([t.page_content for t in docs_chunk],embeddings,index_name=index_name)

testingIndex = Pinecone.from_existing_index(index_name,embeddings)

query = "How do I get NFL Ticket?"
testingIndex.similarity_search(
    query,
    k=3
)
