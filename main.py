from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import os
from datetime import datetime

from app.agents.coordinator import DataAnalysisCoordinator
from app.models.schemas import AnalysisResponse
from app.database.vector_db import VectorStore
from app.utils.gemini_client import GeminiClient

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="Autonomous Data Analyst",
    version="1.0.0",
    description="Upload CSV → Auto Analysis → Chat with Data"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

coordinator = DataAnalysisCoordinator()
vector_db = VectorStore()
gemini = GeminiClient()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -------------------------
# Helper function to convert numpy types
# -------------------------
def convert_numpy(obj):
    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(i) for i in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj


# -------------------------
# Routes
# -------------------------
@app.get("/")
async def home():
    return {
        "message": "Autonomous Data Analyst API is running",
        "upload_csv": "/analyze-csv",
        "chat_with_data": "/ask",
        "docs": "/docs"
    }


@app.post("/analyze-csv", response_model=AnalysisResponse)
async def analyze_csv(file: UploadFile = File(...)):
    try:
        # save file
        filename = f"{datetime.now().timestamp()}_{file.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as f:
            f.write(await file.read())

        # read CSV
        try:
            df = pd.read_csv(filepath)
        except Exception:
            raise HTTPException(400, "Unable to parse CSV. Ensure it's valid.")

        if df.empty:
            raise HTTPException(400, "CSV file contains no data.")

        # perform analysis
        result = coordinator.orchestrate_analysis(df, file.filename)

        # convert any numpy types to native Python
        result = convert_numpy(result)

        # store memory
        combined_context = (
            f"SUMMARY: {result['summary_report']}\n\n"
            f"EDA: {result['analysis_report']}\n\n"
            f"QUALITY: {result['data_quality_report']}\n\n"
            f"ANOMALIES: {result['anomaly_report']}"
        )
        vector_db.add_context(file.filename, combined_context)

        # dashboard placeholder
        result["dashboard_url"] = None

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/ask")
async def ask_question(query: str, dataset: str):
    try:
        # fetch dataset-specific context
        contexts = vector_db.search(dataset)

        if not contexts:
            return {"answer": "No relevant context found for this dataset."}

        merged_context = "\n\n".join(contexts)

        answer = gemini.ask(query, merged_context)
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok"}
