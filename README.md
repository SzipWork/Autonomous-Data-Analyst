# Autonomous-Data-Analyst
An intelligent data analysis platform that automates the entire data analysis workflow using AI agents.

## Key Features
- **Multi-Agent Architecture:** Uses specialized agents (CleaningAgent, AnalysisAgent, VisualizationAgent, ChatAgent, DataAnalysisCoordinator) to manage the data analysis workflow.
- **Data Quality Assurance:** Automatically identifies and removes duplicate rows, and reports on missing values.
- **Exploratory Data Analysis (EDA):** Generates summary statistics, column types, and dataset shape information.
- **Anomaly Detection:** Simple anomaly detection for numeric columns (values $> 3\sigma$ from the mean).
- **Visualization**: Recommends and generates a variety of plots (histograms, box plots, scatter plots, heatmaps, etc.) using pandas, matplotlib, and seaborn.
- **AI Contextual Chat:** Integrates the Gemini 2.5 Pro model (via ChatGoogleGenerativeAI) to answer user questions based only on the provided dataset's summary context.
- **Vector Database (ChromaDB):** Includes a VectorStore class for optional persistent memory and context retrieval (with a dictionary-based fallback).
- **Dockerized Deployment:** Uses docker-compose for easy, reproducible setup of both the FastAPI backend and Streamlit frontend.

## Prerequisites
- Docker and Docker Compose
- Google AI API Key

## Setup and Installation
Follow these steps to get the application running locally using Docker Compose.
 1. **Configure the API Key**
   Create a file named `.env` in the root directory and add your Google AI API key:
 `GOOGLE_API_KEY=YOUR_GEMINI_API_KEY_HERE`

 2. **Build and Run the Containers**
   From the root directory of the project, run the following command:
   `docker-compose up --build`
    This command will:
    1. Build the Docker images for the backend (FastAPI) and frontend (Streamlit).
    2. Start the services on the analyst-network.
 
 3. **Access the Application**
   The services will be accessible via your local machine's ports:
    - Frontend (Streamlit UI): http://localhost:8501
    - Backend (FastAPI/API): http://localhost:8000

## Docker Compose Configuration
- The `docker-compose.yml` defines the networking and service dependencies:

- `backend` (FastAPI): Exposes port 8000. The frontend uses the internal service name http://backend:8000 to communicate.

- `frontend` (Streamlit): Exposes port 8501. It waits for the backend to start using `depends_on: backend`.

- `analyst-network`: Ensures both services can communicate using their service names.
