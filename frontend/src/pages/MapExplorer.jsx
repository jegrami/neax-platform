
import { useState } from 'react'
import MapView from '../components/maps/MapView'
import LeftSidebar from '../components/maps/LeftSidebar'
import RightSidebar from '../components/maps/RightSidebar'

function MapExplorer() {
  const [leftOpen, setLeftOpen] = useState(true);
  const [rightOpen, setRightOpen] = useState(true);
  
  return (
    <div className="flex h-screen w-full overflow-hidden">
      {/* Left Sidebar */}
      <LeftSidebar 
        isOpen={leftOpen} 
        toggle={() => setLeftOpen(!leftOpen)} 
      />
      
      {/* Map Container - takes remaining space */}
      <div className="flex-1 relative">
        <MapView 
          leftSidebarOpen={leftOpen}
          rightSidebarOpen={rightOpen}
        />
      </div>
      
      {/* Right Sidebar */}
      <RightSidebar 
        isOpen={rightOpen} 
        toggle={() => setRightOpen(!rightOpen)} 
      />
    </div>
  );
}

export default MapExplorer;