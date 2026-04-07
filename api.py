from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from chart_pipeline import ChartPipeline
from examples import CHART_EXAMPLES


app = FastAPI(
    title="VAIA API",
    description="API for chart generation from natural language prompts.",
    version="1.0.0",
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
    prompt: str = Field(..., min_length=3, description="Natural language chart prompt.")


class GenerateResponse(BaseModel):
    chart: dict
    javascript: str
    source: str
    raw_response: str = ""
    warnings: list[str] = Field(default_factory=list)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/examples")
def examples() -> dict[str, list[str]]:
    return {"examples": [example["request"] for example in CHART_EXAMPLES]}


@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest) -> GenerateResponse:
    prompt = request.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    result = pipeline.generate_d3_payload(prompt)

    return GenerateResponse(
        chart=result.chart.to_dict(),
        javascript=result.javascript,
        source=result.source,
        raw_response=result.raw_response,
        warnings=result.warnings,
    )
