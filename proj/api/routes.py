# api/routes.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List
import tempfile
import requests
import os

from app.embedding import load_document, create_vectorstore
from app.decision import evaluate_with_llm

router = APIRouter()

class QueryRequest(BaseModel):
    documents: str  # URL to the document
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[dict]

@router.post("/api/v1/hackrx/run", response_model=QueryResponse)
def run_query(payload: QueryRequest):
    try:
        # Download the file to a temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            response = requests.get(payload.documents)
            tmp.write(response.content)
            tmp_path = tmp.name

        # Load and embed the document
        docs = load_document(tmp_path)
        vectorstore = create_vectorstore(docs)  # ✅ No API key needed for HuggingFaceEmbeddings

        # Evaluate each query
        results = []
        for q in payload.questions:
            try:
                answer = evaluate_with_llm(q, vectorstore)
                results.append(answer)
            except Exception as e:
                results.append({
                    "decision": "error",
                    "justification": str(e),
                    "amount": None,
                    "clauses_used": []
                })

        return {"answers": results}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
