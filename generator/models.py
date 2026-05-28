from dataclasses import dataclass, field
from typing import Any
import pandas as pd

@dataclass
class VisualizationDataSpec:
    dimension: str | None
    metric: str
    metric_secondary: str | None
    aggregation: str | None
    color: str | None = None
    filters: dict[str, list[str]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "dimension": self.dimension,
            "metric": self.metric,
            "aggregation": self.aggregation,
        }
        
        if self.metric_secondary:
            payload["metric_secondary"] = self.metric_secondary

        if self.color:
            payload["color"] = self.color
        
        if self.filters:
            payload["filters"] = self.filters

        return payload

@dataclass
class VisualizationRenderOptions:
    log_scale_y: bool = False
    show_trend_line: bool = False
    nbins: int = 40
    top_n: int | None = None 

@dataclass
class VisualizationSpec:
    chart_type: str
    data: VisualizationDataSpec
    title: str
    description: str
    explanation: str
    render_options: VisualizationRenderOptions = field(default_factory=VisualizationRenderOptions)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "VisualizationSpec":
        data = payload["data"]
        raw_options = payload.get("render_options")

        if isinstance(raw_options, VisualizationRenderOptions):
            options = raw_options
        elif isinstance(raw_options, dict):
            options = VisualizationRenderOptions(**{
                k: v for k, v in raw_options.items()
                if k in VisualizationRenderOptions.__dataclass_fields__
            })
        else:
            options = VisualizationRenderOptions()

        return cls(
            chart_type=payload["type"],
            data=VisualizationDataSpec(
                dimension=data["dimension"],
                metric=data["metric"],
                aggregation=data.get("aggregation"),
                color=data.get("color"),
                metric_secondary=data.get("metric_secondary"),
                filters=data.get("filters")
            ),
            title=payload["title"],
            description=payload["description"],
            explanation=payload["explanation"],
            render_options=options,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.chart_type,
            "data": self.data.to_dict(),
            "title": self.title,
            "description": self.description,
            "explanation": self.explanation,
            "render_options": self.render_options
        }
