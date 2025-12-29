from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings import init_embeddings

embed_model = init_embeddings(
    model = "nomic-ai/text-embedding-nomic-embed-text-v1.5",
    provider = "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "not-needed",
    check_embedding_ctx_length=False
)

def load_pdf_resume(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    resume_content = ""
    for page in docs:
        resume_content += page.page_content
    metadata = {
        "source": pdf_path,
        "page_count": len(docs)
    }
    return resume_content, metadata

resume_path = "C:/Users/HP/AppData/Local/Temp/d80dd2f9-c147-4084-b7a0-f8c004f3b6c5_fake-resumes.7z.6c5/resume-005.pdf"
resume_text, resume_info = load_pdf_resume(resume_path)
print(resume_info)
print(resume_text)

resume_embeddings = embed_model.embed_documents([resume_text])
for embedding in resume_embeddings:
    print(f"Len = {len(embedding)} --> {embedding[:4]}")