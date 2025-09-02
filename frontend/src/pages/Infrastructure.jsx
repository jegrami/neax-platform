
import { useEffect } from 'react'
import scrollAnimation from '../components/ScrollAnimation.jsx'

import infraImage1 from '../assets/infra/infrastructure.jpg'
import infraImage2 from '../assets/infra/infra-2.jpg'
import infraImage3 from '../assets/infra/infra-3.jpg'
import infraImage4 from '../assets/infra/infra-4.jpg'
import infraImage5 from '../assets/infra/infra-5.jpg'


function GradientDivider(){
    return (
        <div className="h-[1px] w-3/4 mt-30 bg-gradient-to-r from-green-500 via-blue-500 to-pink-500 max-w-4xl mx-auto"></div>
    );
}

function Infrastructure(){
    useEffect(() => {
        window.scrollTo(0, 0);
    }, [])

    const { ref: ref1, isVisible: isVisible1 } = scrollAnimation();
    const { ref: ref2, isVisible: isVisible2 } = scrollAnimation();
    const { ref: ref3, isVisible: isVisible3 } = scrollAnimation();
    const { ref: ref4, isVisible: isVisible4 } = scrollAnimation();


    return (
        <main>
            <section style={{backgroundImage: `url(${infraImage1})`}}
                className="h-screen bg-center bg-cover text-center flex  justify-center items-center relative px-4 sm:px-6 lg:px-8 mb-30"
            >
                <div className="absolute inset-0 bg-black/40"></div>
                <div className="relative z-10 max-w-4xl mx-auto space-y-4 sm:space-y-7 font-inter">
                    <h1 className="text-3xl sm:text-5xl md:text-6xl lg:text-7xl text-white tracking-wide md:tracking-wider">Infrastructure</h1>
                    <p className="text-base sm:text-lg text-gray-300 tracking-tighter max-w-2xl mx-auto px-4 font-semibold">A closer look at Nigeria's energy infrastructure</p>
                </div>
            
            </section>

            <GradientDivider />

            <section ref={ref1} className="py-6 lg:py-10">
                <div className="max-w-6xl mx-auto px-6">
                    <div className="flex flex-col lg:flex-row gap-8">
                        <div className="flex-1 flex justify-center">
                            <img 
                                src={infraImage2}
                                alt="Infrastructure image 1"
                                className={
                                    `w-full max-w-md h-80 obect-cover transition-all duration-700 ease-out ${isVisible1 ? 'scale-100 opacity-100' : 'scale-85 opacity-0' } `
                                }
                            />
                        </div>
                        <div className={
                                `flex-1 transition-all duration-700 ease-out delay-200 ${isVisible1 ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'}` 
                            }
                        >
                            <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">NATIONAL SNAPSHOT</h2>
                            <div className="font-inconsolata text-base text-gray-700">
                                <p className="mb-4">
                                    Nigeria operates 14 GW installed capacity but delivers only 4.14 GW daily. 
                                    The transmission network spans 20,000 km with 800+ substations managed by TCN.
                                </p>
                                <p>The country has 28 grid connected power plants. Distribution covers all 36 states through 11 DisCos and reaches 70% of the population.
                                   Grid coverage concentrates in urban areas, leaving rural communities underserved.
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
                                src={infraImage3}
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

                            <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">THE GRID</h2>
                            <div className="font-inconsolata text-base text-gray-700">
                                <p className="mb-4">
                                    <strong>Transmission:</strong> The Transmission Company of Nigeria manages the national 
                                    grid at 330kV and 132kV levels. The Radial distribution system design creates vulnerability 
                                    to cascading failures, unlike the Ring Main or looped systems that provide redundancy.
                                </p>
                                <p className="mb-4">
                                    <strong>Distribution:</strong> Eleven DisCos deliver power to end-users through poles, transformers, and feeders. 
                                    Only about 57% of customers have meters. This ceates billing opacity and planning challenges.
                                </p>
                                <p className="mb-4"><strong>Substations:</strong> Over 800 substations handle voltage stepping and grid control. 
                                    Most require upgrades for modern load and safety standards.
                                </p>
                                <p><strong>Monitoring:</strong> SCADA systems are rolling out for real-time monitoring, 
                                    but most grid infrastructure lacks modern automation.
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
                                src={infraImage4}
                                alt="Infrastructure image 3"
                                className={
                                    `w-full max-w-md h-80 object-cover transition-all duration-700 ease-out ${isVisible3 ? 'scale-100 opacity-100' : 'scale-85 opacity-0'}`
                                }
                            />
                        </div>
                        <div className={
                            `flex-1 transition-all duration-700 ease-out delay-200 ${isVisible3 ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'}`
                            }
                        >

                            <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">INFRASTRUCTURE GAPS & PRIORITIES</h2>
                            <div className="font-inconsolata text-base text-gray-700">
                                <p className="mb-4">
                                    Grid unreliability plagues the system with frequent outages and 15-20% transmission losses.
                                    Aging infrastructure, particularly distribution components over 30 years old, creates
                                    maintenance backlogs.
                               </p>
                               <p>
                                    Only 40% of generated electricity reaches end-users due to infrastructural constraints.
                                    Rural exclusion persists in remote villages where grid extension isn't economically viable.    
                                </p>  
                                
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <GradientDivider />

            <section ref={ref4} className="py-6 lg:py-8 mb-20">
                <div className="max-w-6xl mx-auto px-6">
                    <div className="flex flex-col lg:flex-row gap-8">
                        <div className="flex-1 flex justify-center">
                            <img 
                                src={infraImage5}
                                alt="Infrastructure image2"
                                className={
                                    `w-full max-w-md h-80 object-cover transition-all duration-700 ease-out ${isVisible4 ? 'scale-100 opacity-100' : 'scale-85 opacity-0'}`
                                }
                            />
                        </div>
                        <div className={
                            `flex-1 transition-all duration-700 ease-out delay-200 ${isVisible4 ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'}`
                            }
                        >

                            <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">WHY INFRASTRUCTURE MATTERS</h2>
                            <div className="font-inconsolata text-base text-gray-700">
                                <p className="mb-4">
                                    Reniable power drives economic growth through manufacturing, digital economies, 
                                    and small business support. Robust energy infrastructure ensures that schools can 
                                    operate effectively, hospitals can deliver critical care, and communities can access 
                                    essential services. Security systems, from street lighting to surveillance, 
                                    rely on consistent power to keep citizens safe.


                               </p>
                               <p>
                                    Detailed data on Nigeria’s energy infrastructure is vital for building smarter, 
                                    more resilient grids that integrate renewable energy and withstand climate-driven 
                                    challenges. This dataset provides actionable insights to drive informed decisions and 
                                    foster sustainable development and a more connected Nigeria.
                               </p>  
                                
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </main>
    )
}

export default Infrastructure;