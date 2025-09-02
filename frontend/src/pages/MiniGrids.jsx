import { useEffect } from 'react'

import scrollAnimation from '../components/ScrollAnimation.jsx'

import mgridImage from '../assets/minigrid/minigrid.jpg'
import mgridImage1 from '../assets/minigrid/minigrid-1.jpg'
import mgridImage2 from '../assets/minigrid/minigrid-2.jpg'
import mgridImage3 from '../assets/minigrid/minigrid-3.jpg'

function GradientDivider(){
    return (
        <div className="h-[1px] w-3/4 mt-30 bg-gradient-to-r from-green-500 via-blue-500 to-pink-500 max-w-4xl mx-auto"></div>
    );
}

function MiniGrid() {
    useEffect(() => {
        window.scrollTo(0, 0);
    }, [])

    const {ref: ref1, isVisible: isVisible1} = scrollAnimation();
    const {ref: ref2, isVisible: isVisible2} = scrollAnimation();
    const {ref: ref3,  isVisible: isVisible3} = scrollAnimation();
    const {ref: ref4,  isVisible: isVisible4} = scrollAnimation();

    return (
        <main>
            <section style={{backgroundImage: `url(${mgridImage})`}}
                    className="relative h-screen bg-cover bg-center flex justify-center items-center px-4 sm:px-6 lg:px-8"
            >
                <div className="absolute bg-black/60 inset-0"></div>
                <div className="relative z-10 max-w-4xl mx-auto space-y-4 sm:space-y-7 font-inter">
                    <h1 className="text-3xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-white tracking-wide md:tracking-wider">Mini Grids</h1>
                    <p className="text-base sm:text-lg text-gray-300 tracking-tighter max-w-2xl font-semibold mx-auto px-4">The landscape of decentralized energy solutions</p>
                </div>

            </section>

            <GradientDivider />

            <section ref={ref1} className="py-6 lg:py-8">
                <div className="max-w-6xl mx-auto px-6">
                    <div className="flex flex-col lg:flex-row gap-8">
                        <div className="flex-1 flex justify-center">
                            <img 
                                src={mgridImage1}
                                alt="Infrastructure image 4"
                                className={
                                    `w-full max-w-md h-80 object-cover transition-all duration-700 ease-out ${isVisible1 ? 'scale-100 opacity-100' : 'scale-85 opacity-0'}`
                                }
                            />
                        </div>
                        <div className={
                            `flex-1 transition-all duration-700 ease-out delay-200 ${isVisible1 ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'}`
                            }
                        >

                            <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">THE REALITY CHECK</h2>
                            <div className="font-inconsolata text-base text-gray-700">
                                <p className="mb-4">
                                    Most electrification programs focus on extending the national grid. But 
                                    areas without electricity are remote villages with sparse population, so grid-extension is 
                                    often a costly solution to implement. Decentralized Renewable Energy (DRE), however, 
                                    has proved to be a better solution for solving electricity access problem in 
                                    remote villages. 
                                </p>
                                <p className="mb-4">
                                    Minigrids can be deployed faster and at a lower cost than grid-extension.
                                    They are a better business model that attracts investment from private and 
                                    public sectors. There are also more relaible and can be deployed in a variety of use cases.
                                    
                                </p>
                                <p className="mb-4">
                                    According to the <a href="https://www.irena.org/Publications/2025/Jun/Tracking-SDG-7-The-Energy-Progress-Report-2025" target="_blank" rel="noopener noreferrer">Energy Progress Report 2025</a>, mini-grids in Nigeria have
                                    connected connected nearly 6 million people through more than 170 mini-grids 
                                    and almost 1.2 million stand-alone solar systems. DRE solutions as 
                                    viable for solving Nigeria's electricity crises.
                                    
                                </p>
                                
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <GradientDivider />

            <section ref={ref2} className="py-6 lg:py-8">
                <div className="max-w-6xl mx-auto px-6">
                    <div className="flex flex-col lg:flex-row gap-8">
                        <div className="flex-1 flex justify-center">
                            <img 
                                src={mgridImage2}
                                alt="Infrastructure image 4"
                                className={
                                    `w-full max-w-md h-80 object-cover transition-all duration-700 ease-out ${isVisible2 ? 'scale-100 opacity-100' : 'scale-85 opacity-0'}`
                                }
                            />
                        </div>
                        <div className={
                            `flex-1 transition-all duration-700 ease-out delay-200 ${isVisible2 ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'}`
                            }
                        >

                            <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">MARKET OPPORTUNITY</h2>
                            <div className="font-inconsolata text-base text-gray-700">
                                <p className="mb-4">
                                    The numbers are promising. <a  href="https://www.tdworld.com/grid-innovations/distribution/article/20971606/report-shows-us20-billion-investment-opportunity-for-nigeria-in-scaling-minigrids " target="_blank" rel="noopener noreferrer">A 2018 report by T&D World</a> shows a 
                                    $20 billion investment opportunity for Nigeria in scaling minigrids. 
                                    Rural businesses are desperate for reliable power. 
                                </p>
                                <p className="mb-4">
                                   Before minigrids, market stall owners received only 6–8 hours of power each day.
                                    Now, a 1 MW solar minigrid with battery storage can power entire markets, 
                                    providing reliable and silent power.
                                    
                                </p>
                                <p>In 2023, the federal government, through the Rural Electrification
                                    Agency, comissioned a 352 kW interconnected minigrid that provides
                                    electricity to more than 2,000 households and 141 commercial users in 
                                    a rural community in Nasarawa state. One connection, thousands of 
                                    houses.

                                </p>
                                
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <GradientDivider />

            <section ref={ref3} className="py-6 lg:py-8">
                <div className="max-w-6xl mx-auto px-6">
                    <div className="flex flex-col lg:flex-row gap-8">
                        <div className="flex-1 flex justify-center">
                            <img 
                                src={mgridImage3}
                                alt="Infrastructure image 4"
                                className={
                                    `w-full max-w-md h-80 object-cover transition-all duration-700 ease-out ${isVisible3 ? 'scale-100 opacity-100' : 'scale-85 opacity-0'}`
                                }
                            />
                        </div>
                        <div className={
                            `flex-1 transition-all duration-700 ease-out delay-200 ${isVisible3 ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'}`
                            }
                        >

                            <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">KEY INSIGHTS</h2>
                            <div className="font-inconsolata text-base text-gray-700">
                                <p className="mb-4">
                                    <strong>170 units</strong> of minigrids already established through recent programs.
                                </p>
            
                                <p className="mb-4">
                                    <strong>6 milllion</strong> Nigerians so far have been connected to power  
                                    through minigrids. 
                                    
                                </p>
                                <p className="mb-4">
                                    <strong>59%:</strong>  Share of solar PV in minigrids as of 2024 (up from 14% in 2018)
                                </p>
                                <p>
                                    <strong>300,000:</strong> Target households for rural electrification through minigrids.
                                </p>
                                
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <GradientDivider />

            <section ref={ref4} className="py-6 lg:py-8">
                <div className="max-w-6xl mx-auto px-6">
                    <div className="flex flex-col lg:flex-row gap-8">
                        <div className="flex-1 flex justify-center">
                            <img 
                                src={mgridImage}
                                alt="Infrastructure image 4"
                                className={
                                    `w-full max-w-md h-80 object-cover transition-all duration-700 ease-out ${isVisible4 ? 'scale-100 opacity-100' : 'scale-85 opacity-0'}`
                                }
                            />
                        </div>
                        <div className={
                            `flex-1 transition-all duration-700 ease-out delay-200 ${isVisible4 ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'}`
                            }
                        >

                            <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">WHY THIS MATTERS</h2>
                            <div className="font-inconsolata text-base text-gray-700">
                                <p className="mb-4">
                                    Minigrids are the fastest path to universal electricity access in Nigeria. 
                                    They can reach remote areas where grid extension is uneconomical.
                                </p>
            
                                <p className="mb-4">
                                    The dataset reveals where minigrids are deployed, their capacity, 
                                    technology mix, and performance. It shows which business models work 
                                    and which don't. For investors, developers, and policymakers, 
                                    this data is essential for scaling success.
                                    
                                </p>
                                
                            </div>
                        </div>
                    </div>
                </div>
            </section>

        </main>

    )
}

export default MiniGrid;

