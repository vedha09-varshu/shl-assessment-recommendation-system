from fastapi import FastAPI
from pydantic import BaseModel
from retriever.search import search_assessments

app = FastAPI(title="SHL Assessment Recommendation API")

class QueryRequest(BaseModel):
    query: str

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/recommend")
def recommend(request: QueryRequest):
    results = search_assessments(request.query, top_k=6)

    response = []
    for r in results:
        response.append({
            "assessment_name": r["name"],
            "url": r["url"],
            "test_type": r["test_type"]
        })

    return {
        "query": request.query,
        "recommended_assessments": response
    }
