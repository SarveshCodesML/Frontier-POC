from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import Docx2txtLoader
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain import PromptTemplate, LLMChain
import chainlit as cl
import pinecone

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
callbacks = [StreamingStdOutCallbackHandler()]

OPENAI_API_KEY = "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"
PINECONE_API_KEY = "5bbf89ec-5a64-4c98-a9bc-a91e8ffcada6"
PINECONE_API_ENV = "gcp-starter"

template = """Please do not answer question if you don't know, just say I am still learning and unable to get answer currently for this question. Question:{question}
Answer:"""

llm = ChatOpenAI(
    temperature=0.0,
    openai_api_key=OPENAI_API_KEY,
    model_name='gpt-3.5-turbo',
    streaming=True, 
    callbacks=[StreamingStdOutCallbackHandler()]

    )

qa = load_qa_chain(
    llm=llm,
    chain_type="stuff",
    callbacks=callbacks
)

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_API_ENV
)

index_name = "python-index"

docsearch = Pinecone.from_existing_index(index_name,embeddings)

@cl.on_message
async def factory(message):
    print(message)
    prompt = PromptTemplate(template=template,input_variables=["question"])
    ##query = "How do I get NFL ticket"
    docs = docsearch.similarity_search(message)
    print("docs searched")
    
    await cl.Message(content=qa.run(input_documents=docs, question=message,prompt=prompt)).send()

    
    
    ##return cl.Message(content=qa.run(input_documents=docs,question=message)).send()