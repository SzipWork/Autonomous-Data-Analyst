# app/models/schemas.py
from pydantic import BaseModel
from typing import List, Dict, Any

class AnalysisResponse(BaseModel):
    dataset_name: str
    analysis_report: Dict[str, Any]
    data_quality_report: Dict[str, Any]
    anomaly_report: Dict[str, Any]
    visualization_specs: List[Dict[str, Any]]
    generated_visualizations: List[str]
    summary_report: str
    cleaned_preview: List[Dict[str, Any]]
    dashboard_url: str | None = None
