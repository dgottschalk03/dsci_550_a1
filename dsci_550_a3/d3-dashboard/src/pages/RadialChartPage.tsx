import React, { useEffect } from "react";

function RadialChartPage() {
  useEffect(() => {
    const timeout = setTimeout(() => {
      const script = document.createElement("script");
      script.src = "/scripts/radial_chart.js";
      script.async = true;
      document.body.appendChild(script);
    }, 200);

    return () => {
      clearTimeout(timeout);
      const scripts = document.querySelectorAll("script[src='/scripts/radial_chart.js']");
      scripts.forEach(script => script.remove());
    };
  }, []);

  return (
    <div style={{ fontFamily: "sans-serif", padding: "15px 20px" }}>
      <h1 style={{ textAlign: "center", fontSize: "2em", margin: "10px 0", color: "#0a1f44" }}>
        Which Religions Are Closest to Haunted Places, and What Apparitions Appear Near Them?
      </h1>

      <div style={{ fontSize: "0.9em", maxWidth: "850px", margin: "0 auto 15px", lineHeight: "1.4" }}>
        <div style={{ textAlign: "center", marginTop: "15px" }}><strong>Description</strong></div>
        <p style={{ textAlign: "justify", marginTop: "5px" }}>
          To explore how spiritual geography relates to reported hauntings, we created a radial stacked bar chart where each bar represents a religion. The height of the bar reflects the median distance from haunted places to the nearest place of worship associated with that religion, meaning shorter bars indicate haunted places tend to be located closer to those religious sites. Each bar is divided into colored segments, which represent the percentage breakdown of apparition types (e.g., Ghost, Spirit, Demon, Orb, Unknown) most commonly reported near that religion.
        </p>

        <div style={{ textAlign: "center", marginTop: "15px" }}><strong>Interactive Features</strong></div>
        <p style={{ textAlign: "justify", marginTop: "5px" }}>
          Click on a bar to expand it to the full radius of the circle, this makes it easier to see the detailed apparition type breakdown. Hover over any segment to see a tooltip with the religion name, apparition type, exact percentage, and median distance to the nearest worship site.
        </p>

        <div style={{ textAlign: "center", marginTop: "15px" }}><strong>Insight</strong></div>
        <p style={{ textAlign: "justify", marginTop: "5px" }}>
          Religions like Biker, Interfaith, and Tenrikyo are closest to haunted places but mostly report “Unknown” apparitions. Christianity shows the widest range of apparition types, reflecting strong cultural influence on how hauntings are described. Jewish, Muslim, Buddhist, and UU sites commonly report Ghosts and Spirits, pointing to shared ideas across traditions. Some groups (e.g., Mazónica, Jain, Religious Science) report only “Unknowns,” likely due to small sample sizes or less emphasis on specific descriptions. This chart builds on earlier clustering results by adding a visual layer that shows not just where hauntings happen, but how they are interpreted through different spiritual lenses, turning abstract data into an interactive view of cultural patterns in haunting reports.
        </p>
      </div>

      <div style={{ display: "flex", justifyContent: "center" }}>
        <svg></svg>
      </div>
    </div>
  );
}

export default RadialChartPage;
