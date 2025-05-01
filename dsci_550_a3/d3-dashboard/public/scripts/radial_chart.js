console.log("✅ radial_chart.js is running!");

const width = 928, height = width;
const innerRadius = 180;
const outerRadius = width / 2 - 40;
const capDistance = 4000;

const svg = d3.select("svg")
  .attr("width", width)
  .attr("height", height)
  .attr("viewBox", [-width / 2, -height / 2, width, height])
  .style("font", "10px sans-serif");

const tooltip = d3.select("body").append("div")
  .attr("class", "tooltip")
  .style("position", "absolute")
  .style("background", "rgba(255,255,255,0.95)")
  .style("padding", "8px")
  .style("border", "1px solid #999")
  .style("border-radius", "4px")
  .style("pointer-events", "none")
  .style("font", "12px sans-serif")
  .style("z-index", "10")
  .style("visibility", "hidden");

let activeReligion = null;

d3.json("/data/radial_data.json").then(data => {
  const apparitionTypes = [...new Set(data.flatMap(d => Object.keys(d.apparitions)))];

  const mutedRainbow = [
    "#a6cee3", "#1f78b4", "#b2df8a", "#33a02c",
    "#fac8e3", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6"
  ];
  const color = d3.scaleOrdinal(apparitionTypes, mutedRainbow);

  data.sort((a, b) => a.median_distance - b.median_distance);

  const angle = d3.scaleBand()
    .domain(data.map(d => d.religion))
    .range([0, 2 * Math.PI])
    .align(0);

  const radius = d3.scaleLinear()
    .domain([0, capDistance])
    .range([innerRadius, outerRadius]);

  const customLabelMap = {
    "unitarian_universalist": "UU",
    "christian;presbyterian": "Presb",
    "religious_science": "Rel. Science"
  };

  const arc = d3.arc()
    .innerRadius(d => radius(d.y0))
    .outerRadius(d => radius(d.y1))
    .startAngle(d => angle(d.religion))
    .endAngle(d => angle(d.religion) + angle.bandwidth())
    .padAngle(0.01)
    .padRadius(innerRadius);

  const allBarsGroup = svg.append("g").attr("class", "bar-group");

  const getStackedByReligion = () => {
    const grouped = {};
    data.forEach(d => {
      const base = Math.min(d.median_distance, capDistance);
      let prev = 0;

      apparitionTypes.forEach(type => {
        const pct = d.apparitions[type] || 0;
        let y0 = (base * prev) / 100;
        let y1 = (base * (prev + pct)) / 100;
        if (activeReligion === d.religion) {
          const scale = capDistance / base;
          y0 *= scale;
          y1 *= scale;
        }
        grouped[d.religion] ??= [];
        grouped[d.religion].push({ religion: d.religion, type, data: d, y0, y1 });
        prev += pct;
      });
    });
    return Object.entries(grouped);
  };

  function updateChart() {
    const groupedData = getStackedByReligion();

    const religionGroups = allBarsGroup.selectAll(".bar-group-religion")
      .data(groupedData, d => d[0]);

    religionGroups.exit().transition().duration(600).style("opacity", 0).remove();

    const merged = religionGroups.enter()
      .append("g")
      .attr("class", "bar-group-religion")
      .merge(religionGroups);

    merged.transition().duration(800)
      .style("opacity", d => (activeReligion && d[0] !== activeReligion) ? 0 : 1);

    merged.each(function ([religion, segments]) {
      const group = d3.select(this);
      const paths = group.selectAll("path").data(segments, d => d.type);

      paths.join(
        enter => enter.append("path")
          .attr("fill", d => color(d.type))
          .attr("d", arc)
          .style("cursor", "pointer")
          .on("click", (event, d) => {
            activeReligion = activeReligion === d.religion ? null : d.religion;
            updateChart();
            event.stopPropagation();
          })
          .on("mouseover", (event, d) => {
            const dist = Math.round(d.data.median_distance);
            const isCapped = dist > capDistance;
            tooltip.html(`
              <strong>Religion:</strong> ${d.data.religion}<br>
              <strong>Apparition:</strong> ${d.type}<br>
              <strong>Percentage:</strong> ${(d.data.apparitions[d.type] || 0).toFixed(1)}%<br>
              <strong>Median Distance:</strong> ${dist} m${isCapped ? " (capped)" : ""}
            `).style("visibility", "visible");
          })
          .on("mousemove", e => tooltip.style("top", `${e.pageY - 10}px`).style("left", `${e.pageX + 15}px`))
          .on("mouseout", () => tooltip.style("visibility", "hidden")),
        update => update.transition().duration(800).attr("d", arc)
      );
    });

    svg.selectAll(".distance-label")
      .transition().duration(400)
      .style("opacity", activeReligion ? 0 : 1);
  }

  updateChart();
  svg.on("click", () => { activeReligion = null; updateChart(); });

  svg.append("g")
    .attr("text-anchor", "middle")
    .selectAll("g")
    .data(angle.domain())
    .join("g")
    .attr("transform", d => `
      rotate(${(angle(d) + angle.bandwidth() / 2) * 180 / Math.PI - 90})
      translate(${innerRadius},0)
    `)
    .call(g => g.append("line").attr("x2", -4).attr("stroke", "#000"))
    .call(g => g.append("text")
      .attr("transform", d =>
        (angle(d) + angle.bandwidth() / 2 + Math.PI / 2) % (2 * Math.PI) < Math.PI
          ? "rotate(90)translate(0,12)"
          : "rotate(-90)translate(0,-6)")
      .style("font-size", "10px")
      .text(d => customLabelMap[d] || (d.length > 14 ? d.slice(0, 12) + "…" : d))
      .append("title").text(d => d));

  svg.append("g")
    .attr("class", "radial-axis")
    .attr("text-anchor", "middle")
    .call(g => g.selectAll("g")
      .data(radius.ticks(4).slice(1))
      .join("g")
      .attr("fill", "none")
      .call(g => g.append("circle")
        .attr("stroke", "#999")
        .attr("stroke-opacity", 0.5)
        .attr("r", radius))
      .call(g => g.append("text")
        .attr("class", "distance-label")
        .attr("y", d => -radius(d))
        .attr("dy", "0.35em")
        .attr("fill", "#000")
        .text(d => `${Math.round(d)} m`)));

  svg.append("g")
    .attr("class", "legend")
    .attr("text-anchor", "start")
    .attr("transform", `translate(0, 0)`)
    .selectAll("g")
    .data(apparitionTypes)
    .join("g")
    .attr("transform", (d, i, nodes) => `translate(-40, ${-nodes.length * 10 + i * 20})`)
    .call(g => g.append("rect")
      .attr("width", 14)
      .attr("height", 14)
      .attr("fill", d => color(d)))
    .call(g => g.append("text")
      .attr("x", 20)
      .attr("y", 7)
      .attr("dy", "0.35em")
      .style("font-size", "12px")
      .text(d => d));
});
