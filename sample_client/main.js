document.body.addEventListener("htmx:afterRequest", function(evt) {

    if (evt.detail.xhr.responseURL.includes("/generate")) {

        const response = JSON.parse(evt.detail.xhr.responseText)

        renderChart(JSON.parse(response.code))

    }

})

function renderChart(code) {

    console.log("Received chart data:", code)

    const data = code.data
    const width = code.width || 600
    const height = code.height || 400
    const margin = code.margin || { top: 20, right: 20, bottom: 20, left: 20 }

    console.log("Rendering chart with data:", data)

    d3.select("#chart").selectAll("*").remove()

    const svg = d3.select("#chart")
        .append("svg")
        .attr("width", width)
        .attr("height", height)

    const x = d3.scaleBand()
        .domain(data.map(d => d.label))
        .range([margin.left, width - margin.right])
        .padding(0.2)

    const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.value)])
        .nice()
        .range([height - margin.bottom, margin.top])

    svg.selectAll("rect")
        .data(data)
        .enter()
        .append("rect")
        .attr("x", d => x(d.label))
        .attr("y", d => y(d.value))
        .attr("width", x.bandwidth())
        .attr("height", d => y(0) - y(d.value))
        .attr("fill", "#1f77b4")

    svg.append("g")
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x))

    svg.append("g")
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y))
}