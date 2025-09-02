import neaxLogo from '../assets/neax-logo.png'
import { Link } from 'react-router-dom'
import { useState } from 'react'
import { Menu, X} from 'lucide-react'

function Header() {
    const [isOpen, setIsOpen] = useState(false)

    return (
        <header className=" bg-green-50 shadow-md fixed top-0 left-0 w-full z-50 ">
            <div className="flex items-center justify-between px-2 py-2 max-w-6xl mx-auto">
                <div className="flex items-center">
                    <img className="w-15 md:w-20" src={neaxLogo} alt="Logo" />
                    <Link to="/" className="text-xl md:text-2xl lg:text-3xl text-green-800 font-mindshine tracking-tighter">
                        Nigeria Energy Access Explorer
                    </Link>
                </div>

                <nav className="hidden sm:flex gap-10 font-roboto font-semibold text-green-800">
                    <Link to="/" className="relative hover:text-green-500 cursor-pointer transition-all ease-in-out before:transition-[width] before:ease-in-out before:duration-600 before:absolute before:bg-green-500 before:origin-center before:h-[2px] before:w-0 hover:before:w-[50%] before:bottom-0 before:left-[50%] after:transition-[width] after:ease-in-out after:duration-700 after:absolute after:bg-green-500 after:origin-center after:h-[2px] after:w-0 hover:after:w-[50%] after:bottom-0 after:right-[50%]">Home</Link>
                    <Link to="/data" className="relative hover:text-green-500 cursor-pointer transition-all ease-in-out before:transition-[width] before:ease-in-out before:duration-600 before:absolute before:bg-green-500 before:origin-center before:h-[2px] before:w-0 hover:before:w-[50%] before:bottom-0 before:left-[50%] after:transition-[width] after:ease-in-out after:duration-700 after:absolute after:bg-green-500 after:origin-center after:h-[2px] after:w-0 hover:after:w-[50%] after:bottom-0 after:right-[50%]">Data</Link>
                    <Link to="/about" className="relative hover:text-green-500 cursor-pointer transition-all ease-in-out before:transition-[width] before:ease-in-out before:duration-600 before:absolute before:bg-green-500 before:origin-center before:h-[2px] before:w-0 hover:before:w-[50%] before:bottom-0 before:left-[50%] after:transition-[width] after:ease-in-out after:duration-700 after:absolute after:bg-green-500 after:origin-center after:h-[2px] after:w-0 hover:after:w-[50%] after:bottom-0 after:right-[50%]">About</Link>
                </nav>

                <button
                    className="sm:hidden text-2xl"
                    onClick={() => setIsOpen(!isOpen)}
                    aria-label="Toggle mobile menu"
                >
                    {isOpen ? <X size={28} /> : <Menu size={28} />}
                </button>
            </div>
            {isOpen && (
                <div className="relative">
                    
                    <nav className="sm:hidden px-4 pb-4 absolute top-full right-4 mt-2 bg-white rounded shadow-md z-20 w-40 animate-slide-down">
                        <ul className="flex flex-col px-4 py-2 space-y-2">
                            <li>
                                <Link to="/" className="block hover:underline" onClick={() => setIsOpen(false)}>Home</Link>
                            </li>
                            <li>
                                <Link to ="/data" className="block hover:underline" onClick={() => setIsOpen(false)} >Data</Link>
                            </li>
                            <li>
                                <Link to="/about" className="block hover:underline" onClick={() => setIsOpen(false)}>About</Link>
                            </li>
                        </ul>
                    </nav>
                </div>
            )}
        </header>
    )
}

export default Header;