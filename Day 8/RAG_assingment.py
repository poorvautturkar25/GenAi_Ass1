import os
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings import init_embeddings
from langchain.chat_models import init_chat_model

embed_model = init_embeddings(
    model="text-embedding-nomic-embed-text-v1.5",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed",
    check_embedding_ctx_length=False
)

llm = init_chat_model(
    model="llama-3.2-1b-instruct",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed"
)

def load_pdf_resume(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    text = ""
    for page in docs:
        text += page.page_content + "\n"

    return text

def get_chroma_collection():
    client = chromadb.PersistentClient(path="./chroma_db")
    return client.get_or_create_collection(name="resumes")


def ingest_resumes_from_folder(folder_path):
    collection = get_chroma_collection()

    for file in os.listdir(folder_path):
        if not file.lower().endswith(".pdf"):
            continue

        resume_id = file
        pdf_path = os.path.join(folder_path, file)

        existing = collection.get(ids=[resume_id])
        if existing["ids"]:
            collection.delete(ids=[resume_id])

        resume_text = load_pdf_resume(pdf_path)
        embedding = embed_model.embed_documents([resume_text])

        collection.add(
            ids=[resume_id],
            documents=[resume_text],
            embeddings=embedding
        )


def extract_skills_llm(resume_text):
    clean_text = " ".join(resume_text.split())

    prompt = f"""
You are an information extraction system.

Extract ONLY skills, tools, technologies, or competencies
EXPLICITLY written in the resume.

Rules:
- Output ONLY a comma-separated list
- No explanations
- No headings
- No extra text
- If none found, output exactly: No skills listed

Resume text:
{clean_text[:2500]}
"""

    response = llm.invoke(prompt).content.strip()

    skills = response.splitlines()[0]

    banned = ["Here", "skills", "extracted", ":", "•", "|"]
    for b in banned:
        skills = skills.replace(b, "")

    skills = skills.strip(" ,")

    if len(skills.split(",")) < 2:
        return "No skills listed"

    return skills

def generate_reason(resume_text, skills, job_role):
    if skills == "No skills listed":
        return "The resume does not explicitly list technical skills relevant to the job role."

    prompt = f"""
Using ONLY the information below, explain in 2–3 sentences
why this candidate fits the job role: {job_role}.

Candidate resume:
{resume_text[:600]}

Extracted skills:
{skills}

Rules:
- Mention candidate name if present
- Do NOT invent skills
- Do NOT repeat the resume
"""

    response = llm.invoke(prompt).content.strip()

    sentences = response.split(".")
    return ".".join(sentences[:3]).strip()


def shortlist_resumes(job_role, top_k):
    collection = get_chroma_collection()

    query_embedding = embed_model.embed_query(job_role)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    shortlisted = []

    for i in range(len(results["ids"][0])):
        resume_id = results["ids"][0][i]
        resume_text = results["documents"][0][i]

        skills = extract_skills_llm(resume_text)
        reason = generate_reason(job_role, skills, resume_text)

        shortlisted.append({
            "resume_id": resume_id,
            "skills": skills,
            "reason": reason
        })

    return shortlisted


if __name__ == "__main__":

    # Run ONCE, then comment this line
    ingest_resumes_from_folder(
        r"C:\Users\saniy\Downloads\fake-resumes"
    )

    job_role = input("Enter job role: ")
    top_k = int(input("Enter number of resumes to shortlist: "))

    results = shortlist_resumes(job_role, top_k)

    for res in results:
        print("\nResume ID :", res["resume_id"])
        print("Skills    :", res["skills"])
        print("Reason    :", res["reason"])
        print("-" * 50)