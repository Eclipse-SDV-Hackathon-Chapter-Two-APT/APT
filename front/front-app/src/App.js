import './App.css';
import React, { useEffect, useRef, useState } from "react";

const App = () => {
  const socketRef = useRef(null);
  const [message, setMessage] = useState(''); // 서버로부터 받은 메시지
  const [inputMessage, setInputMessage] = useState(''); // 보내고자 하는 메시지

  const [accidents, setAccidents] = useState([]); // 사고 데이터 리스트
  const [selectedAccident, setSelectedAccident] = useState(null); // 선택된 사고
  const mapRef = useRef(null); // 지도 DOM 요소
  const mapInstance = useRef(null); // Google Maps 객체
  const markers = useRef([]); // 지도에 표시된 마커 리스트

  const [status, setStatus] = useState("Disconnected");
  let socket;

  useEffect(() => {
    if (!socketRef.current) {
      socket = new WebSocket("ws://0.0.0.0:8765");
      socketRef.current = socket;

      socket.onopen = () => {
        setStatus("Connected");
        console.log("WebSocket Connected");
        socket.send("Hello Server!"); // 서버로 메시지 보내기
      };

      socket.onmessage = (event) => {
        console.log("Message from server:", event.data);
        // setMessages((prev) => [...prev, event.data]);
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
      if (socket.readyState === 1) {
        socket.close();
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
          position: { lat: accident.lat, lng: accident.lng },
          map: mapInstance.current,
          title: `사고 차량: ${accident.vehicleId}`,
        });
        markers.current.push(marker);
      });
    }
  }, [accidents]);

  const handleAccidentClick = (accident) => {
    setSelectedAccident(accident);
    mapInstance.current.panTo({ lat: accident.lat, lng: accident.lng }); // 지도 중심 이동
    mapInstance.current.setZoom(14); // 클릭한 사고 차량에 맞게 줌 레벨 조정
  };

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {/* 지도 */}
      <div ref={mapRef} style={{ flex: 3, height: "100%" }}></div>

      {/* 사고 정보 리스트 */}
      <div style={{ flex: 1, overflowY: "scroll", padding: "10px", background: "#f8f8f8" }}>
        <h2>사고 정보</h2>
        {accidents.map((accident, index) => (
          <div
            key={index}
            onClick={() => handleAccidentClick(accident)} // 클릭 시 해당 사고 위치로 지도 이동
            style={{
              padding: "10px",
              margin: "10px 0",
              background: selectedAccident === accident ? "#e0f7fa" : "#ffffff",
              border: "1px solid #ccc",
              cursor: "pointer",
            }}
          >
            <p>차량 ID: {accident.vehicleId}</p>
            <p>위도: {accident.lat}</p>
            <p>경도: {accident.lng}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;
