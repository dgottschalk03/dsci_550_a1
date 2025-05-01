import React, { useEffect, useRef } from "react";
import * as d3 from "d3";
import * as topojson from "topojson-client";

export default function BubbleMap() {
  const svgRef = useRef(null);

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    const width = 960;
    const height = 700;

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

    svg.selectAll("*").remove(); // Clear previous renders
    svg
      .attr("width", width)
      .attr("height", height)
      .style("font", "10px sans-serif");

    const projection = d3.geoAlbersUsa()
      .scale(1200)
      .translate([width / 2, height / 2]);

    const path = d3.geoPath().projection(projection);
    const color = d3.scaleSequential(d3.interpolateReds).domain([0, 15000]);
    const size = d3.scaleSqrt().domain([1, 20]).range([2, 25]);

    Promise.all([
      d3.json("https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json"),
      d3.json("/data/processed/bubble_map_data.json")
    ])
      .then(([us, data]) => {
        svg.append("g")
          .selectAll("path")
          .data(topojson.feature(us, us.objects.states).features)
          .join("path")
          .attr("fill", "#f0f0f0")
          .attr("stroke", "#ccc")
          .attr("d", path);

        svg.append("g")
          .selectAll("circle")
          .data(data)
          .join("circle")
          .attr("cx", d => {
            const coords = projection([d.longitude, d.latitude]);
            return coords ? coords[0] : -1000;
          })
          .attr("cy", d => {
            const coords = projection([d.longitude, d.latitude]);
            return coords ? coords[1] : -1000;
          })
          .attr("r", d => size(d.haunted_count))
          .attr("fill", d => color(d.avg_total_deaths))
          .attr("fill-opacity", 0.75)
          .attr("stroke", "#333")
          .attr("stroke-width", 0.5)
          .on("mouseover", (event, d) => {
            tooltip
              .style("opacity", 1)
              .style("left", `${event.pageX + 10}px`)
              .style("top", `${event.pageY - 28}px`)
              .style("visibility", "visible")
              .html(`
                <strong>${d.city}, ${d.state}</strong><br/>
                Hauntings: ${d.haunted_count}<br/>
                Avg Total Deaths: ${d.avg_total_deaths}<br/>
                % Under 21: ${d.avg_percent_under_21}
              `);
          })
          .on("mouseout", () => tooltip.style("visibility", "hidden"));
      })
      .catch(err => console.error("Error loading data:", err));
  }, []);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "2rem",
        maxWidth: "1200px",
        margin: "0 auto",
      }}
    >
      <h2
        style={{
          color: "darkred",
          fontSize: "28px",
          textAlign: "center",
          marginBottom: "1rem",
        }}
      >
        Haunted Places and Alcohol Influence (Bubble Map)
      </h2>
  
      <div
        style={{
          maxWidth: "800px",
          fontSize: "15px",
          textAlign: "center",
          lineHeight: "1.6",
          marginBottom: "2rem",
        }}
      >
        <p>
          This map visualizes haunted locations across the United States based on reports from our dataset.
          Each circle (bubble) represents a city or town. The size of the bubble reflects the number of reported haunted places,
          with larger bubbles indicating more hauntings. The color of the bubble corresponds to the average number of
          alcohol-related deaths in that location, with darker red hues representing higher mortality rates.
        </p>
        <p>
          Our analysis suggests that areas with higher alcohol-related mortality also tend to report more supernatural sightings.
          These findings align with our earlier observations from assignment 1 that alcohol abuse can contribute to increased haunted activity.
        </p>
      </div>
  
      <div
        style={{
          width: "100%",
          display: "flex",
          justifyContent: "center",
        }}
      >
        <svg ref={svgRef} style={{ maxWidth: "100%", height: "auto" }} />
      </div>
    </div>
  );
  
  
  
}
