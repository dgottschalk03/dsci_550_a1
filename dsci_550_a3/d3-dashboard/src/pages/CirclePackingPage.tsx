import React, { useEffect } from "react";

function CirclePackingPage() {
    useEffect(() => {
        // ✅ Always clean chart div before adding
        const chartDiv = document.getElementById("chart");
        if (chartDiv) {
          chartDiv.innerHTML = ""; // Clears old SVG/content
        }
      
        // ✅ Then create the new script
        const script = document.createElement("script");
        script.src = "/scripts/circlepacking.js";
        script.async = true;
        script.id = "circlepacking-script"; // Optional: ID for extra clarity
        document.body.appendChild(script);
      
        return () => {
          // ✅ Cleanup when leaving page
          const oldScript = document.getElementById("circlepacking-script");
          if (oldScript) {
            document.body.removeChild(oldScript);
          }
          if (chartDiv) {
            chartDiv.innerHTML = "";
          }
        };
      }, []);

  return (
    <div style={{ textAlign: "center", padding: "40px", minHeight: "100vh" }}>
      <h1 style={{ fontSize: "2rem", marginBottom: "20px", color: "#0a1f44" }}>
        Haunted Apparition Types and City Sightings (Circle Packing Map)
      </h1>

      <p style={{ maxWidth: "800px", margin: "0 auto 20px", fontSize: "16px", lineHeight: "1.6" }}>
        This map visualizes haunted locations across the United States based on apparition type and city reports from our dataset. 
        Larger colored bubbles represent different apparition types, such as "Ghost," "Spirit," or "Unknown." Smaller bubbles within each 
        type correspond to cities, with the size of each city bubble reflecting the number of reported sightings. Cities with more than 10 sightings are labeled. 
        Solid circles represent cities associated with a single apparition type, while boldened outline circles indicate cities reporting multiple apparition types. 
        You can hover over each of the circles for more information.
      </p>

      <p style={{ maxWidth: "800px", margin: "0 auto 30px", fontSize: "16px", lineHeight: "1.6" }}>
        Our analysis suggests that most haunted sightings are concentrated in a few apparition types, with Ghosts and Spirits being the most frequently reported. 
        Our circle packing visualization highlights this dominance and shows that cities like Los Angeles, San Antonio, and Columbus report multiple apparition types. 
        These patterns reinforce previous findings that hauntings cluster around urban areas and culturally significant locations, shaped by social and environmental factors.
      </p>

      {/* ✅ This is where D3 injects the circles */}
      <div id="chart" style={{ display: "flex", justifyContent: "center", marginTop: "30px" }}></div>
    </div>
  );
}

export default CirclePackingPage;
