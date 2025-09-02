
import { useEffect } from 'react'

import studentImage from '../assets/student-studying.webp'
import electricityImage from  '../assets/electric/electimage.jpg'
import electricityImage1 from '../assets/electric/electimage-1.jpg'
import electricityImage2 from '../assets/electric/electimage-2.jpg'
import electricityImage3 from '../assets/electric/electimage3.jpeg'


function ElectricityAccess(){
    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    return (
        <main>
            <section style={{backgroundImage: `url(${electricityImage})`}} 
                    className=" py-12 sm:py-20 px-4 sm:px-6 text-center bg-cover bg-center h-screen relative flex justify-center items-center"
            >
                <div className="absolute inset-0 bg-black/60"></div>
                <div className="max-w-4xl mx-auto space-y-4 md:space-y-7 z-10 relative">
                    <h1 className="text-3xl sm:text-5xl md:text-6xl lg:text-7xl tracking-wide lg:tracking-wider text-white font-bold font-inter">Electricity</h1>
                    <p className="text-gray-300 font-inter font-medium text-base md:text-lg tracking-tighter mx-w-2xl">Tracking household electricity connection accross the nation</p>
                </div>
                
            </section>

            <section style={{backgroundImage: `url(${electricityImage2})`}}
                    className="bg-cover bg-center w-full h-screen relative flex items-center justify-end"
            >
                <div className="absolute inset-0 bg-black/50"></div>
                <div className="flex flex-col text-gray-200 z-10 relative pt-30 px-4 sm:px-6 lg:px-8 max-w-xl lg:mr-10">
                    <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">THE CHALLENGE</h2>
                    <div className="text-base font-inconsolata">
                        <p className="mb-4">Nigeria has the world's largest energy access gap. With 227 million people,
                        about 70% have access to electricity, leaving about 80 million
                        stil without power. 

                    </p>
                    <h3 className="mb-1 font-semibold">Urban vs Rural Divide
                        <span className="block text-sm font-medium text-gray-300 mb-1">Urban areas: 95% connected | Rural communities: 40% connected</span>
                    </h3>
                    <p>Nigeria's electricity story is two different realities. 
                        Cities enjoy near-universal access while rural areas remain largely
                        diconnected from the grid. Some city neighborhoods enjoy 20&ndash;23 hours 
                        power while others in the same city experience several blackouts daily.
                        
                    </p>
                    </div>
                </div>

            </section>
            <section style={{backgroundImage: `url(${electricityImage1})`,
                            
                            transform: 'scaleX(-1)'
                    }}
                    className="relative h-screen w-full flex bg-cover bg-center items-center"
            >
                <div className="absolute inset-0 bg-black/40 scale-x-[-1]"></div>
                <div className="relative z-10 scale-x-[-1] text-gray-200 flex flex-col max-w-xl px-4 sm:px-6 lg:px-8">
                    <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">KEY INSIGHTS</h2>
                    <div className="font-inconsolata text-base">
                        <p className="mb-2"><strong>80 Million:</strong> number of people who still lack access to electricity.</p>
                        <p className="mb-2"><strong>70% Connected:</strong> the overall assess rate&mdash;fewer homes have relaible supply.</p>
                        <p className="mb-2"><strong>Rural Disadvantage:</strong> only 40% of rural households have electricity, compared to 150% urban coverage.</p>
                        <p className="mb-2"><strong>Consumption Pattern:</strong> in 2020, residential sector consumed around 59,000 terajoules of electricity, versus the 14,000 terajoules consumed by by industries.</p>
                        <p><strong>Export Revenue:</strong> Nigeria earned $155 million from electricity exports in 2022.</p>
                    </div>
                </div>
                
            </section>
            <section style={{backgroundImage: `url(${electricityImage3})`}}
                    className="h-screen w-full bg-cover bg-center relative flex items-center justify-end"
             >
                <div className="absolute inset-0 bg-black/70"></div>
                <div className="relative flex flex-col max-w-xl px-4 sm:px-6 lg:px-8 text-gray-200 z-10">
                    <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">WHY THIS MATTERS</h2>
                    <div className="font-inconsolata text-base md:text-lg">
                        <p className="mb-4">Electricity access drives economic development, education, healthcare, and social inclusion.
                            Data fousing of national averages often mask the stark disparity that exists between
                            states, urban&ndash;rural areas, and even neighborhoods within cities.
                        </p>
                        <p>This dataset tracks household electricity connections nationwide, revealing 
                            disparities that aggregate statistics often hide. Understanding these patterns 
                            is essential for targeted infrastructure investment and policy development.
                        </p>
                    </div>
                </div>

            </section>
            
        </main>
    )
}

export default ElectricityAccess;