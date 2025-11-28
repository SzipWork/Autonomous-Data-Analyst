# app/agents/cleaning_agent.py
import pandas as pd

class CleaningAgent:
    def clean_dataset(self, df: pd.DataFrame):
        report = {}

        report["missing_values"] = df.isnull().sum().to_dict()
        report["duplicates_removed"] = int(df.duplicated().sum())

        df = df.drop_duplicates()

        return df, report
