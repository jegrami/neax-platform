import { MapContainer, TileLayer, useMap } from "react-leaflet";
import { useEffect, useRef } from "react";

function ResizeHandler({ leftSidebarOpen, rightSidebarOpen }) {
  const map = useMap();
  
  useEffect(() => {
    // Use a timeout to ensure DOM has updated
    const timer = setTimeout(() => {
      map.invalidateSize();
    }, 100);
    
    return () => clearTimeout(timer);
  }, [leftSidebarOpen, rightSidebarOpen, map]);
  
  return null;
}

function MapView({ leftSidebarOpen, rightSidebarOpen }) {
  const mapRef = useRef(null);
  const position = [9.082, 8.6753]; // Nigeria center coordinates
  
  return (
    <div className="absolute inset-0 w-full h-full">
      <MapContainer
        ref={mapRef}
        center={position}
        zoom={6}
        className="w-full h-full"
        style={{ 
          height: '100%', 
          width: '100%',
          zIndex: 1
        }}
        zoomControl={true}
        scrollWheelZoom={true}
        doubleClickZoom={true}
        dragging={true}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors"
          maxZoom={18}
          tileSize={256}
        />
        <ResizeHandler 
          leftSidebarOpen={leftSidebarOpen}
          rightSidebarOpen={rightSidebarOpen}
        />
      </MapContainer>
    </div>
  );
}

export default MapView;