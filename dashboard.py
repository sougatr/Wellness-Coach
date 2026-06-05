import os
import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core import Settings

st.set_page_config(page_title="Wellness Coach: Unleashing the Super Ager Within", layout="wide")

st.title("Wellness Coach: Unleashing the Super Ager Within")
st.caption("Evidence-based answers grounded in trusted wellness and healthy-ageing guidelines")

@st.cache_resource
def load_engine():
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    api_key = os.environ.get("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"]
    Settings.llm = GoogleGenAI(model="gemma-4-26b-a4b-it", api_key=api_key)
    docs = SimpleDirectoryReader(".", required_exts=[".pdf"]).load_data()
    index = VectorStoreIndex.from_documents(docs)
    return index.as_query_engine()

engine = load_engine()

question = st.text_input("Ask a question about your guidelines:")

if question:
    with st.spinner("Searching your documents..."):
        answer = engine.query(question)
    st.subheader("Answer")
    st.write(str(answer))
    st.subheader("Sources used")
    for i, node in enumerate(answer.source_nodes):
        st.markdown(f"**Source {i+1}** (relevance: {node.score:.2f})")
        st.write(node.node.get_content()[:300] + "...")
