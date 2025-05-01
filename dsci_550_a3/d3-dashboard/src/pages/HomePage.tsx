import React from "react";

function HomePage() {
  return (
    <div
      style={{
        backgroundImage: "url('/background.jpg')",
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
        width: "100vw",          // ✅ Ensures full width
        height: "100vh",         // ✅ Ensures full height
        margin: 0,
        padding: 0,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          backgroundColor: "rgba(0, 0, 0, 0.7)",
          padding: "40px",
          borderRadius: "12px",
          textAlign: "center",
          color: "white",
          maxWidth: "800px",
        }}
      >
        <h1 style={{ fontSize: "2.5rem", marginBottom: "20px" }}>
          Haunted Places Visualizations Hub
        </h1>
        <p style={{ fontSize: "1.2rem", lineHeight: "1.6" }}>
        Explore five interactive visualizations created by our team to uncover patterns and relationships among haunted locations. Use the navigation bar above to explore each chart!
        </p>
      </div>
    </div>
  );
}

export default HomePage;
