const width = 932;
const height = 932;
const baseColor = d3.scaleOrdinal(d3.schemeCategory10);

const apparitionTypes = ["Ghost", "Spirit", "Orb", "Unknown", "Demon", "Evil Presence", "Poltergeist", "Phantom"];

const pack = data => d3.pack()
  .size([width, height])
  .padding(3)
  (d3.hierarchy(data)
    .sum(d => d.value));

// ✅ Always clear old content
const chartDiv = document.getElementById("chart");
if (chartDiv) {
  chartDiv.innerHTML = "";
}

const tooltip = d3.select("body")
  .append("div")
  .attr("class", "tooltip")
  .style("position", "absolute")
  .style("background", "white")
  .style("border", "1px solid #aaa")
  .style("padding", "6px 10px")
  .style("font-size", "13px")
  .style("pointer-events", "none")
  .style("visibility", "hidden")
  .style("box-shadow", "0px 2px 5px rgba(0,0,0,0.2)")
  .style("border-radius", "4px");

d3.json("/data/treemap.json").then(data => {
  const root = pack(data);

  const svg = d3.select("#chart")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [0, 0, width, height])
    .attr("style", "width: 100%; height: auto; height: intrinsic;");

  const node = svg.selectAll("g")
    .data(root.descendants().filter(d => d.data.value > 5 || d.children))
    .join("g")
    .attr("transform", d => `translate(${d.x},${d.y})`);

  node.each(function(d) {
    const g = d3.select(this);
    if (d.children) {
      g.append("circle")
        .attr("r", d.r)
        .attr("fill", baseColor(d.data.name));
    } else {
      const parentColor = d.parent ? baseColor(d.parent.data.name) : "#ccc";
      const lighterColor = d3.color(parentColor).brighter(1);

      if (d.data.name && d.data.name.includes(",")) {
        g.append("circle")
          .attr("r", d.r)
          .attr("fill", lighterColor)
          .attr("stroke", parentColor)
          .attr("stroke-width", 2)
          .attr("stroke-dasharray", "4 2"); // dashed outline
      } else {
        g.append("circle")
          .attr("r", d.r)
          .attr("fill", lighterColor)
          .attr("stroke", "#fff")
          .attr("stroke-width", 1);
      }
    }
  });

  node.on("mouseover", (event, d) => {
      tooltip
        .style("visibility", "visible")
        .html(`<strong>${d.data.name}</strong><br/>${d.data.value ? d.data.value + " sightings" : "Apparition Type"}`);
    })
    .on("mousemove", (event) => {
      tooltip
        .style("top", (event.pageY - 10) + "px")
        .style("left", (event.pageX + 10) + "px");
    })
    .on("mouseout", () => {
      tooltip.style("visibility", "hidden");
    });

  node.append("text")
    .filter(d => (d.children && d.r > 80) || (!d.children && d.data.value > 10))
    .style("text-anchor", "middle")
    .style("font-size", d => d.children ? "14px" : "8px")
    .attr("dy", "0.3em")
    .text(d => d.data.name);
});
