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
  const directionsService = useRef(null);
  const directionsRenderer = useRef(null);
  const trafficLayer = useRef(null);

  const [newAccident, setNewAccident] = useState(null);
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

            const newAccident = {
              vehicleRegistrationNumber,
              timestamp,
              latitude,
              longitude,
            };
            setAccidents((prev) => [...prev, newAccident]);
            setNewAccident(newAccident);
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
          zoom: 15,
        });
        directionsService.current = new window.google.maps.DirectionsService();
        directionsRenderer.current = new window.google.maps.DirectionsRenderer()
        directionsRenderer.current.setMap(mapInstance.current);

        trafficLayer.current = new window.google.maps.TrafficLayer();
        trafficLayer.current.setMap(mapInstance.current);
      }
    };

    const script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.REACT_APP_GOOGLE_MAPS_API_KEY}&region=GER&language=en`;
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


  useEffect(() => {
    if (newAccident) {
      const timer = setTimeout(() => {
        setNewAccident(null);
      }, 3000); // 3초 후에 애니메이션 클래스 제거
      return () => clearTimeout(timer);
    }
  }, [newAccident]);

  const handleNewAccident = (accident) => {
    setAccidents((prevAccidents) => [...prevAccidents, accident]);
    setNewAccident(accident);
  };

  const handleAccidentClick = (accident) => {
    setSelectedAccident(accident);
    mapInstance.current.panTo({ lat: accident.latitude, lng: accident.longitude });
    mapInstance.current.setZoom(18);
  };

  const handleDeleteAccident = (vehicleRegistrationNumber) => {
    setAccidents((prevAccidents) =>
      prevAccidents.filter(
        (accident) => accident.vehicleRegistrationNumber !== vehicleRegistrationNumber
      )
    );
  };

  const handleNavigate = (accident) => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        const currentLocation = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };

        const destination = {
          lat: accident.latitude,
          lng: accident.longitude,
        };

        const request = {
          origin: currentLocation,
          destination: destination,
          travelMode: window.google.maps.TravelMode.DRIVING,
        };

        directionsService.current.route(request, (result, status) => {
          if (status === window.google.maps.DirectionsStatus.OK) {
            directionsRenderer.current.setDirections(result);
          } else {
            console.error("Directions request failed due to " + status);
          }
        });
      });
    } else {
      console.error("Geolocation is not supported by this browser.");
    }
  };

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <div ref={mapRef} style={{ flex: 3, height: "100%" }}></div>
      <div style={{ flex: 1, display: "flex", flexDirection: "column", background: "#f8f8f8" }}>
        <div
          className=" h-[70px] relative left-[-0.5px] top-[-0.5px] bg-[#103a5e] flex justify-center items-center"
          style={{ boxShadow: '3px 0px 10px 0 rgba(0,0,0,0.25)' }}
        >
          <p className="absolute left-[300px] top-0 text-[35px] font-semibold text-center text-[#f3efef]">
            EMS
          </p>
          <p className="absolute left-[185px] top-11 text-xs font-semibold text-center text-[#b2b2b2]">
            Comprehensive Control System
          </p>
        </div>

        <div style={{ flex: 1, overflowY: "scroll", paddingLeft: "25px", marginTop: "0px", background: "#f8f8f8" }}>
          {accidents.slice().reverse().map((accident, index) => (
            <div
              key={index}
              onClick={() => handleAccidentClick(accident)}
              className={`w-[370px] h-[132.83px] relative mb-4 ${newAccident === accident ? 'blink' : ''}`}
              style={{
                padding: "10px",
                margin: "40px 0",
                background: "#ffffff",
                cursor: "pointer",
                position: "relative",
                filter: "drop-shadow(0px 4px 4px rgba(0,0,0,0.25))",
                borderRadius: "5px"
              }}
            >
              <div style={{
                width: "3.9px",
                height: "132.83px",
                position: "absolute",
                left: "-1px",
                top: "0.66px",
                borderTopLeftRadius: "10px",
                borderBottomLeftRadius: "10px",
                backgroundColor: selectedAccident === accident ? "#ff0fca" : "#0097fb",

              }}
              />
              <div className="flex flex-col justify-start items-start w-[335px] h-[104px] absolute left-[10px] top-[20px]">
                <div className="self-stretch flex-grow-0 flex-shrink-0 h-[26px] relative overflow-hidden">
                  <p className="absolute left-1.5 top-1 text-[15px] font-semibold text-left text-[#103a5e]">
                    Vehicle Number
                  </p>
                  <p className="w-[166px] h-[19px] absolute left-[152px] top-[3px] text-[13px] font-medium text-left text-[#7d7d7d]">
                    {accident.vehicleRegistrationNumber}
                  </p>
                </div>
                <div className="self-stretch flex-grow-0 flex-shrink-0 h-[26px] relative overflow-hidden">
                  <p className="absolute left-1.5 top-1 text-[15px] font-semibold text-left text-[#103a5e]">
                    Occurrence Time
                  </p>
                  <p className="w-[166px] h-[19px] absolute left-[152px] top-[3px] text-[13px] font-medium text-left text-[#7d7d7d]">
                    {accident.timestamp}
                  </p>
                </div>
                <div className="self-stretch flex-grow-0 flex-shrink-0 h-[26px] relative overflow-hidden">
                  <p className="absolute left-1.5 top-1 text-[15px] font-semibold text-left text-[#103a5e]">
                    Latitude
                  </p>
                  <p className="w-[108px] h-[19px] absolute left-[152px] top-[3px] text-[13px] font-medium text-left text-[#7d7d7d]">
                    {accident.latitude}
                  </p>
                </div>
                <div className="self-stretch flex-grow-0 flex-shrink-0 h-[26px] relative overflow-hidden">
                  <p className="absolute left-1.5 top-1 text-[15px] font-semibold text-left text-[#103a5e]">
                    Longitude
                  </p>
                  <p className="w-[108px] h-[19px] absolute left-[152px] top-[3px] text-[13px] font-medium text-left text-[#7d7d7d]">
                    {accident.longitude}
                  </p>
                </div>
                <div className="w-[88.73px] h-[22.44px] absolute right-0 bottom-0">
                  <div
                    className="flex justify-center items-center w-[88.73px] h-[22.44px] px-2.5 py-[3px] rounded-lg bg-[#103a5e]"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleNavigate(accident);
                    }}
                  >
                    <p className="flex-grow-0 flex-shrink-0 text-[11px] font-medium text-left text-white">
                      Create Route
                    </p>
                  </div>
                </div>
              </div>
              <svg
                width="31"
                height="30"
                viewBox="0 0 31 30"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                className="w-[30px] h-[30px] absolute left-[10px] top-[-15px]"
                preserveAspectRatio="xMidYMid meet"
                style={{ zIndex: 1 }}
              >
                <path d={selectedAccident === accident ? "M6.875 27.5V24.75H9.075L12.375 13.75H20.625L23.925 24.75H26.125V27.5H6.875ZM11.9625 24.75H21.0375L18.5625 16.5H14.4375L11.9625 24.75ZM15.125 11V4.125H17.875V11H15.125ZM23.3063 14.4031L21.3469 12.4437L26.2281 7.59687L28.1531 9.52187L23.3063 14.4031ZM24.75 20.625V17.875H31.625V20.625H24.75ZM9.69375 14.4031L4.84688 9.52187L6.77188 7.59687L11.6531 12.4437L9.69375 14.4031ZM1.375 20.625V17.875H8.25V20.625H1.375Z"
                  : "M26.4357 12.6938L24.7257 7.56375C24.4776 6.81685 24.0005 6.16713 23.3621 5.70689C22.7237 5.24664 21.9565 4.9993 21.1695 5H9.77195C8.98494 4.9993 8.21772 5.24664 7.57931 5.70689C6.9409 6.16713 6.46376 6.81685 6.2157 7.56375L4.5057 12.6938C4.05098 12.884 3.66265 13.2045 3.38954 13.6148C3.11642 14.0252 2.9707 14.5071 2.9707 15V21.25C2.9707 22.1725 3.4757 22.97 4.2207 23.4038V26.25C4.2207 26.5815 4.3524 26.8995 4.58682 27.1339C4.82124 27.3683 5.13918 27.5 5.4707 27.5H6.7207C7.05222 27.5 7.37017 27.3683 7.60459 27.1339C7.83901 26.8995 7.9707 26.5815 7.9707 26.25V23.75H22.9707V26.25C22.9707 26.5815 23.1024 26.8995 23.3368 27.1339C23.5712 27.3683 23.8892 27.5 24.2207 27.5H25.4707C25.8022 27.5 26.1202 27.3683 26.3546 27.1339C26.589 26.8995 26.7207 26.5815 26.7207 26.25V23.4038C27.0999 23.1863 27.4152 22.8727 27.6346 22.4946C27.8541 22.1164 27.97 21.6872 27.9707 21.25V15C27.9707 14.5071 27.825 14.0252 27.5519 13.6148C27.2787 13.2045 26.8904 12.884 26.4357 12.6938ZM9.77195 7.5H21.1682C21.707 7.5 22.1845 7.8425 22.3545 8.355L23.737 12.5H7.20445L8.5857 8.355C8.66864 8.10599 8.82785 7.88941 9.04076 7.73595C9.25368 7.58249 9.5095 7.49994 9.77195 7.5ZM7.3457 20C7.09939 19.9999 6.85551 19.9513 6.62798 19.857C6.40045 19.7627 6.19373 19.6244 6.01962 19.4502C5.84551 19.276 5.70742 19.0692 5.61324 18.8416C5.51905 18.614 5.47062 18.3701 5.4707 18.1238C5.47078 17.8774 5.51938 17.6336 5.61372 17.406C5.70805 17.1785 5.84628 16.9718 6.0205 16.7977C6.19473 16.6236 6.40154 16.4855 6.62913 16.3913C6.85673 16.2971 7.10064 16.2487 7.34695 16.2488C7.8444 16.2489 8.32141 16.4467 8.67304 16.7986C9.02467 17.1504 9.22212 17.6276 9.22195 18.125C9.22179 18.6224 9.02402 19.0995 8.67215 19.4511C8.32029 19.8027 7.84315 20.0002 7.3457 20ZM23.5957 20C23.3494 19.9999 23.1055 19.9513 22.878 19.857C22.6504 19.7627 22.4437 19.6244 22.2696 19.4502C22.0955 19.276 21.9574 19.0692 21.8632 18.8416C21.7691 18.614 21.7206 18.3701 21.7207 18.1238C21.7208 17.8774 21.7694 17.6336 21.8637 17.406C21.958 17.1785 22.0963 16.9718 22.2705 16.7977C22.4447 16.6236 22.6515 16.4855 22.8791 16.3913C23.1067 16.2971 23.3506 16.2487 23.597 16.2488C24.0944 16.2489 24.5714 16.4467 24.923 16.7986C25.2747 17.1504 25.4721 17.6276 25.472 18.125C25.4718 18.6224 25.274 19.0995 24.9222 19.4511C24.5703 19.8027 24.0931 20.0002 23.5957 20Z"}
                  fill={selectedAccident === accident ? "#ff0fca" : "#0097FB"}></path>
              </svg>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleDeleteAccident(accident.vehicleRegistrationNumber);
                }}
                style={{
                  position: "absolute",
                  top: "10px",
                  right: "10px",
                  color: "grey",
                  border: "none",
                  borderRadius: "50%",
                  padding: "0px px",
                  cursor: "pointer",
                }}
              >
                X
              </button>
            </div>
          ))}
      </div>
      </div>
    </div>
  );
};

export default App;