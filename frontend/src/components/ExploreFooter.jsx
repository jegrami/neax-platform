import { Link } from 'react-router-dom'

function ExploreFooter() {
    return (
        <footer className="bg-black text-white px-4 sm:px-6 md:px-8 pt-4 pb-16">
            <div className="text-center">
                <Link to="/data"
                    className="inline-block border px-6 py-2 rounded-full hover:border-green-500 hover:text-gray-300 font-roboto tracking-wide"

                >
                    EXPLORE DATA
                </Link>
            </div>
           <div className="h-[1px] mt-12 mb-16 w-3/4 mx-auto bg-gradient-to-r from-green-500 via-blue-500 to-pink-500 rounded-full" />

           <div className="space-x-5 text-center text-sm font-roboto uppercase">
                <a href="mailto:jegrami.dev@gmail.com" 
                    className="relative inline-block after:absolute after:left-0 after:-bottom-0.5 after:h-[1px] after:w-0 after:bg-green-500 after:transition-all after:duration-300 hover:after:w-full hover:text-gray-300"
                >
                    email
                </a>
                <a href="https://linkedin.com/in/jeremiah-igrami" 
                    className="relative inline-block after:absolute after:left-0 after:-bottom-0.5 after:h-[1px] after:w-0 after:bg-green-500 after:transition-all after:duration-300 hover:after:w-full hover:text-gray-300"
                >
                    linkedin
                </a>

                <a href="https://x.com/je_grami"
                    className="relative inline-block after:absolute after:left-0 after:-bottom-0.5 after:h-[1px] after:bg-green-500 after:transition-all after:duration-300 hover:after:w-full hover:text-gray-300"
                >
                    x
                </a>
                <a href="https://github.com//jegrami"
                    className="relative inline-block after:absolute after:left-0 after:-bottom-0.5 after:h-[1px] after:w-0 after:bg-green-500 after:transition-all after:duration-300 hover:after:w-full hover:text-gray-300"
                >
                    github
                </a>
           </div>

           <div className="text-center mt-8 font-light text-normal font-inconsolata"><span className="font-mindshine">&copy;</span> 2025 Nigeria Energy Access Explorer. All Rights Reserved</div>


        </footer>
    )
}

export default ExploreFooter;