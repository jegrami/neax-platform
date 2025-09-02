import { Link } from 'react-router-dom'

import solarImage from '../assets/solar/solar-1.jpg'
import electricityImage from '../assets/electric/electricity.jpg'
import generatorImage from '../assets/genuse/generator.jpg'
import energyImage from '../assets/infra/infra-2.jpg'
import assetsImage from '../assets/asset/asset-2.jpeg'
import minigridImage from '../assets/minigrid/minigrid.jpg'

const exploreItems = [
    {
        title: 'Electricity Access',
        subtitle: 'Grids, mini-grids, and underserved communities',
        image: electricityImage,
        link: '/explore/electricity',
    },
    {
        title: 'Asset Ownership',
        subtitle: 'Fridge, TV, clean cooking stove, smartphone, satellite dish & more',
        image: assetsImage,
        link: '/explore/assets',
    }, 
    {
        title: 'Mini Grids',
        subtitle: 'Rural and renewable power solutions',
        image: minigridImage,
        link: '/explore/minigrids',

    }, 
    {
        title: 'Solar Potential',
        subtitle: 'Regions with the highest solar energy potential',
        image: solarImage,
        link: '/explore/solar',
    },
    {
        title: 'Generator Usage',
        subtitle: "Nigeria's fuel dependence by region",
        image: generatorImage,
        link: '/explore/generator',
    }, 
    {
        title: 'Energy Infrastructure',
        subtitle: "Transmission lines, power plants, mini-grids",
        image: energyImage,
        link: '/explore/infrastructure',
    },
];

function WhatYouCanExplore() {
    return (
        <section className="bg-white py-30 px-4 sm:px-6 lg-px-8"> 
            <div className="max-w-6xl mx-auto">
                <h2 className="text-2xl sm:text-3xl font-bold font-inter mb-10 text-gray-900 text-center">What you can explore</h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                    {exploreItems.map((item, index) => (
                        <Link 
                            key={index}
                            to={item.link}
                            className="relative h-56 rounded-xl overflow-hidden shadow hover:shadow-lg transition group"
                         >
                            <img 
                                src={item.image} 
                                alt={item.title}
                                className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                            />
                            <div className="absolute inset-0 bg-black/70 group-hover:bg-black/80 transition"></div>
                            <div className="relative z-10 p-4 text-white flex flex-col justify-end h-full">
                                <h3 className="text-lg font-bold">{item.title}</h3>
                                <p className="text-base">{item.subtitle}</p>
                                <p className="text-[12px] text-gray-100 mt-2 hover:text-gray-300">Click to learn more</p>
                            </div>
                            

                        </Link>

                    ))}
                </div>
            </div>
        </section>
    )
}


export default WhatYouCanExplore;