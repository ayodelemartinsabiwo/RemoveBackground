import { Link } from 'react-router-dom'
import { Check, Upload, Sparkles, Zap, Shield, Download, Image as ImageIcon, Palette, Cloud } from 'lucide-react'
import Header from '@/components/common/Header'
import Footer from '@/components/common/Footer'
import HeroShowcase from '@/components/home/HeroShowcase'
import ProTips from '@/components/home/ProTips'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-white">
      <Header />

      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-primary-50 via-orange-50 to-white pt-8 md:pt-12 pb-16 md:pb-20 overflow-hidden">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-6 leading-tight">
              Remove Backgrounds with
              <span className="text-primary-500 block mt-2">AI Precision</span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-10 max-w-3xl mx-auto">
              Professional-grade background removal powered by advanced AI.
              Perfect edges, preserved hair strands, and instant results.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
              <Link
                to="/editor"
                className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-primary-500 text-white font-semibold rounded-lg hover:bg-primary-600 transition-colors shadow-lg hover:shadow-xl text-lg"
              >
                <Upload className="w-5 h-5" />
                Try It Free - 3 Credits
              </Link>
              <Link
                to="/pricing"
                className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-white text-primary-500 font-semibold rounded-lg border-2 border-primary-500 hover:bg-primary-50 transition-colors text-lg"
              >
                View Pricing Plans
              </Link>
            </div>

            {/* User Categories */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-12 mb-20 max-w-4xl mx-auto">
              <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                <div className="text-3xl mb-2">🎨</div>
                <h4 className="font-semibold text-gray-900">Creative Professionals</h4>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                <div className="text-3xl mb-2">🛍️</div>
                <h4 className="font-semibold text-gray-900">E-commerce & Business</h4>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                <div className="text-3xl mb-2">📸</div>
                <h4 className="font-semibold text-gray-900">Content Creators</h4>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                <div className="text-3xl mb-2">👤</div>
                <h4 className="font-semibold text-gray-900">Personal Users</h4>
              </div>
            </div>
          </div>

          {/* Hero Showcase with 3 Floating Demo Cards */}
          <HeroShowcase />
        </div>
      </section>

      {/* Why Choose Us */}
      <section id="why-choose-us" className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Why Choose Palmar Professional?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Built with advanced AI and designed for professionals who demand perfection
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <div className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow">
              <div className="w-16 h-16 bg-primary-100 rounded-lg flex items-center justify-center mb-6">
                <Sparkles className="w-8 h-8 text-primary-500" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Intelligent Optimization</h3>
              <p className="text-gray-600 leading-relaxed">
                BiRefNet-portrait and U2Net models work together to detect hair strands,
                soft edges, and complex boundaries with precision AI can't match.
              </p>
            </div>

            <div className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow">
              <div className="w-16 h-16 bg-primary-100 rounded-lg flex items-center justify-center mb-6">
                <Zap className="w-8 h-8 text-primary-500" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Automatic Enhancement</h3>
              <p className="text-gray-600 leading-relaxed">
                Hair smoothing, artifact cleanup, and edge refinement happen automatically.
                Your images look professional without manual touch-ups.
              </p>
            </div>

            <div className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow">
              <div className="w-16 h-16 bg-primary-100 rounded-lg flex items-center justify-center mb-6">
                <Shield className="w-8 h-8 text-primary-500" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Quality-First Approach</h3>
              <p className="text-gray-600 leading-relaxed">
                Multi-resolution processing ensures crisp results at any size.
                From thumbnails to ultra-HD prints, quality never compromises.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Powerful Features for Every Need
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Everything you need to create stunning images with transparent backgrounds
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                  <Sparkles className="w-6 h-6 text-primary-500" />
                </div>
              </div>
              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">AI-Powered Precision</h3>
                <p className="text-gray-600">
                  BiRefNet model ensures perfect edge detection and hair strand preservation
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                  <Zap className="w-6 h-6 text-primary-500" />
                </div>
              </div>
              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Lightning Fast</h3>
                <p className="text-gray-600">
                  Process images in seconds with our optimized cloud infrastructure
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                  <ImageIcon className="w-6 h-6 text-primary-500" />
                </div>
              </div>
              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Multi-Resolution Output</h3>
                <p className="text-gray-600">
                  Get Small (512px), HD (1920px), or Ultra-HD (3840px) versions based on your plan
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                  <Palette className="w-6 h-6 text-primary-500" />
                </div>
              </div>
              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Custom Backgrounds</h3>
                <p className="text-gray-600">
                  Add solid colors, gradients, or upload your own texture backgrounds
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                  <Cloud className="w-6 h-6 text-primary-500" />
                </div>
              </div>
              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Cloud Storage</h3>
                <p className="text-gray-600">
                  Access your processed images anytime, anywhere from any device
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                  <Shield className="w-6 h-6 text-primary-500" />
                </div>
              </div>
              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Secure & Private</h3>
                <p className="text-gray-600">
                  Your images are encrypted and stored securely with enterprise-grade protection
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Pro Tips Section with Flip Cards */}
      <ProTips />

      {/* How It Works */}
      <section id="how-it-works" className="py-20 bg-gradient-to-br from-primary-50 to-orange-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Three simple steps to perfect background removal
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-12 max-w-6xl mx-auto">
            <div className="text-center">
              <div className="w-20 h-20 bg-primary-500 rounded-full flex items-center justify-center text-white text-3xl font-bold mx-auto mb-6 shadow-lg">
                1
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Upload Your Image</h3>
              <p className="text-gray-600 leading-relaxed">
                Drag and drop or click to upload your image. We support JPG, PNG, and WEBP formats up to 10MB.
              </p>
            </div>

            <div className="text-center">
              <div className="w-20 h-20 bg-primary-500 rounded-full flex items-center justify-center text-white text-3xl font-bold mx-auto mb-6 shadow-lg">
                2
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">AI Processes</h3>
              <p className="text-gray-600 leading-relaxed">
                Our advanced AI removes the background with precision, preserving every detail and edge.
              </p>
            </div>

            <div className="text-center">
              <div className="w-20 h-20 bg-primary-500 rounded-full flex items-center justify-center text-white text-3xl font-bold mx-auto mb-6 shadow-lg">
                3
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Download & Use</h3>
              <p className="text-gray-600 leading-relaxed">
                Download your processed image in the resolution tier included with your plan. Add custom backgrounds if needed.
              </p>
            </div>
          </div>

          <div className="text-center mt-12">
            <Link
              to="/editor"
              className="inline-flex items-center gap-2 px-8 py-4 bg-primary-500 text-white font-semibold rounded-lg hover:bg-primary-600 transition-colors shadow-lg hover:shadow-xl text-lg"
            >
              <Upload className="w-5 h-5" />
              Start Removing Backgrounds Now
            </Link>
          </div>
        </div>
      </section>

      {/* Desktop Version Section */}
      <section id="desktop" className="py-20 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary-500/10 to-orange-500/10"></div>
        <div className="container mx-auto px-4 relative z-10">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Prefer Offline? Get the Desktop Version
            </h2>
            <p className="text-xl text-gray-300 max-w-2xl mx-auto">
              One-time purchase. Unlimited processing. No internet required.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-12 max-w-5xl mx-auto items-center">
            {/* Features List */}
            <div>
              <h3 className="text-2xl font-bold mb-6">Desktop Lifetime License</h3>
              <ul className="space-y-4">
                <li className="flex items-start gap-3">
                  <Check className="w-6 h-6 text-green-400 flex-shrink-0 mt-0.5" />
                  <div>
                    <div className="font-semibold">Unlimited Offline Processing</div>
                    <div className="text-gray-400 text-sm">Process as many images as you want without internet</div>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <Check className="w-6 h-6 text-green-400 flex-shrink-0 mt-0.5" />
                  <div>
                    <div className="font-semibold">No Subscription Needed</div>
                    <div className="text-gray-400 text-sm">Pay once, use forever. No monthly fees or credit limits</div>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <Check className="w-6 h-6 text-green-400 flex-shrink-0 mt-0.5" />
                  <div>
                    <div className="font-semibold">Windows Context Menu Integration</div>
                    <div className="text-gray-400 text-sm">Right-click any image to remove background instantly</div>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <Check className="w-6 h-6 text-green-400 flex-shrink-0 mt-0.5" />
                  <div>
                    <div className="font-semibold">Your Data Stays Local</div>
                    <div className="text-gray-400 text-sm">Complete privacy - nothing uploaded to the cloud</div>
                  </div>
                </li>
              </ul>

              <div className="mt-8 p-4 bg-gray-800 rounded-lg border border-gray-700">
                <p className="text-sm text-gray-300">
                  <strong className="text-white">Perfect for:</strong> High-volume users, photographers,
                  agencies, and anyone who needs unlimited processing without recurring costs or internet dependency.
                </p>
              </div>
            </div>

            {/* Pricing Card */}
            <div>
              <div className="bg-gradient-to-br from-primary-500 to-orange-500 rounded-2xl p-8 shadow-2xl">
                <div className="text-center">
                  <div className="text-sm font-semibold text-white/90 mb-2">ONE-TIME PAYMENT</div>
                  <div className="text-6xl font-bold text-white mb-2">$320.95</div>
                  <div className="text-white/90 mb-6">Lifetime License</div>

                  <a
                    href="https://github.com/ayodelemartinsabiwo/RemoveBackground/releases/download/v1.0.0/BackgroundRemover_Setup.exe"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center justify-center gap-3 w-full px-8 py-4 bg-white text-primary-600 font-bold rounded-lg hover:bg-gray-100 transition-colors shadow-lg hover:shadow-xl text-lg mb-6"
                  >
                    <Download className="w-6 h-6" />
                    Download for Windows
                  </a>

                  <div className="space-y-2 text-sm text-white/90">
                    <div className="flex items-center justify-center gap-2">
                      <Check className="w-5 h-5" />
                      <span>Instant download</span>
                    </div>
                    <div className="flex items-center justify-center gap-2">
                      <Check className="w-5 h-5" />
                      <span>Free updates forever</span>
                    </div>
                    <div className="flex items-center justify-center gap-2">
                      <Check className="w-5 h-5" />
                      <span>30-day money-back guarantee</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-6 text-center">
                <p className="text-gray-400 text-sm">
                  Prefer flexibility? <Link to="/pricing" className="text-primary-400 hover:text-primary-300 underline">Check out our web plans</Link> with cloud storage and multi-device access.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
            Ready to Remove Backgrounds Like a Pro?
          </h2>
          <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
            Join thousands of professionals who trust Palmar Professional for their background removal needs.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/editor"
              className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-primary-500 text-white font-semibold rounded-lg hover:bg-primary-600 transition-colors shadow-lg hover:shadow-xl text-lg"
            >
              <Upload className="w-5 h-5" />
              Start Free Trial
            </Link>
            <Link
              to="/pricing"
              className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-white text-primary-500 font-semibold rounded-lg border-2 border-primary-500 hover:bg-primary-50 transition-colors text-lg"
            >
              Compare All Plans
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  )
}
