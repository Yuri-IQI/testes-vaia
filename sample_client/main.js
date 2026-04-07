const API_URL = "http://127.0.0.1:8000/generate";

const form = document.getElementById("chart-form");
const promptInput = document.getElementById("prompt");
const statusElement = document.getElementById("status");
const chartElement = document.getElementById("chart");
const jsonOutput = document.getElementById("json-output");
const jsOutput = document.getElementById("js-output");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const prompt = promptInput.value.trim();
    if (!prompt) {
        setStatus("Type a prompt before generating a chart.", true);
        return;
    }

    setStatus("Generating chart...");
    chartElement.innerHTML = "";

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ prompt }),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText || "The API request failed.");
        }

        const payload = await response.json();
        renderChart(payload.chart);

        jsonOutput.textContent = JSON.stringify(payload.chart, null, 2);
        jsOutput.textContent = payload.javascript;
        setStatus(`Rendered with source: ${payload.source}`);
    } catch (error) {
        setStatus(`Error: ${error.message}`, true);
        jsonOutput.textContent = "No chart available.";
        jsOutput.textContent = "No JavaScript snippet available.";
    }
});


function setStatus(message, isError = false) {
    statusElement.textContent = message;
    statusElement.style.color = isError ? "#b91c1c" : "#475569";
}


function renderChart(chart) {
    const width = 760;
    const height = 420;
    const margin = { top: 56, right: 24, bottom: 64, left: 64 };
    const data = chart.labels.map((label, index) => ({
        label,
        value: Number(chart.values[index]),
    }));

    if (chart.type === "pie") {
        renderPieChart(chart, data, width, height);
        return;
    }

    const svg = d3
        .select(chartElement)
        .append("svg")
        .attr("viewBox", `0 0 ${width} ${height}`)
        .attr("role", "img");

    svg.append("text")
        .attr("x", width / 2)
        .attr("y", 32)
        .attr("text-anchor", "middle")
        .attr("font-size", 22)
        .attr("font-weight", 700)
        .text(chart.title);

    const x = chart.type === "bar"
        ? d3.scaleBand()
            .domain(data.map((item) => item.label))
            .range([margin.left, width - margin.right])
            .padding(0.2)
        : d3.scalePoint()
            .domain(data.map((item) => item.label))
            .range([margin.left, width - margin.right])
            .padding(0.5);

    const y = d3.scaleLinear()
        .domain([0, d3.max(data, (item) => item.value)]).nice()
        .range([height - margin.bottom, margin.top]);

    const xAxis = (group) =>
        group
            .attr("transform", `translate(0,${height - margin.bottom})`)
            .call(d3.axisBottom(x))
            .call((selection) => selection.selectAll("text").attr("font-size", 12));

    const yAxis = (group) =>
        group
            .attr("transform", `translate(${margin.left},0)`)
            .call(d3.axisLeft(y))
            .call((selection) => selection.selectAll("text").attr("font-size", 12));

    svg.append("g").call(xAxis);
    svg.append("g").call(yAxis);

    svg.append("g")
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y).tickSize(-(width - margin.left - margin.right)).tickFormat(() => ""))
        .attr("color", "#cbd5e1");

    if (chart.type === "bar") {
        svg.append("g")
            .selectAll("rect")
            .data(data)
            .join("rect")
            .attr("x", (item) => x(item.label))
            .attr("y", (item) => y(item.value))
            .attr("width", x.bandwidth())
            .attr("height", (item) => y(0) - y(item.value))
            .attr("rx", 10)
            .attr("fill", "#2563eb");
        return;
    }

    const line = d3.line()
        .x((item) => x(item.label))
        .y((item) => y(item.value));

    svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "#0f766e")
        .attr("stroke-width", 3)
        .attr("d", line);

    svg.append("g")
        .selectAll("circle")
        .data(data)
        .join("circle")
        .attr("cx", (item) => x(item.label))
        .attr("cy", (item) => y(item.value))
        .attr("r", 5)
        .attr("fill", "#0f766e");
}


function renderPieChart(chart, data, width, height) {
    const radius = Math.min(width, height) / 2 - 40;
    const svg = d3
        .select(chartElement)
        .append("svg")
        .attr("viewBox", `0 0 ${width} ${height}`)
        .attr("role", "img");

    svg.append("text")
        .attr("x", width / 2)
        .attr("y", 32)
        .attr("text-anchor", "middle")
        .attr("font-size", 22)
        .attr("font-weight", 700)
        .text(chart.title);

    const group = svg
        .append("g")
        .attr("transform", `translate(${width / 2}, ${height / 2 + 12})`);

    const color = d3.scaleOrdinal()
        .domain(data.map((item) => item.label))
        .range(["#2563eb", "#0f766e", "#f59e0b", "#dc2626", "#7c3aed", "#ea580c"]);

    const pie = d3.pie().value((item) => item.value);
    const arc = d3.arc().innerRadius(55).outerRadius(radius);
    const labelArc = d3.arc().innerRadius(radius * 0.75).outerRadius(radius * 0.75);

    group.selectAll("path")
        .data(pie(data))
        .join("path")
        .attr("d", arc)
        .attr("fill", (item) => color(item.data.label))
        .attr("stroke", "#ffffff")
        .attr("stroke-width", 2);

    group.selectAll("text")
        .data(pie(data))
        .join("text")
        .attr("transform", (item) => `translate(${labelArc.centroid(item)})`)
        .attr("text-anchor", "middle")
        .attr("font-size", 12)
        .attr("font-weight", 700)
        .text((item) => item.data.label);
}
