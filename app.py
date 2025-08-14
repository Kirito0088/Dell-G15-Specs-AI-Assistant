# --- Core Libraries ---
import streamlit as st
from dotenv import load_dotenv
import os
import asyncio
import platform
import nest_asyncio # Import the new library

# --- LangChain Libraries ---
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# --- Stronger Fix for asyncio issues ---
# nest_asyncio allows the asyncio event loop to be nested, which is what we need
# for libraries like Google's AI client to work inside Streamlit's event loop.
nest_asyncio.apply()

# --- Application Logic ---

# Load environment variables from .env file
load_dotenv()

# --- Caching the RAG Chain ---
# Re-enabling the cache now that we have a robust asyncio fix.
# This is critical for performance.
@st.cache_resource
def create_rag_chain():
    """
    This function builds the complete Retrieval-Augmented Generation (RAG) chain.
    """
    # 1. Load the knowledge base from the text file
    loader = TextLoader("knowledge.txt")
    documents = loader.load()

    # 2. Split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)

    # 3. Create embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # 4. Create the FAISS vector store
    db = FAISS.from_documents(docs, embeddings)

    # 5. Define the custom prompt template (The "Ethical" Layer)
    prompt_template = """
    You are a helpful AI assistant for answering questions about the Dell G15 5530 laptop.
    You must follow these rules strictly:
    1. Only use the information provided in the context below to answer the question.
    2. If the context does not contain the answer, or if the user asks a question unrelated to the laptop, you MUST respond with: "I'm sorry, I can only answer questions based on the provided specifications for the Dell G15 5530."
    3. Do not answer any harmful, unethical, or inappropriate questions. Refuse politely by using the response from rule #2.

    Context: {context}
    Question: {question}

    Answer:
    """
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    # 6. Initialize the LLM (Google's Gemini model)
    # UPDATED to a current, recommended model name to fix the 404 error.
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

    # 7. Assemble the RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True, # Keep this True as the chain requires it
        chain_type_kwargs={"prompt": PROMPT}
    )
    return qa_chain

# --- Streamlit User Interface ---

# Page Configuration
st.set_page_config(
    page_title="Dell G15 Specs AI",
    page_icon="🤖",
    layout="wide"
)

# --- Sidebar ---
with st.sidebar:
    st.header("About This Project")
    st.info(
        "This is a simple AI assistant built by me (Jayesh Mahajan). "
        "It uses Retrieval-Augmented Generation (RAG) to answer questions "
        "about a Dell G15 5530 laptop based on a provided text file. "
        "This project demonstrates skills learned from IBM's RAG and AI Ethics courses."
    )
    st.warning("The AI can only answer questions based on the data it was given.")

# --- Main App ---
st.title("🤖 My Dell G15 5330 Specs AI Assistant")
st.caption("Powered by my knowledge from IBM's RAG and AI Ethics courses, made by Python.")

# Create the RAG chain by calling our cached function
chain = create_rag_chain()

# Get user input
user_question = st.text_input("Ask me anything about my Dell G15 5530!", placeholder="e.g., How much RAM does it have?")

st.divider()

# Handle user input
if user_question:
    with st.spinner("Consulting the official specs..."):
        result = chain({"query": user_question})
        
        st.header("Answer")
        st.success(result["result"])
