with open('wellness_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = (
    'def load_engine():\n'
    '    from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings\n'
    '    from llama_index.embeddings.huggingface import HuggingFaceEmbedding\n'
    '    from llama_index.llms.google_genai import GoogleGenAI\n'
    '\n'
    '    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")\n'
    '    api_key = os.environ.get("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"]\n'
    '    Settings.llm = GoogleGenAI(model="gemma-4-26b-a4b-it", api_key=api_key)\n'
    '    docs = SimpleDirectoryReader(".", required_exts=[".pdf", ".html"]).load_data()\n'
    '    index = VectorStoreIndex.from_documents(docs)\n'
    '    return index.as_query_engine(\n'
    '    similarity_top_k=10,\n'
    '    response_mode="tree_summarize",\n'
    ')\n'
)

new = (
    'def load_engine():\n'
    '    import chromadb\n'
    '    from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext\n'
    '    from llama_index.embeddings.huggingface import HuggingFaceEmbedding\n'
    '    from llama_index.llms.google_genai import GoogleGenAI\n'
    '    from llama_index.vector_stores.chroma import ChromaVectorStore\n'
    '\n'
    '    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")\n'
    '    api_key = os.environ.get("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"]\n'
    '    Settings.llm = GoogleGenAI(model="gemma-4-26b-a4b-it", api_key=api_key)\n'
    '\n'
    '    chroma_client = chromadb.PersistentClient(path="./chroma_db")\n'
    '    chroma_collection = chroma_client.get_or_create_collection("wellness_docs")\n'
    '    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)\n'
    '\n'
    '    if chroma_collection.count() > 0:\n'
    '        index = VectorStoreIndex.from_vector_store(vector_store)\n'
    '    else:\n'
    '        docs = SimpleDirectoryReader(".", required_exts=[".pdf", ".html"]).load_data()\n'
    '        storage_context = StorageContext.from_defaults(vector_store=vector_store)\n'
    '        index = VectorStoreIndex.from_documents(docs, storage_context=storage_context)\n'
    '\n'
    '    return index.as_query_engine(\n'
    '    similarity_top_k=10,\n'
    '    response_mode="tree_summarize",\n'
    ')\n'
)

count = content.count(old)
print("Occurrences found:", count)
if count == 0:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('wellness_app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: ChromaDB persistence added to load_engine")

