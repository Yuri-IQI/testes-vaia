import pandas as pd
import plotly.express as px
from generator.models import VisualizationSpec
import plotly.graph_objects as go
from pandas.api.types import is_datetime64_any_dtype

def build_plotly_figure(plot_frame: pd.DataFrame, spec: VisualizationSpec) -> go.Figure:
    dimension = spec.data.dimension
    metric = spec.data.metric
    color = spec.data.color

    if spec.chart_type == "bar":
        figure = px.bar(
            plot_frame,
            x=dimension,
            y=metric,
            color=color,
            barmode="group",
            title=spec.title,
        )
    elif spec.chart_type == "line":
        figure = px.line(
            plot_frame,
            x=dimension,
            y=metric,
            color=color,
            markers=True,
            title=spec.title,
        )
    elif spec.chart_type == "scatter":
        figure = px.scatter(
            plot_frame,
            x=spec.data.dimension,
            y=spec.data.metric,
            color=spec.data.color,
            title=spec.title,
    )
    elif spec.chart_type == "histogram":
        figure = px.histogram(
            plot_frame,
            x=spec.data.metric,
            color=spec.data.color,
            nbins=40,
            title=spec.title,
        )
    elif spec.chart_type == "box":
        figure = px.box(
            plot_frame,
            x=spec.data.dimension,
            y=spec.data.metric,
            color=spec.data.color,
            title=spec.title,
        )
    elif spec.chart_type == "pie":
        figure = px.pie(
            plot_frame,
            names=dimension,
            values=metric,
            title=spec.title,
            hole=0.25,
        )
    else:
        raise Exception("Unrecognized chart type: " + spec.chart_type)

    figure.update_layout(template="plotly_white", margin={"l": 24, "r": 24, "t": 60, "b": 24})
    return figure

def build_matplotlib_figure(plot_frame: pd.DataFrame, spec: VisualizationSpec):
    import matplotlib.pyplot as plt

    chart_type = spec.chart_type
    dimension = spec.data.dimension
    metric = spec.data.metric
    color = spec.data.color
    nbins = getattr(spec.render_options, "nbins", None) or 40
    log_scale_y = getattr(spec.render_options, "log_scale_y", False)
    show_trend_line = getattr(spec.render_options, "show_trend_line", False)

    fig, ax = plt.subplots(figsize=(10, 6))

    if chart_type == "histogram":
        plot_frame[metric].plot(kind="hist", bins=nbins, ax=ax, color="#2563eb", edgecolor="white")
        if log_scale_y:
            ax.set_yscale("log")
        ax.set_xlabel(metric)
        ax.set_ylabel("Frequency")

    elif chart_type == "box":
        if color:
            groups = [group[metric].dropna() for _, group in plot_frame.groupby(dimension)]
            labels = [str(k) for k, _ in plot_frame.groupby(dimension)]
            ax.boxplot(groups, labels=labels)
        else:
            plot_frame.boxplot(column=metric, by=dimension, ax=ax)
            plt.suptitle("")
        ax.set_xlabel(dimension)
        ax.set_ylabel(metric)

    elif chart_type == "scatter":
        if color:
            for group_name, group in plot_frame.groupby(color):
                ax.scatter(group[dimension], group[metric], label=str(group_name), alpha=0.6)
            ax.legend(title=color)
        else:
            ax.scatter(plot_frame[dimension], plot_frame[metric], alpha=0.6, color="#2563eb")
        if show_trend_line:
            import numpy as np
            x = pd.to_numeric(plot_frame[dimension], errors="coerce").dropna()
            y = pd.to_numeric(plot_frame[metric], errors="coerce").dropna()
            if len(x) == len(y) and len(x) > 1:
                m, b = np.polyfit(x, y, 1)
                ax.plot(x, m * x + b, color="#ef4444", linewidth=1.5, linestyle="--", label="Trend")
                ax.legend()
        if log_scale_y:
            ax.set_yscale("log")
        ax.set_xlabel(dimension)
        ax.set_ylabel(metric)

    elif chart_type == "bar":
        if color:
            pivot = plot_frame.pivot(index=dimension, columns=color, values=metric).fillna(0)
            pivot.plot(kind="bar", ax=ax)
            ax.legend(title=color)
        else:
            ax.bar(plot_frame[dimension].astype(str), plot_frame[metric], color="#2563eb")
        if log_scale_y:
            ax.set_yscale("log")
        ax.set_xlabel(dimension)
        ax.set_ylabel(metric)

    elif chart_type == "line":
        if color:
            for group_name, group in plot_frame.groupby(color):
                group = group.sort_values(dimension)
                ax.plot(group[dimension], group[metric], marker="o", linewidth=2.2, label=str(group_name))
            ax.legend(title=color)
        else:
            ax.plot(plot_frame[dimension], plot_frame[metric], marker="o", linewidth=2.4, color="#0f766e")
        if log_scale_y:
            ax.set_yscale("log")
        if is_datetime64_any_dtype(plot_frame[dimension]):
            fig.autofmt_xdate()
        ax.set_xlabel(dimension)
        ax.set_ylabel(metric)

    elif chart_type == "pie":
        if dimension is None:
            raise ValueError("Pie chart requires a dimension column.")
        ax.pie(
            plot_frame[metric],
            labels=plot_frame[dimension].astype(str),
            autopct="%1.1f%%",
            startangle=90,
        )
        ax.axis("equal")

    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")

    ax.set_title(spec.title)
    ax.grid(alpha=0.25, axis="y") if chart_type in {"bar", "line", "scatter"} else None
    plt.tight_layout()
    return fig