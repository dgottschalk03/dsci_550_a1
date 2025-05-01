(function() {
    const width = 900;
    const height = 600;
    const margin = {top: 60, right: 30, bottom: 60, left: 220};
  
    // ✅ Clear old scatterplot content
    const scatterDiv = document.getElementById("scatterplot");
    if (scatterDiv) {
      scatterDiv.innerHTML = "";
    }
  
    const svg = d3.select("#scatterplot")
      .append("svg")
      .attr("width", width)
      .attr("height", height);
  
    const tooltip = d3.select("body").append("div")
      .attr("class", "tooltip")
      .style("opacity", 0);
  
    d3.json("/data/scatter_daylight_apparition_cleaned.json").then(function(data) {
      const x = d3.scaleLinear()
        .domain(d3.extent(data, d => d.Daylight_Duration_Hours))
        .range([margin.left, width - margin.right]);
  
      const y = d3.scalePoint()
        .domain([...new Set(data.map(d => d.Primary_Apparition_Type))].sort())
        .range([margin.top, height - margin.bottom])
        .padding(0.5);
  
      svg.append("g")
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x));
  
      svg.append("g")
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y));
  
      svg.append("line")
        .attr("x1", x(12))
        .attr("x2", x(12))
        .attr("y1", margin.top)
        .attr("y2", height - margin.bottom)
        .attr("stroke", "#aaa")
        .attr("stroke-dasharray", "4")
        .attr("stroke-width", 1.5);
  
      const points = svg.append("g")
        .selectAll("circle")
        .data(data)
        .join("circle")
        .attr("cx", d => x(d.Daylight_Duration_Hours))
        .attr("cy", d => y(d.Primary_Apparition_Type))
        .attr("r", d => d.Violent ? 5 : 3)
        .attr("fill", d => d.Violent ? "#e60000" : "#4A90E2")
        .attr("opacity", 0.7)
        .on("mouseover", (event, d) => {
          d3.select(event.currentTarget)
            .transition()
            .duration(150)
            .attr("r", 7)
            .attr("stroke", "white")
            .attr("stroke-width", 1.5);
  
          tooltip.transition()
            .duration(200)
            .style("opacity", .95);
          tooltip.html(`Apparition: <b>${d.Primary_Apparition_Type}</b><br/>Daylight: <b>${d.Daylight_Duration_Hours.toFixed(2)} hrs</b><br/>Violent: <b>${d.Violent ? "Yes" : "No"}</b>`)
            .style("left", (event.pageX + 10) + "px")
            .style("top", (event.pageY - 28) + "px");
        })
        .on("mouseout", (event, d) => {
          d3.select(event.currentTarget)
            .transition()
            .duration(150)
            .attr("r", d.Violent ? 5 : 3)
            .attr("stroke", "none");
  
          tooltip.transition()
            .duration(400)
            .style("opacity", 0);
        });
  
      const apparitionTypes = [...new Set(data.map(d => d.Primary_Apparition_Type))].sort();
      const select = d3.select("#apparitionSelect");
  
      apparitionTypes.forEach(type => {
        select.append("option").text(type).attr("value", type);
      });
  
      select.on("change", function(event) {
        const selected = this.value;
        points.style("display", d => selected === "All" || d.Primary_Apparition_Type === selected ? "" : "none");
      });
  
      d3.select("#resetButton").on("click", () => {
        select.property("value", "All");
        points.style("display", "");
      });
    });
  })();
  