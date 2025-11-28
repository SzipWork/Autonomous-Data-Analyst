# app/agents/coordinator.py
import pandas as pd
from app.agents.analysis_agent import AnalysisAgent
from app.agents.cleaning_agent import CleaningAgent
from app.agents.visualization_agent import VisualizationAgent

class DataAnalysisCoordinator:
    def __init__(self):
        self.analysis_agent = AnalysisAgent()
        self.cleaning_agent = CleaningAgent()
        self.visualization_agent = VisualizationAgent()

    def orchestrate_analysis(self, df: pd.DataFrame, dataset_name: str):
        state = {"dataset_name": dataset_name}

        df, clean_report = self.cleaning_agent.clean_dataset(df)
        state["data_quality_report"] = clean_report

        analysis = self.analysis_agent.perform_eda(df)
        state["analysis_report"] = analysis

        anomalies = self.analysis_agent.detect_anomalies(df)
        state["anomaly_report"] = anomalies

        viz_specs = self.visualization_agent.recommend_visualizations(df, analysis)
        images = self.visualization_agent.generate_visualizations(df, viz_specs)

        state["visualization_specs"] = viz_specs
        state["generated_visualizations"] = images
        state["cleaned_preview"] = df.head().to_dict(orient="records")

        state["summary_report"] = f"Dataset «{dataset_name}» analyzed successfully with {len(images)} charts."

        return state
