import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_mistralai.chat_models import ChatMistralAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

# Charger les variables d'environnement
load_dotenv()
api_key = os.getenv('MISTRAL_API_KEY')

# Charger le texte
def load_documents(file_path):
    loader = TextLoader(file_path)
    docs = loader.load()
    return docs

# Initialiser les embeddings et charger le vector store
def initialize_vector_store(vector_store_path, embeddings):
    return FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)

# Configurer le modèle de génération Mistral
def initialize_mistral_model(api_key):
    return ChatMistralAI(mistral_api_key=api_key)

# Créer un template de prompt pour la génération de réponses
def create_prompt_template():
    return ChatPromptTemplate.from_template("""
    Answer the following question based on the provided context:
    <context>
    {context}
    </context>

    Question: {input}
    """)

# Fonction pour récupérer les documents les plus pertinents
def retrieve_documents(vector_store, query, k=5):
    retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": k})
    docs = retriever.invoke(query)
    return docs

# Concaténer les documents récupérés en un contexte
def concatenate_documents(docs):
    return "\n\n".join([doc.page_content for doc in docs])

# Générer une réponse basée sur les documents récupérés
def generate_response(model, prompt_template, context, question):
    prompt_text = prompt_template.format(context=context, input=question)
    response = model.invoke(prompt_text)
    return response

# Pipeline complet pour poser une question et obtenir une réponse
def qa_pipeline(api_key, vector_store_path, query, file_path=None, k=5):
    # Charger ou générer les documents et embeddings si nécessaire
    embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=api_key)
    
    # Charger le vector store
    vector_store = initialize_vector_store(vector_store_path, embeddings)
    
    # Récupérer les documents les plus pertinents
    docs = retrieve_documents(vector_store, query, k)

    # Concaténer les documents pour former le contexte
    context = concatenate_documents(docs)

    # Initialiser le modèle Mistral
    model = initialize_mistral_model(api_key)

    # Créer le template de prompt
    prompt_template = create_prompt_template()

    # Générer une réponse à partir du modèle
    response = generate_response(model, prompt_template, context, query)

    return response

# Exécution du pipeline pour une question donnée
if __name__ == "__main__":
    vector_store_path = "vector_store_faiss"
    #query = "Quels sont les meilleurs endroits à visiter en Bolivie ? fais une reponse structurée en bulletpoints."
    query = "peux-tu me citer 30 noms de restaurants en bolivie ?"

    response = qa_pipeline(api_key, vector_store_path, query, k=5)
    print("Réponse générée :", response)