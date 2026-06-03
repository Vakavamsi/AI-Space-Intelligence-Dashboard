import { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState({
    people_count: 0,
    status: "Loading...",
    space_utilization: "0%",
  });

  const [currentTime, setCurrentTime] = useState(
    new Date().toLocaleTimeString()
  );

  const fetchData = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/occupancy");
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchData();

    const interval = setInterval(() => {
      fetchData();
      setCurrentTime(new Date().toLocaleTimeString());
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const cardStyle = {
    background: "white",
    padding: "25px",
    borderRadius: "15px",
    width: "280px",
    textAlign: "center",
    boxShadow: "0px 4px 15px rgba(0,0,0,0.1)",
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#f4f6f9",
        padding: "30px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1
        style={{
          textAlign: "center",
          marginBottom: "40px",
          fontSize: "55px",
        }}
      >
        AI Space Intelligence Dashboard
      </h1>

      <div
        style={{
          display: "flex",
          gap: "20px",
          justifyContent: "center",
          flexWrap: "wrap",
        }}
      >
        <div style={cardStyle}>
          <h2>People Count</h2>
          <h1 style={{ fontSize: "60px" }}>{data.people_count}</h1>
        </div>

        <div style={cardStyle}>
          <h2>Crowd Status</h2>
          <div
            style={{
              fontSize: "35px",
              fontWeight: "bold",
              color: "#2563eb",
              marginTop: "30px",
            }}
          >
            {data.status}
          </div>
        </div>

        <div style={cardStyle}>
          <h2>Space Utilization</h2>
          <h1 style={{ fontSize: "60px" }}>
            {data.space_utilization}
          </h1>
        </div>

        <div style={cardStyle}>
          <h2>WiFi Devices</h2>
          <h1 style={{ fontSize: "60px" }}>3</h1>
        </div>

        <div style={cardStyle}>
          <h2>Predicted Occupancy</h2>
          <h1 style={{ fontSize: "60px" }}>
            {data.people_count + 2}
          </h1>
        </div>

        <div style={cardStyle}>
          <h2>Current Time</h2>
          <h3>{currentTime}</h3>
        </div>
      </div>
    </div>
  );
}

export default App;