import os
from langchain.embeddings import VertexAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.llms import VertexAI
from langchain.chains import ConversationalRetrievalChain

from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# setting the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the file path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ["credentials"]


class Agent:
    def __init__(self):

        self.embeddings = VertexAIEmbeddings(temperature=0)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

        self.llm = VertexAI(model_name="code-bison", max_output_tokens=100, temperature=0.1)

        self.chat_history = None
        self.chain = None
        self.db = None

    def ask(self, question: str) -> str:
        if self.chain is None:
            response = "Please, Add Your document."
        else:
            response = self.chain({"question": question, "chat_history": self.chat_history})
            response = response["answer"].strip()
            self.chat_history.append((question, response))
        return response

    def ingest(self, file_path: os.PathLike) -> None:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        splitted_documents = self.text_splitter.split_documents(documents)

        if self.db is None:
            self.db = FAISS.from_documents(splitted_documents, self.embeddings)
            self.chain = ConversationalRetrievalChain.from_llm(self.llm, self.db.as_retriever())
            self.chat_history = []
        else:
            self.db.add_documents(splitted_documents)

    def forget(self) -> None:
        self.db = None
        self.chain = None
        self.chat_history = None
