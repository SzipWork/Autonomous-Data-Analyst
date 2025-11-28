# app/agents/analysis_agent.py
import pandas as pd

class AnalysisAgent:
    def perform_eda(self, df: pd.DataFrame):
        summary = df.describe(include="all").to_dict()
        dtypes = df.dtypes.astype(str).to_dict()

        return {
            "summary_statistics": summary,
            "column_types": dtypes,
            "row_count": len(df),
            "column_count": len(df.columns),
        }

    def detect_anomalies(self, df: pd.DataFrame):
        anomalies = {}

        for col in df.select_dtypes(include=["number"]).columns:
            mean = df[col].mean()
            std = df[col].std()
            if std > 0:
                anomalies[col] = (df[col] > mean + 3*std).sum()

        return anomalies
