import { Landmark, Megaphone, ChartNoAxesCombined, PlugZap } from 'lucide-react'

function WhoThisIsFor() {
    const audience = [
        {
            icon: <Landmark className="w-8 h-8 text-blue-500" />, 
            title: "Government Planners",
            description: "Use real-time data to guide electrification projects, infrastructure expansion, and policy planning."
        }, 
        {
            icon: <ChartNoAxesCombined className="w-8 h-8 text-green-500" />,
            title: "NGOs and Researchers",
            description: "Access curated, open-access datasets for development planning, monitoring, and academi insights."
        }, 
        {
            icon: <PlugZap className="w-8 h-8 text-yellow-500" />,
            title:  "Clean Energy Startups",
            description: "Discover underserved areas, compare regions, and identify business opportunities for solar and mini-grids."
        }, 
        {
            icon: <Megaphone className="w-8 h-8 text-blue-950" />,
            title: "Community Advocates",
            description: "Explore localized data to support advocacy, funding requests, and project accountablity."
        },
    ];

    return (
        <section className="bg-white py-30 px-4 sm:px-6 lg:px-8">
            <div className="max-w-6xl mx-auto">
                <h2 className="text-2xl sm:text-3xl font-bold font-inter text-center text-gray-900 mb-10">Who this is for</h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                    {audience.map((item, idx) => (
                        <div key={idx} 
                            className="bg-white border border-gray-200 rounded-xl shadow-sm p-6 text-center transition hover:shadow-md hover:border-blue-500 hover:scale-105"
                        >
                            <div className="mb-4 flex justify-center">{item.icon}</div>
                            <div className="text-lg font-semibold mb-4">{item.title}</div>
                            <p className="text-gray-600">{item.description}</p>
                        </div>

                    ))}
                </div>
            </div>
        </section>
    )
}

export default WhoThisIsFor;