# app/agents/visualization_agent.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

class VisualizationAgent:

    def recommend_visualizations(self, df: pd.DataFrame, analysis_report):
        specs = []

        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

        # 1. Histogram for numeric columns
        for col in numeric_cols:
            specs.append({"type": "histogram", "column": col}), 

        # 2. Box plot for numeric columns
        for col in numeric_cols:
            specs.append({"type": "boxplot", "column": col})

        # 3. Line plot for time/index trends
        if len(numeric_cols) > 0:
            specs.append({"type": "lineplot", "columns": numeric_cols})

        # 4. Bar chart for categorical columns
        for col in categorical_cols:
            specs.append({"type": "barchart", "column": col})

        # 5. Scatter plot for pairs of numeric columns
        if len(numeric_cols) >= 2:
            for i in range(len(numeric_cols) - 1):
                specs.append({
                    "type": "scatter",
                    "x": numeric_cols[i],
                    "y": numeric_cols[i + 1]
                })

        # 6. Correlation heatmap
        if len(numeric_cols) >= 2:
            specs.append({"type": "heatmap", "columns": numeric_cols})

        return specs


    def generate_visualizations(self, df: pd.DataFrame, specs):
        images = []

        for spec in specs:
            plt.figure(figsize=(6, 4))

            # =========================
            # HISTOGRAM
            # =========================
            if spec["type"] == "histogram":
                col = spec["column"]
                df[col].hist()
                plt.title(f"Histogram: {col}")

            # =========================
            # BOXPLOT
            # =========================
            elif spec["type"] == "boxplot":
                col = spec["column"]
                sns.boxplot(x=df[col])
                plt.title(f"Box Plot: {col}")

            # =========================
            # LINE PLOT
            # =========================
            elif spec["type"] == "lineplot":
                cols = spec["columns"]
                df[cols].plot()
                plt.title("Line Plot of Numeric Columns")
                plt.legend(cols)

            # =========================
            # BAR CHART
            # =========================
            elif spec["type"] == "barchart":
                col = spec["column"]
                df[col].value_counts().plot(kind="bar")
                plt.title(f"Bar Chart: {col}")

            # =========================
            # SCATTER PLOT
            # =========================
            elif spec["type"] == "scatter":
                x = spec["x"]
                y = spec["y"]
                plt.scatter(df[x], df[y])
                plt.xlabel(x)
                plt.ylabel(y)
                plt.title(f"Scatter Plot: {x} vs {y}")

            # =========================
            # HEATMAP
            # =========================
            elif spec["type"] == "heatmap":
                cols = spec["columns"]
                corr = df[cols].corr()
                sns.heatmap(corr, annot=True, cmap="coolwarm")
                plt.title("Correlation Heatmap")

            # Save the plot to Base64
            buffer = BytesIO()
            plt.savefig(buffer, format="png", bbox_inches="tight")
            buffer.seek(0)
            img_b64 = base64.b64encode(buffer.read()).decode("utf-8")
            plt.close()

            images.append(img_b64)

        return images
