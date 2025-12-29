from langchain_huggingface import HuggingFaceEmbeddings

emb = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

print("Embedding length:", len(emb.embed_query("hello world")))
