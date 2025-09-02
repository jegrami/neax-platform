import { ArrowLeft, ArrowRight, BarChart3, Info, Download, Share2 } from "lucide-react";

function RightSidebar({ toggle, isOpen }) {
  return (
    <div className={`
      bg-white border-l border-gray-200 h-full flex-shrink-0 relative z-10
      transition-all duration-300 ease-in-out
      ${isOpen ? "w-80" : "w-0"}
    `}>
      {/* Toggle Button - Always visible and positioned correctly */}
      <button
        onClick={toggle}
        className={`
          absolute top-4 bg-white border border-gray-300 rounded-md p-2 shadow-lg
          hover:bg-gray-200 transition-all duration-300 z-30
          ${isOpen ? "left-[-20px]" : "left-[-44px]"}
        `}
      >
        {isOpen ? <ArrowRight size={16} /> : <ArrowLeft size={16} />}
      </button>

      {/* Sidebar Content */}
      <div className={`
        h-full overflow-hidden
        ${isOpen ? "opacity-100" : "opacity-0 pointer-events-none"}
        transition-opacity duration-300
      `}>
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center gap-2 mb-3">
              <BarChart3 size={20} className="text-green-600" />
              <h2 className="text-lg font-semibold text-gray-900">Insights</h2>
            </div>
            
            {/* Action Buttons */}
            <div className="flex gap-2">
              <button className="flex items-center gap-1 px-3 py-1.5 text-xs bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors">
                <Download size={14} />
                Download
              </button>
              <button className="flex items-center gap-1 px-3 py-1.5 text-xs bg-gray-50 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors">
                <Share2 size={14} />
                Share
              </button>
            </div>
          </div>

          {/* Content Area */}
          <div className="flex-1 overflow-y-auto">
            <div className="p-4">
              {/* Map Info */}
              <div className="mb-6">
                <div className="flex items-center gap-2 mb-3">
                  <Info size={16} className="text-blue-600" />
                  <h3 className="font-medium text-gray-900">Map Overview</h3>
                </div>
                <div className="bg-blue-50 rounded-lg p-3">
                  <p className="text-sm text-gray-700">
                    Displaying energy access data for Nigeria. Zoom and pan to explore different regions.
                  </p>
                </div>
              </div>

              {/* Statistics */}
              <div className="mb-6">
                <h3 className="font-medium text-gray-900 mb-3">Key Statistics</h3>
                <div className="space-y-3">
                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="text-2xl font-bold text-green-600">85.2%</div>
                    <div className="text-sm text-gray-600">Population with electricity access</div>
                  </div>
                  
                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="text-2xl font-bold text-blue-600">220M</div>
                    <div className="text-sm text-gray-600">Total population</div>
                  </div>
                  
                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="text-2xl font-bold text-orange-600">5.2 kWh</div>
                    <div className="text-sm text-gray-600">Average solar irradiance</div>
                  </div>
                </div>
              </div>

              {/* Chart Placeholder */}
              <div className="mb-6">
                <h3 className="font-medium text-gray-900 mb-3">Trends</h3>
                <div className="bg-gray-100 rounded-lg p-4 h-48 flex items-center justify-center">
                  <div className="text-center text-gray-500">
                    <BarChart3 size={48} className="mx-auto mb-2 opacity-50" />
                    <p className="text-sm">Charts and visualizations will appear here based on selected data layers</p>
                  </div>
                </div>
              </div>

              {/* Data Sources */}
              <div>
                <h3 className="font-medium text-gray-900 mb-3">Data Sources</h3>
                <div className="space-y-2">
                  <div className="text-xs text-gray-600 bg-gray-50 rounded px-2 py-1">
                    World Bank - Energy Access Database
                  </div>
                  <div className="text-xs text-gray-600 bg-gray-50 rounded px-2 py-1">
                    NASA - Solar Resource Data
                  </div>
                  <div className="text-xs text-gray-600 bg-gray-50 rounded px-2 py-1">
                    OpenStreetMap - Infrastructure Data
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RightSidebar;