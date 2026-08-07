from pathlib import Path
from pydantic import BaseModel
from typing import Optional

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .pdf_service import extract_text_from_pdf
from .gemini_service import analyze_contract, answer_question


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app = FastAPI(title="ClauseIQ API")


# Allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global storage for contract text (session-based)
last_contract_text = ""


# Pydantic model for ask endpoint
class QuestionRequest(BaseModel):
    question: str


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "ClauseIQ Backend Running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    """Analyze a PDF contract using Gemini AI"""
    try:
        # Read uploaded PDF
        pdf_bytes = await file.read()

        # Extract text from PDF
        contract_text = extract_text_from_pdf(pdf_bytes)

        # Check whether text was extracted
        if not contract_text.strip():
            return {
                "error": "Could not extract text from the PDF."
            }

        # Send contract text to Gemini
        analysis = analyze_contract(contract_text)

        # Store the contract text for follow-up questions
        global last_contract_text
        last_contract_text = contract_text

        # Return analysis to frontend
        return {
            "filename": file.filename,
            "analysis": analysis
        }
    except Exception as e:
        return {
            "error": f"Analysis failed: {str(e)}"
        }


@app.post("/ask")
async def ask(question_req: QuestionRequest):
    """Ask a question about the uploaded contract"""
    try:
        prompt_text = question_req.question.strip()

        if not prompt_text:
            return {
                "error": "Question is required."
            }

        if not last_contract_text.strip():
            return {
                "error": "Upload a contract before asking questions."
            }

        answer = answer_question(last_contract_text, prompt_text)

        return {
            "answer": answer
        }
    except Exception as e:
        return {
            "error": f"Failed to answer question: {str(e)}"
        }


# Mount static files to serve frontend
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

