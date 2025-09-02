import { useState, useEffect, useRef } from 'react';
import scrollAnimation from '../components/ScrollAnimation';

import solar1 from '../assets/solar/solar-1.jpg'
import solar2 from '../assets/solar/solar-2.jpg'
import solar3 from '../assets/solar/solar-3.jpeg'
import solar4 from '../assets/solar/solar-4.jpg'
import solar5 from '../assets/solar/solar-5.jpg'

function GradientDivider(){
    return (
        <div className="h-[1px] w-3/4 mt-30 bg-gradient-to-r from-green-500 via-blue-500 to-pink-500 max-w-4xl mx-auto"></div>
    );
}

function SolarPotential(){
    useEffect(() => {
        window.scrollTo(0, 0);
    }, [])

    const {ref: ref1, isVisible: isVisible1} = scrollAnimation();
    const {ref: ref2, isVisible: isVisible2} = scrollAnimation();
    const {ref: ref3, isVisible: isVisible3} = scrollAnimation();
    const {ref: ref4, isVisible: isVisible4} = scrollAnimation();

    return (
        <main>
          <section style={{backgroundImage: `url(${solar1})`}}
                className="relative h-screen bg-cover bg-center flex text-center justify-center items-center px-4 sm:px-6 lg-px-8 mb-30"
          >
            <div className="absolute bg-black/40 inset-0"></div>
            <div className="relative z-10 max-w-4xl mx-auto space-y-4 md:space-y-7 font-inter">
                <h1 className="text-3xl sm:text-5xl md:text-6xl lg:text-7xl text-white font-bold traking-wide md:traking-wider lg:tracking-widest">Solar</h1>
                <p className="text-base md:text-lg max-w-2xl mx-auto px-4 text-gray-300 tracking-tighter">A look into Nigeria's solar energy potential</p>
            </div>

          </section> 

          <GradientDivider />

          <section ref={ref1} className="py-6 lg:py-10">
            <div className="max-w-6xl mx-auto px-6">
                <div className="flex flex-col lg:flex-row gap-8">
                    <div className="flex flex-1 justify-center">
                        <img src={solar2} 
                            className={
                                `w-full max-w-md h-80 object-cover transition-all duration-700 ease-out ${isVisible1 ? 'scale-100 opacity-100' :'scale-85 opacity-0'}`
                            }
                        />
                    </div>
                    <div className={
                        `flex-1 transition-all duration-700 ease-out delay-200 ${isVisible1 ? 'translate-y-0 opacity-100': 'translate-y-5 opacity-0'}`
                        }
                    >
                        <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">THE OPPORTUNITY</h2>
                        <div className="font-inconsolata text-base text-gray-700">
                            <p className="mb-4">
                                Nigeria is a solar powerhouse. We have an average of 6.5 hours of daily sunshine,
                                and solar radiaiton in the north can reach up to 7kwh/m<sup>2</sup>/day. 
                            </p>
                            <p className="mb-4">
                                The country recieves enough sunlight to generate 1,770 TWh annually, nearly 50 times its 2023 
                                electricity consumption. Despite this, solar currently accounts for only 1.6% of Nigeria's 
                                energy mix. This dataset reveals untapped potential to transform Nigeria’s energy landscape.
                            </p>
                            <p>The growth trajectory is promising. Solar capacity jumped from 1.5 MW in 2015 to over 150 MW in 2022. 
                               That's 100x growth in seven years. The momentum exists, but scale remains the challenge.
                            </p>
                        </div>
                    </div>

                </div>
            </div>
          </section> 

          <GradientDivider />

           <section ref={ref2} className="py-6 lg:py-10">
            <div className="max-w-6xl mx-auto px-6">
                <div className="flex flex-col lg:flex-row gap-8">
                    <div className="flex flex-1 justify-center">
                        <img src={solar3} 
                            className={
                                `w-full max-w-md h-80 object-cover transition-all duration-700 ease-out ${isVisible2 ? 'scale-100 opacity-100' :'scale-85 opacity-0'}`
                            }
                        />
                    </div>
                    <div className={
                        `flex-1 transition-all duration-700 ease-out delay-200 ${isVisible2 ? 'translate-y-0 opacity-100': 'translate-y-5 opacity-0'}`
                        }
                    >
                        <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">THE GRID ALTERNATIVE</h2>
                        <div className="font-inconsolata text-base text-gray-700">
                            <p className="mb-4">
                                Solar offers a solution to Nigeria's electricity crisis that doesn't require massive grid expansion. 
                                Nigeria's renewable energy market is projected to grow from 3.13 gigawatts in 2024 to 
                                5.01 gigawatts by 2029, with a compound annual growth rate of 9.88%.
                            </p>
                            <p className="mb-4">
                                Mini-grids and distributed solar can reach the 80 million people without power 
                                faster than extending the national grid. Rural areas with 40% electricity access 
                                could leapfrog to solar-powered systems. The technology exists, the sun is free, 
                                and the need is urgent.
                            </p>
                            
                        </div>
                    </div>

                </div>
            </div>
          </section> 

          <GradientDivider />

          <section ref={ref3} className="py-6 lg:py-10">
            <div className="max-w-6xl mx-auto px-6">
                <div className="flex flex-col lg:flex-row gap-8">
                    <div className="flex flex-1 justify-center">
                        <img src={solar4} 
                            className={
                                `w-full max-w-md h-80 object-cover transition-all duration-700 ease-out ${isVisible3 ? 'scale-100 opacity-100' :'scale-85 opacity-0'}`
                            }
                        />
                    </div>
                    <div className={
                        `flex-1 transition-all duration-700 ease-out delay-200 ${isVisible3 ? 'translate-y-0 opacity-100': 'translate-y-5 opacity-0'}`
                        }
                    >
                        <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">KEY INSIGHTS</h2>
                        <div className="font-inconsolata text-base text-gray-700">
                            <p className="mb-4">
                                <strong>385.7MWp:</strong> current installed solar capacity, which barely scratches the surface.
                            </p>
                            <p className="mb-4">
                                <strong>5.44 kWh/m2:</strong> average daily solar irradiation across the country.
                            </p>
                            <p><strong>1500 × 109 MWh:</strong> annual solar radiation received, 
                                enough to power the continent.
                            </p>
                            <p><strong>9.88%:</strong> annual growth rate projected for renewable energy through 2029.</p>
                            <p><strong>Cost Advantage: </strong>Global solar costs are now $0.80/W, 
                            making large-scale projects in Nigeria highly viable.
                            </p>
                            
                        </div>
                    </div>

                </div>
            </div>
          </section> 

          <GradientDivider />

          <section ref={ref4} className="py-6 lg:py-10 mb-20">
            <div className="max-w-6xl mx-auto px-6">
                <div className="flex flex-col lg:flex-row gap-8">
                    <div className="flex flex-1 justify-center">
                        <img src={solar5} 
                            className={
                                `w-full max-w-md h-80 object-cover transition-all duration-700 ease-out ${isVisible4 ? 'scale-100 opacity-100' :'scale-85 opacity-0'}`
                            }
                        />
                    </div>
                    <div className={
                        `flex-1 transition-all duration-700 ease-out delay-200 ${isVisible4 ? 'translate-y-0 opacity-100': 'translate-y-5 opacity-0'}`
                        }
                    >
                        <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">WHY THIS MATTERS</h2>
                        <div className="font-inconsolata text-base text-gray-700">
                            <p className="mb-4">
                                Nigeria's solar potential could transform its energy landscape. 
                                The data reveals where to build, what capacity to expect, and which regions offer the best returns.
                            </p>
                            <p className="mb-4">
                                This dataset maps Nigeria's solar resources with precision. 
                                 It shows irradiation levels, seasonal variations, and generation potential across 
                                 all states. The numbers don't lie. Nigeria has world-class solar resources waiting 
                                 to be unlocked.
                            </p>
                            
                        </div>
                    </div>

                </div>
            </div>
          </section> 
        </main>
    )

}

export default SolarPotential;