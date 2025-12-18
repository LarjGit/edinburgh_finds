import Image from 'next/image'
import Link from 'next/link'  // ADD THIS IMPORT

export default function Navigation() {
  return (
    <nav className="bg-slate-900 text-white shadow-sm sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center">
            <Image 
              src="/images/branding/logo-horizontal.png" 
              alt="Edinburgh Finds" 
              width={200}
              height={60}
              priority
            />
          </Link>
          
          {/* Desktop Navigation */}
          <div className="hidden md:flex gap-8">
            <Link 
              href="/" 
              className="text-white hover:text-teal-400 transition-colors font-medium"
            >
              Home
            </Link>
            <Link 
              href="/about" 
              className="text-white hover:text-teal-400 transition-colors font-medium"
            >
              About
            </Link>
            <Link 
              href="/contact" 
              className="text-white hover:text-teal-400 transition-colors font-medium"
            >
              Contact
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button 
            className="md:hidden p-2"
            aria-label="Menu"
          >
            <svg 
              className="w-6 h-6 text-white" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M4 6h16M4 12h16M4 18h16" 
              />
            </svg>
          </button>
        </div>
      </div>
    </nav>
  )
}