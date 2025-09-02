

import { ArrowLeft, ArrowRight, Search, Layers, Filter } from "lucide-react";

function LeftSidebar({ toggle, isOpen }) {
  return (
    <div className={`
      bg-white border-r border-gray-200 h-full flex-shrink-0 relative z-10
      transition-all duration-300 ease-in-out
      ${isOpen ? "w-80" : "w-0"}
    `}>
      {/* Toggle Arrow */}
      <button
        onClick={toggle}
        className={`
          absolute top-4 bg-white border border-gray-300 rounded-md p-2 shadow-lg
          hover:bg-gray-200 transition-all duration-300 z-30
          ${isOpen ? "right-[-20px]" : "right-[-44px]"}
        `}
      >
        {isOpen ? <ArrowLeft size={16} /> : <ArrowRight size={16} />}
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
              <Layers size={20} className="text-blue-600" />
              <h2 className="text-lg font-semibold text-gray-900">Data Layers</h2>
            </div>
            
            {/* Search */}
            <div className="relative">
              <Search size={16} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Search datasets..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
              />
            </div>
          </div>

          {/* Filters Section */}
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center gap-2 mb-3">
              <Filter size={16} className="text-gray-600" />
              <h3 className="font-medium text-gray-900">Filters</h3>
            </div>
            
            {/* Energy Category Filter */}
            <div className="space-y-2">
              <div className="flex items-center">
                <input type="checkbox" id="energy" className="mr-2" defaultChecked />
                <label htmlFor="energy" className="text-sm text-gray-700">Energy</label>
                <span className="ml-auto text-xs text-gray-500 bg-blue-100 px-2 py-1 rounded">35</span>
              </div>
            </div>
          </div>

          {/* Content Area */}
          <div className="flex-1 overflow-y-auto">
            <div className="p-4">
              <h3 className="font-medium text-gray-900 mb-3">Available Datasets</h3>
              
              {/* Dataset List */}
              <div className="space-y-3">
                <div className="border border-gray-200 rounded-lg p-3 hover:border-blue-300 cursor-pointer transition-colors">
                  <div className="flex items-start justify-between">
                    <div>
                      <h4 className="font-medium text-sm text-gray-900">Electricity Access</h4>
                      <p className="text-xs text-gray-600 mt-1">Population with access to electricity</p>
                    </div>
                    <input type="checkbox" className="mt-1" />
                  </div>
                </div>
                
                <div className="border border-gray-200 rounded-lg p-3 hover:border-blue-300 cursor-pointer transition-colors">
                  <div className="flex items-start justify-between">
                    <div>
                      <h4 className="font-medium text-sm text-gray-900">Solar Potential</h4>
                      <p className="text-xs text-gray-600 mt-1">Solar irradiance and potential</p>
                    </div>
                    <input type="checkbox" className="mt-1" />
                  </div>
                </div>
                
                <div className="border border-gray-200 rounded-lg p-3 hover:border-blue-300 cursor-pointer transition-colors">
                  <div className="flex items-start justify-between">
                    <div>
                      <h4 className="font-medium text-sm text-gray-900">Grid Infrastructure</h4>
                      <p className="text-xs text-gray-600 mt-1">Power transmission and distribution</p>
                    </div>
                    <input type="checkbox" className="mt-1" />
                  </div>
                </div>
                
                <div className="border border-gray-200 rounded-lg p-3 hover:border-blue-300 cursor-pointer transition-colors">
                  <div className="flex items-start justify-between">
                    <div>
                      <h4 className="font-medium text-sm text-gray-900">Mini-grids</h4>
                      <p className="text-xs text-gray-600 mt-1">Mini-grid locations and capacity</p>
                    </div>
                    <input type="checkbox" className="mt-1" />
                  </div>
                </div>
              </div>
              
              <button 
                className="w-full mt-4 text-center text-sm text-blue-600 hover:text-blue-800 font-medium"
                onClick={() => {
                  // This would navigate to a dedicated datasets page or open a modal
                  // showing all available datasets with detailed information
                  console.log('Navigate to full datasets catalog');
                }}
              >
                View all datasets →
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LeftSidebar;