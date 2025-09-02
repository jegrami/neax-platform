import heroImage from '../assets/neax-hero.jpg'
import heroImage1 from '../assets/hero-bg-1.jpg'


function Hero(){
    return (
        <section 
            className="relative h-screen w-full bg-cover bg-center bg-no-repeat"
            style={{backgroundImage: `url(${heroImage1})`}}
        >
            {/* Dark overlay */}
            <div className="absolute inset-0 bg-black/80"></div>
            
            {/* Hero content */}
            <div className="relative z-10 flex items-center justify-center h-full px-6 sm:px-12">
                <div className="text-center max-w-4xl">
                    <h1 className="text-4xl sm:text-6xl lg:text-7xl font-bold mb-6 font-inter text-white leading-tight">
                        <span className="block text-green-400">Shining a light on</span>
                        <span className="block text-blue-100">Nigeria's energy landscape</span>
                    </h1>
                    
                    <p className="text-xl sm:text-2xl text-gray-200 mb-8 font-light max-w-2xl mx-auto">
                        Discover comprehensive data and insights about Nigeria's energy infrastructure and access patterns
                    </p>

                    <a 
                        href="/data" 
                        className="inline-block bg-gradient-to-r from-green-500 to-blue-500 hover:from-green-400 hover:to-blue-400 px-8 py-4 text-lg font-semibold rounded-lg text-white transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
                    >
                        Explore Data →
                    </a>
                </div>
            </div>
        </section>
    )
}

export default Hero;