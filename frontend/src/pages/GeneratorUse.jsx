import { useEffect } from 'react';

import scrollAnimation from '../components/ScrollAnimation'

import genImage from '../assets/genuse/generator.jpg';
import genImage1 from '../assets/genuse/gen-1.jpg';
import genImage2 from '../assets/genuse/gen-2.jpg';
import genImage3 from '../assets/genuse/gen-3.jpg';

function GradientDivider(){
    return (
        <div className="h-[1px] w-3/4 mt-30 bg-gradient-to-r from-green-500 via-blue-500 to-pink-500 max-w-4xl mx-auto"></div>
    );
}

function GeneratorUse() {
    useEffect(()=> {
        window.scrollTo(0, 0);
    }, [])

    const {ref:  ref1, isVisible: isVisible1} = scrollAnimation();
    const {ref: ref2, isVisible: isVisible2} = scrollAnimation();
    const {ref:  ref3, isVisible: isVisible3} = scrollAnimation();



   return (
    <main>
        <section style={{backgroundImage: `url(${genImage})`}}
                className="relative h-screen bg-cover  bg-center flex justify-center items-center text-white"
        >
            <div className="absolute bg-black/60 inset-0"></div>
            <div className="relative z-10 text-center px-4 sm:px-6 lg:px-8 font-inter space-y-4 lg:space-y-7 max-w-4xl mx-auto">
                <h1 className="text-3xl sm:text-5xl md:text-6xl lg:text-7xl font-bold  tracking-wide md:tracking-wider">Generator Use</h1>
                <p className="text-base text-gray-300 md:text-lg max-w-2xl font-semibold">Tracking Nigeria's standby generator market</p>
            </div>
            
        </section>

        <GradientDivider />

        <section ref={ref1} className="py-6 lg:py-10">
            <div className="max-w-6xl mx-auto px-6">
                <div className="flex flex-col lg:flex-row gap-8">
                    <div className="flex-1 flex justify-center">
                        <img 
                            src={genImage1}
                            alt="Generator image "
                            className={
                                `w-full max-w-md h-80 obect-cover transition-all duration-700 ease-out ${isVisible1 ? 'scale-100 opacity-100' : 'scale-85 opacity-0' } `
                            }
                        />
                    </div>
                    <div className={
                            `flex-1 transition-all duration-700 ease-out delay-200 ${isVisible1 ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'}` 
                        }
                    >
                        <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">MARKET SIZE AND OWNERSHIP</h2>
                        <div className="font-inconsolata text-base text-gray-700">
                            <p className="mb-4">
                                Nigeria dominates Africa's generator market. The country accounts for 46% of all generators sold 
                                in Sub-Saharan Africa, and more than 40% of Nigerian households own and use a generator. 
                                The business sector shows even higher reliance on standby generators, as 86% of Nigerian companies 
                                own or share a generator.
                            </p>
                            <p className="mb-4">
                                Generator ownership reflects Nigeria's electricity reality. While the national grid 
                                serves millions, frequent outages and unreliable supply force households and 
                                businesses to invest in backup power. Nigeria ranks as the largest user of oil-fired
                                backup generators on the continent. 
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
                    <div className="flex-1 flex justify-center">
                        <img 
                            src={genImage3}
                            alt="Generator image 2"
                            className={
                                `w-full max-w-md h-80 obect-cover transition-all duration-700 ease-out ${isVisible2 ? 'scale-100 opacity-100' : 'scale-85 opacity-0' } `
                            }
                        />
                    </div>
                    <div className={
                            `flex-1 transition-all duration-700 ease-out delay-200 ${isVisible2 ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'}` 
                        }
                    >
                        <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">FUEL CONSUMPTION PATTERNS</h2>
                        <div className="font-inconsolata text-base text-gray-700">
                            <p className="mb-4">
                                The generator market creates massive fuel demand.  2022 report by Stears and Sterling states that households 
                                in Nigeria spend about $14bn annually to fuel their generators.
                            </p>
                            <p className="mb-4">
                                Diesel generators dominate commercial applications due to their efficiency 
                                and fuel economy. Smaller petrol generators serve residential needs and small businesses. 
                                The fuel costs add up quickly. A typical 5kW diesel generator consumes about 2-3 liters per 
                                hour, meaning daily operating costs can exceed the monthly income of many Nigerians.
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
                    <div className="flex-1 flex justify-center">
                        <img 
                            src={genImage2}
                            alt="Infrastructure image 1"
                            className={
                                `w-full max-w-md h-80 obect-cover transition-all duration-700 ease-out ${isVisible3 ? 'scale-100 opacity-100' : 'scale-85 opacity-0' } `
                            }
                        />
                    </div>
                    <div className={
                            `flex-1 transition-all duration-700 ease-out delay-200 ${isVisible3 ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'}` 
                        }
                    >
                        <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">ECONOMIC IMPLICATIONS</h2>
                        <div className="font-inconsolata text-base text-gray-700">
                            <p className="mb-4">
                                The generator market represents both opportunity and economic burden. 
                                Local assembly operations provide jobs, but most components remain imported. 
                                The maintenance and repair sector employs thousands of technicians across the country.
                            </p>
                            <p className="mb-4">
                                But the economic costs are substantial. Businesses pass generator 
                                operating costs to consumers through higher prices. The noise pollution, 
                                air quality impacts, and carbon emissions create additional social costs. 
                                Generator-dependent businesses struggle to compete with companies in countries with 
                                reliable grid electricity.
                            </p>
                            <p>
                                The generator use data reveal where grid failures occur most frequently, which 
                                sectors depend most heavily on backup power, and how fuel costs impact different 
                                regions and industries. This information guides infrastructure investment decisions,
                                 policy development, and business planning.
                             </p>                     
                        </div>
                    </div>
                </div>
            </div>
            
        </section>

    </main>
   ) 
}

export default GeneratorUse;


