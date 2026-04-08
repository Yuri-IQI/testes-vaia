const API_URL = "http://127.0.0.1:8000/generate";

const form = document.getElementById("chart-form");
const fileInput = document.getElementById("dataset-file");
const promptInput = document.getElementById("prompt");
const statusElement = document.getElementById("status");
const chartElement = document.getElementById("chart");
const specOutput = document.getElementById("spec-output");
const dataOutput = document.getElementById("data-output");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const file = fileInput.files[0];
    const prompt = promptInput.value.trim();

    if (!file) {
        setStatus("Select a CSV file before generating a chart.", true);
        return;
    }

    if (!prompt) {
        setStatus("Type a prompt before generating a chart.", true);
        return;
    }

    setStatus("Generating chart...");
    chartElement.innerHTML = "";

    try {
        const csvText = await file.text();
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                prompt,
                csv_text: csvText,
                filename: file.name,
            }),
        });

        const payload = await response.json();
        if (!response.ok) {
            throw new Error(payload.detail || "The API request failed.");
        }

        renderChart(payload.spec, payload.records);
        specOutput.textContent = JSON.stringify(payload.spec, null, 2);
        dataOutput.textContent = JSON.stringify(payload.records, null, 2);

        const warningSuffix = payload.warnings.length ? ` Warnings: ${payload.warnings.join(" | ")}` : "";
        setStatus(`Rendered with source: ${payload.source}.${warningSuffix}`);
    } catch (error) {
        setStatus(`Error: ${error.message}`, true);
        specOutput.textContent = "No visualization spec available.";
        dataOutput.textContent = "No aggregated data available.";
    }
});


function setStatus(message, isError = false) {
    statusElement.textContent = message;
    statusElement.style.color = isError ? "#b91c1c" : "#475569";
}


function normalizeRecords(spec, records) {
    const dimensionKey = spec.data.dimension;
    const metricKey = spec.data.metric;
    const colorKey = spec.data.color;

    return records.map((record) => ({
        ...record,
        __dimension: String(record[dimensionKey]),
        __metric: Number(record[metricKey]),
        __color: colorKey ? String(record[colorKey]) : null,
    }));
}


function renderChart(spec, records) {
    const data = normalizeRecords(spec, records);
    const width = 860;
    const height = 460;

    if (spec.type === "pie") {
        renderPieChart(spec, data, width, height);
        return;
    }

    if (spec.type === "bar") {
        renderBarChart(spec, data, width, height);
        return;
    }

    renderLineChart(spec, data, width, height);
}


function createBaseSvg(title, width, height) {
    const svg = d3
        .select(chartElement)
        .append("svg")
        .attr("viewBox", `0 0 ${width} ${height}`)
        .attr("role", "img");

    svg.append("text")
        .attr("x", width / 2)
        .attr("y", 30)
        .attr("text-anchor", "middle")
        .attr("font-size", 22)
        .attr("font-weight", 700)
        .text(title);

    return svg;
}


function renderBarChart(spec, data, width, height) {
    const margin = { top: 60, right: 30, bottom: 70, left: 70 };
    const svg = createBaseSvg(spec.title, width, height);
    const dimensionValues = [...new Set(data.map((item) => item.__dimension))];
    const y = d3.scaleLinear()
        .domain([0, d3.max(data, (item) => item.__metric)]).nice()
        .range([height - margin.bottom, margin.top]);

    const yGrid = d3.axisLeft(y)
        .tickSize(-(width - margin.left - margin.right))
        .tickFormat(() => "");

    svg.append("g")
        .attr("transform", `translate(${margin.left},0)`)
        .call(yGrid)
        .attr("color", "#dbe3f0");

    if (spec.data.color) {
        const colorValues = [...new Set(data.map((item) => item.__color))];
        const x0 = d3.scaleBand()
            .domain(dimensionValues)
            .range([margin.left, width - margin.right])
            .padding(0.16);
        const x1 = d3.scaleBand()
            .domain(colorValues)
            .range([0, x0.bandwidth()])
            .padding(0.08);
        const colorScale = d3.scaleOrdinal()
            .domain(colorValues)
            .range(["#2563eb", "#0f766e", "#f59e0b", "#dc2626", "#7c3aed", "#ea580c"]);

        svg.append("g")
            .selectAll("rect")
            .data(data)
            .join("rect")
            .attr("x", (item) => x0(item.__dimension) + x1(item.__color))
            .attr("y", (item) => y(item.__metric))
            .attr("width", x1.bandwidth())
            .attr("height", (item) => y(0) - y(item.__metric))
            .attr("rx", 8)
            .attr("fill", (item) => colorScale(item.__color));

        renderLegend(svg, colorValues, colorScale, width - margin.right - 180, margin.top - 24);

        svg.append("g")
            .attr("transform", `translate(0,${height - margin.bottom})`)
            .call(d3.axisBottom(x0));
    } else {
        const x = d3.scaleBand()
            .domain(dimensionValues)
            .range([margin.left, width - margin.right])
            .padding(0.2);

        svg.append("g")
            .selectAll("rect")
            .data(data)
            .join("rect")
            .attr("x", (item) => x(item.__dimension))
            .attr("y", (item) => y(item.__metric))
            .attr("width", x.bandwidth())
            .attr("height", (item) => y(0) - y(item.__metric))
            .attr("rx", 10)
            .attr("fill", "#2563eb");

        svg.append("g")
            .attr("transform", `translate(0,${height - margin.bottom})`)
            .call(d3.axisBottom(x));
    }

    svg.append("g")
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y));
}


function renderLineChart(spec, data, width, height) {
    const margin = { top: 60, right: 40, bottom: 70, left: 70 };
    const svg = createBaseSvg(spec.title, width, height);
    const dimensionValues = [...new Set(data.map((item) => item.__dimension))];
    const x = d3.scalePoint()
        .domain(dimensionValues)
        .range([margin.left, width - margin.right])
        .padding(0.5);
    const y = d3.scaleLinear()
        .domain([0, d3.max(data, (item) => item.__metric)]).nice()
        .range([height - margin.bottom, margin.top]);

    const yGrid = d3.axisLeft(y)
        .tickSize(-(width - margin.left - margin.right))
        .tickFormat(() => "");

    svg.append("g")
        .attr("transform", `translate(${margin.left},0)`)
        .call(yGrid)
        .attr("color", "#dbe3f0");

    const line = d3.line()
        .x((item) => x(item.__dimension))
        .y((item) => y(item.__metric));

    if (spec.data.color) {
        const grouped = d3.group(data, (item) => item.__color);
        const colorValues = [...grouped.keys()];
        const colorScale = d3.scaleOrdinal()
            .domain(colorValues)
            .range(["#2563eb", "#0f766e", "#f59e0b", "#dc2626", "#7c3aed", "#ea580c"]);

        grouped.forEach((groupData, groupName) => {
            svg.append("path")
                .datum(groupData)
                .attr("fill", "none")
                .attr("stroke", colorScale(groupName))
                .attr("stroke-width", 3)
                .attr("d", line);

            svg.append("g")
                .selectAll(`circle-${groupName}`)
                .data(groupData)
                .join("circle")
                .attr("cx", (item) => x(item.__dimension))
                .attr("cy", (item) => y(item.__metric))
                .attr("r", 4.5)
                .attr("fill", colorScale(groupName));
        });

        renderLegend(svg, colorValues, colorScale, width - margin.right - 180, margin.top - 24);
    } else {
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
            .attr("cx", (item) => x(item.__dimension))
            .attr("cy", (item) => y(item.__metric))
            .attr("r", 4.5)
            .attr("fill", "#0f766e");
    }

    svg.append("g")
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x));

    svg.append("g")
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y));
}


function renderPieChart(spec, data, width, height) {
    const radius = Math.min(width, height) / 2 - 56;
    const svg = createBaseSvg(spec.title, width, height);
    const group = svg
        .append("g")
        .attr("transform", `translate(${width / 2}, ${height / 2 + 18})`);

    const colorScale = d3.scaleOrdinal()
        .domain(data.map((item) => item.__dimension))
        .range(["#2563eb", "#0f766e", "#f59e0b", "#dc2626", "#7c3aed", "#ea580c"]);

    const pie = d3.pie().value((item) => item.__metric);
    const arc = d3.arc().innerRadius(58).outerRadius(radius);
    const labelArc = d3.arc().innerRadius(radius * 0.75).outerRadius(radius * 0.75);

    group.selectAll("path")
        .data(pie(data))
        .join("path")
        .attr("d", arc)
        .attr("fill", (item) => colorScale(item.data.__dimension))
        .attr("stroke", "#ffffff")
        .attr("stroke-width", 2);

    group.selectAll("text")
        .data(pie(data))
        .join("text")
        .attr("transform", (item) => `translate(${labelArc.centroid(item)})`)
        .attr("text-anchor", "middle")
        .attr("font-size", 12)
        .attr("font-weight", 700)
        .text((item) => item.data.__dimension);
}


function renderLegend(svg, values, colorScale, x, y) {
    const legend = svg.append("g").attr("transform", `translate(${x}, ${y})`);

    values.forEach((value, index) => {
        const row = legend.append("g").attr("transform", `translate(0, ${index * 22})`);
        row.append("rect")
            .attr("width", 12)
            .attr("height", 12)
            .attr("rx", 3)
            .attr("fill", colorScale(value));
        row.append("text")
            .attr("x", 18)
            .attr("y", 10)
            .attr("font-size", 12)
            .text(value);
    });
}
