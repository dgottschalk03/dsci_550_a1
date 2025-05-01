import React, { useEffect } from "react";

function ScatterplotPage() {
  useEffect(() => {
    // ✅ Clear any old chart content
    const scatterDiv = document.getElementById("scatterplot");
    if (scatterDiv) {
      scatterDiv.innerHTML = "";
    }

    const script = document.createElement("script");
    script.src = "/scripts/scatterplot.js";  // match what you save it as
    script.async = true;
    script.id = "scatterplot-script";
    document.body.appendChild(script);

    return () => {
      const oldScript = document.getElementById("scatterplot-script");
      if (oldScript) {
        document.body.removeChild(oldScript);
      }
      if (scatterDiv) {
        scatterDiv.innerHTML = "";
      }
    };
  }, []);

  return (
    <div style={{ textAlign: "center", padding: "40px", minHeight: "100vh" }}>
      <h1 style={{ fontSize: "2rem", marginBottom: "20px", color: "#800026" }}>
        Daylight Duration and Haunted Apparitions: Patterns of Supernatural Activity
      </h1>

      <p style={{ maxWidth: "800px", margin: "0 auto 20px", fontSize: "16px", lineHeight: "1.6" }}>
        This scatterplot visualizes the relationship between the number of daylight hours and the types 
        of reported haunted apparitions. Each dot represents a recorded haunted event, categorized by apparition 
        type and colored based on whether the encounter was violent (red) or non-violent (blue). 
        The horizontal position reflects the duration of daylight at the time of the report.
      </p>

      <p style={{ maxWidth: "800px", margin: "0 auto 30px", fontSize: "16px", lineHeight: "1.6" }}>
        Our analysis suggests that sightings of certain apparition types, such as Spirits and Orbs, occur more 
        frequently during periods with longer daylight hours, while Ghost and Demon sightings show a more even 
        distribution across daylight conditions. Violent supernatural encounters appear to have no strong correlation 
        with daylight duration, indicating that violent hauntings may be influenced by other environmental or 
        psychological factors rather than light exposure.
      </p>

      {/* Controls and chart will be injected by D3 */}
      <div id="controls" style={{ marginBottom: "20px" }}></div>
      <div id="scatterplot"></div>
    </div>
  );
}

export default ScatterplotPage;
