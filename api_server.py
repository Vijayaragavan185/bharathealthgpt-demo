# api_server.py - Simple working FastAPI server
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from utils import SimpleMedicalAI, SymptomChecker

app = FastAPI(title="BharatHealthGPT Demo API", version="0.1.0")

# Initialize AI
medical_ai = SimpleMedicalAI()
symptom_checker = SymptomChecker()

class HealthQuery(BaseModel):
    text: str
    language: str = "english"

class SymptomQuery(BaseModel):
    symptoms: List[str]
    language: str = "english"

@app.get("/")
async def root():
    return {"message": "BharatHealthGPT Demo API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}

@app.post("/consult")
async def health_consultation(query: HealthQuery):
    """Main health consultation endpoint"""
    try:
        response = medical_ai.generate_response(query.text, query.language)
        return {
            "success": True,
            "data": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/symptom-check")
async def symptom_check(query: SymptomQuery):
    """Symptom checker endpoint"""
    try:
        advice = symptom_checker.check_symptoms(query.symptoms, query.language)
        return {
            "success": True,
            "advice": advice,
            "emergency": "emergency" in advice.lower() or "आपातकाल" in advice
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 Starting BharatHealthGPT Demo API...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
