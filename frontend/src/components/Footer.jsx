

function Footer() {
    return (
        <footer className="bg-black px-4 sm:px-6 md:px-8 pt-10 pb-8 text-white">
            <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-around items-center font-inconsolata">
                <div classname="mb-2 text-gray-400 font-light">
                    <h2 className="mb-2 text-gray-400 font-light">COMPANY</h2>
                    <a href="/about"
                        className="relative inline-block after:absolute after:left-0 after:-bottom-0.5 after:h-[1px] after:w-0 after:bg-green-500 after:transition-all after:duration-300 hover:after:w-full hover:text-gray-300"
                    >
                        About
                    </a>
                
                </div>
                <div>
                    <h2 className="mb-2 text-gray-400 font-light">DATA SOURCES</h2>
                    <p></p>
                    <p></p>
                </div>
                
                <div className="">
                    <h2 className="mb-2 text-gray-400 font-light">CONTACT</h2>
                    
                        <p>
                            <a href="mailto:jegrami.dev@gmail.com"
                            className="relative inline-block after:absolute after:left-0 after:-bottom-0.5 after:h-[1px] after:w-0 after:bg-green-500 after:transition-all after:duration-300 hover:after:w-full hover:text-gray-300"
                            >
                                Email

                            </a>
                        </p>

                        <p>
                            <a href="https://linkedin.com/in/jeremiah-igrami"
                            className="relative inline-block after:absolute after:left-0 after:-bottom-0.5 after:h-[1px] after:w-0 after:bg-green-500 after:transition-all after:duration-300 hover:after:w-full hover:text-gray-300"
                            >
                                LinkedIn
                            </a>
                        </p>

                        <p>
                            <a href="https://x.com/je_grami"
                            lassName="relative inline-block after:absolute after:left-0 after:-bottom-0.5 after:h-[1px] after:w-0 after:bg-green-500 after:transition-all after:duration-300 hover:after:w-full hover:text-gray-300"
                            >
                                X
                            </a>
                        </p>

                        <p>
                            <a href="https://github.com/jegrami"
                            className="relative inline-block after:absolute after:left-0 after:-bottom-0.5 after:h-[1px] after:w-0 after:bg-green-500 after:transition-all after:duration-300 hover:after:w-full hover:text-gray-300"
                            >
                                Github
                            </a>
                        </p>
                
                </div>
            </div>
            
            <div className="h-[1px] mt-40 bg-gradient-to-r from-green-500 via-blue-500 to-pink-500 w-3/4 mx-auto"></div>
              
                <div className="text-center mt-8 font-light text-sm text-normal font-inconsolata">
                    <span className="font-mindshine">&copy;</span> 2025 Nigeria Energy Access Explorer. All Rights Reserved
                </div>
            
            
        </footer>
    )
}

export default Footer;