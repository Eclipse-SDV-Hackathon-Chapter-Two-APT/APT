import './App.css';
import React, { useEffect, useRef, useState } from "react";

const App = () => {
  const socketRef = useRef(null);
  const [message, setMessage] = useState([]);
  const [accidents, setAccidents] = useState([]);
  const [selectedAccident, setSelectedAccident] = useState(null);
  const mapRef = useRef(null);
  const mapInstance = useRef(null);
  const markers = useRef([]);

  const [status, setStatus] = useState("Disconnected");

  useEffect(() => {
    if (!socketRef.current) {
      const socket = new WebSocket("ws://0.0.0.0:8765");
      socketRef.current = socket;

      socket.onopen = () => {
        setStatus("Connected");
        console.log("WebSocket Connected");
      };

      socket.onmessage = (event) => {
        console.log("Message from server:", event.data);
        try {
          const jsonData = JSON.parse(event.data);
          console.log("Parsed message:", jsonData);

          if (jsonData.type === "accident") {
            const accidentData = JSON.parse(jsonData.data);
            const { vehicleRegistrationNumber, timestamp, location } = accidentData;
            const { latitude, longitude } = location;

            setAccidents((prev) => [
              ...prev,
              {
                vehicleRegistrationNumber,
                timestamp,
                latitude,
                longitude,
              },
            ]);
          } else {
            console.warn("Unknown message type:", jsonData.type);
          }
        } catch (error) {
          console.error("Failed to parse message:", error);
        }
      };

      socket.onerror = (error) => {
        console.error("WebSocket Error:", error);
        setStatus("Error");
      };

      socket.onclose = () => {
        setStatus("Disconnected");
        console.log("WebSocket Disconnected");
      };
    }

    return () => {
      if (socketRef.current?.readyState === 1) {
        socketRef.current.close();
      }
    };
  }, []);

  useEffect(() => {
    const loadGoogleMaps = () => {
      if (window.google) {
        mapInstance.current = new window.google.maps.Map(mapRef.current, {
          center: { lat: 49.014, lng: 8.4043 },
          zoom: 12,
        });
      }
    };

    const script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.REACT_APP_GOOGLE_MAPS_API_KEY}`;
    script.async = true;
    script.defer = true;
    script.onload = loadGoogleMaps;
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  useEffect(() => {
    if (mapInstance.current) {
      markers.current.forEach((marker) => marker.setMap(null));
      markers.current = [];

      accidents.forEach((accident) => {
        const marker = new window.google.maps.Marker({
          position: { lat: accident.latitude, lng: accident.longitude },
          map: mapInstance.current,
          title: `차량 번호: ${accident.vehicleRegistrationNumber}`,
        });
        markers.current.push(marker);
      });
    }
  }, [accidents]);

  const handleAccidentClick = (accident) => {
    setSelectedAccident(accident);
    mapInstance.current.panTo({ lat: accident.latitude, lng: accident.longitude });
    mapInstance.current.setZoom(14);
  };

  const handleDeleteAccident = (vehicleRegistrationNumber) => {
    setAccidents((prevAccidents) =>
      prevAccidents.filter(
        (accident) => accident.vehicleRegistrationNumber !== vehicleRegistrationNumber
      )
    );
  };


  return (
    <div style={{ display: "flex", height: "100vh" }}>

      <div ref={mapRef} style={{ flex: 3, height: "100%" }}></div>

      <div style={{ flex: 1, overflowY: "scroll", padding: "10px", background: "#f8f8f8" }}>
        <h2>사고 정보</h2>
        {accidents.map((accident, index) => (
          <div
            key={index}
            onClick={() => handleAccidentClick(accident)}
            style={{
              padding: "10px",
              margin: "10px 0",
              background: selectedAccident === accident ? "#e0f7fa" : "#ffffff",
              border: "1px solid #ccc",
              cursor: "pointer",
              position: "relative"
            }}
          >
            <p>차량 번호: {accident.vehicleRegistrationNumber}</p>
            <p>시간: {accident.timestamp}</p>
            <p>위도: {accident.latitude}</p>
            <p>경도: {accident.longitude}</p>

            <button
              onClick={(e) => {
                e.stopPropagation();
                handleDeleteAccident(accident.vehicleRegistrationNumber);
              }}
              style={{
                position: "absolute",
                top: "10px",
                right: "10px",
                backgroundColor: "red",
                color: "white",
                border: "none",
                borderRadius: "50%",
                padding: "5px 10px",
                cursor: "pointer",
              }}
            >
              X
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;
