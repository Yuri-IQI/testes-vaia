from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from chart_pipeline import ChartPipeline
from chart_utils import load_csv_dataset
from examples import VISUALIZATION_EXAMPLES


PROJECT_DIR = Path(__file__).resolve().parent
SAMPLE_DATASET_PATH = PROJECT_DIR / "sample_data" / "sample_sales_data.csv"

app = FastAPI(
    title="VAIA Dataset API",
    description="API for dataset-based chart specification generation from natural language prompts.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = ChartPipeline()


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=3)
    csv_text: str = Field(..., min_length=1)
    filename: str = "uploaded.csv"


class GenerateResponse(BaseModel):
    spec: dict[str, Any]
    records: list[dict[str, Any]]
    source: str
    raw_response: str = ""
    warnings: list[str] = Field(default_factory=list)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/examples")
def examples() -> dict[str, list[str]]:
    return {"examples": [example["request"] for example in VISUALIZATION_EXAMPLES]}


@app.get("/sample-dataset")
def sample_dataset():
    if not SAMPLE_DATASET_PATH.exists():
        raise HTTPException(status_code=404, detail="Bundled sample dataset not found.")

    return FileResponse(
        SAMPLE_DATASET_PATH,
        media_type="text/csv",
        filename=SAMPLE_DATASET_PATH.name,
    )


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest) -> GenerateResponse:
    if not request.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV uploads are supported right now.")

    file_bytes = request.csv_text.encode("utf-8")
    if not file_bytes:
        raise HTTPException(status_code=400, detail="The uploaded CSV file is empty.")

    try:
        frame = load_csv_dataset(BytesIO(file_bytes))
        result = pipeline.generate_visualization(frame, request.prompt.strip())
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return GenerateResponse(
        spec=result.spec.to_dict(),
        records=result.frontend_records(),
        source=result.source,
        raw_response=result.raw_response,
        warnings=result.warnings,
    )
