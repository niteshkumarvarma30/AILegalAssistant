from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import sys
import os
rag_path = os.path.join(os.path.dirname(__file__), "rag")
if rag_path not in sys.path:
    sys.path.append(rag_path)
try:
    from rag.vector_search import search_vectors
except ModuleNotFoundError:
    from rag.vector_search import search_vectors
from rag.llm import generate_summary
from rag.explainability import explain_answer
from pdf.pdf_extract import extract_text_from_pdf
from utils.translation import translate_text
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    role: str = "citizen"
    lang: str = "en"

@app.post("/query")
async def query_legal(request: QueryRequest):
    query = request.query
    role = request.role
    lang = request.lang
    # Step 1: (Optional) Translate query to English
    if lang != "en":
        query = translate_text(query, target_lang="en")
    # Step 2: Vector search
    docs, scores = search_vectors(query)
    # Step 3: LLM summary
    answer = generate_summary(query, docs, role)
    # Step 4: Explainability
    highlights = explain_answer(answer, docs)
    # Step 5: (Optional) Translate answer back
    if lang != "en":
        answer = translate_text(answer, target_lang=lang)
    return {"answer": answer, "highlights": highlights, "docs": docs}

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    text = extract_text_from_pdf(await file.read())
    return {"text": text}