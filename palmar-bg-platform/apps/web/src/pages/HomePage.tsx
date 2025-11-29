import { Link } from 'react-router-dom'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <nav className="flex items-center justify-between">
          <div className="text-2xl font-bold text-primary-500">
            Palmar Professional
          </div>
          <div className="flex gap-4">
            <Link to="/login" className="btn-outline">
              Login
            </Link>
            <Link to="/register" className="btn-primary">
              Get Started
            </Link>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <main className="container mx-auto px-4 py-20">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Remove Backgrounds with
            <span className="text-primary-500"> AI Precision</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Professional-grade background removal powered by advanced AI.
            Perfect edges, preserved hair strands, and instant results.
          </p>

          <div className="flex gap-4 justify-center">
            <Link to="/editor" className="btn-primary text-lg px-8 py-3">
              Try It Free
            </Link>
            <Link to="/pricing" className="btn-outline text-lg px-8 py-3">
              View Pricing
            </Link>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-3 gap-8 mt-20">
            <div className="card">
              <div className="text-4xl mb-4">✨</div>
              <h3 className="text-xl font-semibold mb-2">AI-Powered</h3>
              <p className="text-gray-600">
                Advanced BiRefNet model for perfect edge detection
              </p>
            </div>

            <div className="card">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="text-xl font-semibold mb-2">Lightning Fast</h3>
              <p className="text-gray-600">
                Process images in seconds, not minutes
              </p>
            </div>

            <div className="card">
              <div className="text-4xl mb-4">🎨</div>
              <h3 className="text-xl font-semibold mb-2">Custom Backgrounds</h3>
              <p className="text-gray-600">
                Add solid colors, gradients, or textures
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
