import { useEffect } from 'react';

import scrollAnimation from '../components/ScrollAnimation.jsx';

import assetImage from '../assets/asset/asset-1.jpeg'
import assetImage1 from '../assets/asset/asset-2.jpeg';
import assetImage2 from '../assets/asset/asset-3.jpg';
import assetImage3 from '../assets/asset/asset-4.jpg';

function GradientDivider(){
    return (
        <div className="h-[1px] w-3/4 mt-30 bg-gradient-to-r from-green-500 via-blue-500 to-pink-500 max-w-4xl mx-auto"></div>
    );
}

function AssetOwnership() {
    useEffect(()=> {
        window.scrollTo(0, 0);
    })

    const {ref: ref1, isVisible: isVisible1} = scrollAnimation();
    const {ref: ref2, isVisible: isVisible2} = scrollAnimation();   
    const {ref: ref3, isVisible: isVisible3} = scrollAnimation();

    return (
        <main>
            <section style={{backgroundImage: `url(${assetImage1})`}}
                    className="relative h-screen bg-cover bg-center flex justify-center items-center text-white"
            >
                <div className="absolute bg-black/60 inset-0"></div>
                <div className="relative z-10 text-center px-4 sm:px-6 lg:px-8 font-inter space-y-4 lg:space-y-7 max-w-4xl mx-auto">
                    <h1 className="text-3xl sm:text-5xl md:text-6xl lg:text-7xl font-bold tracking-wide md:traking-wider">Asset Ownership</h1>
                    <p className="text-base md:text-lg max-w-2xl mx-auto font-inter text-gray-300 font-medium">Tracking asset and home appliance ownership in Nigerian households</p>
                </div>

            </section>
            
        <GradientDivider />

        <section ref={ref1} className="py-6 lg:py-10">
            <div className="max-w-6xl mx-auto px-6">
                <div className="flex flex-col lg:flex-row gap-8">
                    <div className="flex-1 flex justify-center">
                        <img 
                            src={assetImage}
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
                        <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">DIGITAL CONNECTIVITY</h2>
                        <div className="font-inconsolata text-base text-gray-700">
                            <p className="mb-4">
                                Nigeria's digital adoption continues to expand. Internet connections reached 
                                103 million users in 2024, representing 45.5% of the population. And they 
                                were about 205 million active  lines as of 2024.
                            </p>
                            <p className="mb-4">
                                Smartphone penetration varies between urban and rural areas. 
                                According to GSMA data, urban Nigeria shows 59% smartphone penetration 
                                while rural areas lag at 26%. MTN Nigeria reports smartphone penetration grew to 55.9% 
                                overall by mid-2024. Statista projects smartphone users will reach 140 million in 2025.
                            </p>
                            <p>
                                
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
                            src={assetImage2}
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
                        <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">HOUSEHOLD APPLIANCES</h2>
                        <div className="font-inconsolata text-base text-gray-700">
                            <p className="mb-4">
                                Home appliance ownership reflects Nigeria's economic disparities and infrastructure challenges. 
                                Refrigerators and small kitchen utensils like blenders rank as the most commonly 
                                owned household items according to a 2023 Statista survey of Nigerian consumers.
                            </p>
                            <p className="mb-4">
                                About 70% of households in urban areas have TVs in their homes compared 
                                with 35% in rural areas. And approximately 40% of households in the country own 
                                standby generators. Generator dependency correlates with income 
                                levels and business ownership. Commercial enterprises show 
                                near-universal generator ownership while lower-income households 
                                often cannot afford backup power systems.
                            </p>
                            <p>
                               Nigeria's home appliance market was valued at $466.9 million in 2021 and is projected to 
                               reach $629.2 million by 2029, representing a 3.8% annual growth. Southern states show the 
                               highest appliance ownership rates based on 2020 regional studies. 
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
                            src={assetImage3}
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
                        <h2 className="mb-4 font-bold font-inter text-xl md:text-2xl">KEY STATISTICS</h2>
                        <div className="font-inconsolata text-base text-gray-700">
                            <p className="mb-4">
                                <strong>103 Million:</strong> Internet users in Nigeria as of 2024 (45.5% of the population).
                            </p>
                            <p className="mb-4">
                                <strong>205 Million:</strong> Active cell phone connections in 2024 (<a href="https://datareportal.com/reports/digital-2024-nigeria#:~:text=A%20total%20of%20205.4%20millioncellular%20mobile%20connections%20were,equivalent%20to%2090.7%20percentof%20the%20total%20population.%20ADVERTISEMENT">Data Reportal</a>)
                            </p>
                            <p className="mb-4">
                               <strong>140 Million:</strong> Projected smartphone users by 2025 (<a href="https://www.statista.com/statistics/467187/forecast-of-smartphone-users-in-nigeria/">Statista</a>)
                             </p>  
                             <p className="mb-4">
                                <strong>40%</strong>: Households owning standby generators.
                            </p>  
                            <p className="mb-4">
                                <strong>59%/</strong>: Urban vs rural smartphone penetration (GSMA)
                            </p>   
                            <p>
                                <strong>82%: </strong>Population covered by 4G networks (MTN Nigeria, 2024)
                            </p>              
                        </div>
                    </div>
                </div>
            </div>
            
        </section>
        </main>
    )
}

export default AssetOwnership;


