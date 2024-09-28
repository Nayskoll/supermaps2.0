from langchain_community.document_loaders import TextLoader
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from mistralai import Mistral
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()
api_key = os.getenv('MISTRAL_API_KEY')

# Charger le texte
loader = TextLoader("raw_text_bolivie.txt")
docs = loader.load()

# Découper le texte en chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
documents = text_splitter.split_documents(docs)

# Initialiser les embeddings Mistral
embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=api_key)

# Créer le magasin de vecteurs avec FAISS
try:
    vector_store = FAISS.from_documents(documents, embeddings)
    print("Vector store created successfully.")
except Exception as e:
    print(f"An error occurred while creating the vector store: {e}")


vector_store_path = "vector_store_faiss"
vector_store.save_local(vector_store_path)
print("Vector store saved successfully.")