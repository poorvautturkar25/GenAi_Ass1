from sentence_transformers import SentenceTransformer
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

model = SentenceTransformer("all-MiniLM-L6-V2")

sentences = [
    "I love football.",
    "Soccer is my favorite sport.",
    "Messi talks Spanish."
]

embeddings = model.encode(sentences)

for vec in embeddings:
    print("Len:", len(vec), "-->", vec[:4])

print("Sentence 1 & 2 similarity:", cosine_similarity(embeddings[0], embeddings[1]))
print("Sentence 1 & 3 similarity:", cosine_similarity(embeddings[0], embeddings[2]))
# from sentence_transformers import SentenceTransformer

# # Force fresh download to the new safe folder
# model = SentenceTransformer(
#     "all-MiniLM-L6-V2",
#     cache_folder="D:/Internship/GenAi_Ass1/st_models"  # Use forward slashes on Windows
# )
# print("Model loaded successfully")
