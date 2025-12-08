import { Link } from 'react-router-dom'
import { useState } from 'react'
import { Menu, X } from 'lucide-react'
import { useAuthStore } from '@/store/authStore'

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const { isAuthenticated, logout } = useAuthStore()

  const handleLogout = () => {
    logout()
    setMobileMenuOpen(false)
  }

  return (
    <nav className="sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <img src="/images/icon.ico" alt="Logo" className="h-9 w-auto" />
            <span className="font-bold text-xl text-gray-900">
              Background Remover
            </span>
          </Link>

          {/* Desktop Navigation */}
          <ul className="hidden md:flex items-center gap-8">
            <li>
              <a href="#features" className="text-gray-700 hover:text-primary-500 font-medium transition-colors">
                Features
              </a>
            </li>
            <li>
              <a href="#why-choose-us" className="text-gray-700 hover:text-primary-500 font-medium transition-colors">
                Why Choose Us
              </a>
            </li>
            <li>
              <a href="#how-it-works" className="text-gray-700 hover:text-primary-500 font-medium transition-colors">
                How It Works
              </a>
            </li>
            <li>
              <span className="text-gray-400 font-medium cursor-not-allowed">
                APIs/Plugin <span className="text-xs bg-primary-100 text-primary-600 px-2 py-0.5 rounded ml-1">Coming Soon</span>
              </span>
            </li>
          </ul>

          {/* Auth Buttons */}
          <div className="hidden md:flex items-center gap-4">
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="text-gray-700 hover:text-primary-500 font-medium">
                  Dashboard
                </Link>
                <Link to="/editor" className="btn-primary">
                  Upload Image
                </Link>
                <button onClick={handleLogout} className="text-gray-600 hover:text-gray-900">
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="text-gray-700 hover:text-primary-500 font-medium">
                  Login
                </Link>
                <Link to="/register" className="btn-primary">
                  Get Started Free
                </Link>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 text-gray-700 hover:text-primary-500"
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-200">
            <ul className="flex flex-col gap-4">
              <li>
                <a
                  href="#features"
                  className="block text-gray-700 hover:text-primary-500 font-medium"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Features
                </a>
              </li>
              <li>
                <a
                  href="#why-choose-us"
                  className="block text-gray-700 hover:text-primary-500 font-medium"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Why Choose Us
                </a>
              </li>
              <li>
                <a
                  href="#how-it-works"
                  className="block text-gray-700 hover:text-primary-500 font-medium"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  How It Works
                </a>
              </li>
              <li>
                <span className="block text-gray-400 font-medium">
                  APIs/Plugin <span className="text-xs bg-primary-100 text-primary-600 px-2 py-0.5 rounded ml-1">Coming Soon</span>
                </span>
              </li>
              <li className="pt-4 border-t border-gray-200">
                {isAuthenticated ? (
                  <>
                    <Link
                      to="/dashboard"
                      className="block mb-3 text-gray-700 hover:text-primary-500 font-medium"
                      onClick={() => setMobileMenuOpen(false)}
                    >
                      Dashboard
                    </Link>
                    <Link
                      to="/editor"
                      className="block mb-3 btn-primary w-full text-center"
                      onClick={() => setMobileMenuOpen(false)}
                    >
                      Upload Image
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="block w-full text-left text-gray-600 hover:text-gray-900"
                    >
                      Logout
                    </button>
                  </>
                ) : (
                  <>
                    <Link
                      to="/login"
                      className="block mb-3 text-gray-700 hover:text-primary-500 font-medium"
                      onClick={() => setMobileMenuOpen(false)}
                    >
                      Login
                    </Link>
                    <Link
                      to="/register"
                      className="block btn-primary w-full text-center"
                      onClick={() => setMobileMenuOpen(false)}
                    >
                      Get Started Free
                    </Link>
                  </>
                )}
              </li>
            </ul>
          </div>
        )}
      </div>
    </nav>
  )
}
