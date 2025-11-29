import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { CreditCard, Image as ImageIcon, Download, Trash2, Calendar } from 'lucide-react'
import Header from '@/components/common/Header'
import { userApi, imageApi } from '@/services/api'
import { useAuthStore } from '@/store/authStore'
import { Image } from '@/types'
import toast from 'react-hot-toast'

export default function DashboardPage() {
  const { user } = useAuthStore()
  const [images, setImages] = useState<Image[]>([])
  const [credits, setCredits] = useState(0)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [creditsResponse, imagesResponse] = await Promise.all([
        userApi.getCredits(),
        imageApi.getAll({ limit: 20 }),
      ])

      setCredits(creditsResponse.data.availableCredits)
      setImages(imagesResponse.data.images)
    } catch (error: any) {
      toast.error('Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (imageId: string) => {
    if (!confirm('Are you sure you want to delete this image?')) return

    try {
      await imageApi.delete(imageId)
      setImages(images.filter((img) => img.id !== imageId))
      toast.success('Image deleted')
    } catch (error: any) {
      toast.error('Failed to delete image')
    }
  }

  const handleDownload = async (imageId: string, tier: 'SMALL' | 'HD' | 'ULTRA_HD') => {
    try {
      const response = await imageApi.download(imageId, tier)
      const blob = new Blob([response.data])
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `palmar-${imageId}-${tier}.png`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      toast.success('Download started')
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Download failed')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="container mx-auto px-4 py-12 text-center">
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <div className="container mx-auto px-4 py-12">
        <div className="max-w-7xl mx-auto">
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              Welcome back, {user?.firstName || user?.email}!
            </h1>
            <p className="text-gray-600">Manage your images and credits</p>
          </div>

          {/* Stats Grid */}
          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <div className="bg-white rounded-xl p-6 shadow-lg">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                  <CreditCard className="w-6 h-6 text-primary-500" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Available Credits</p>
                  <p className="text-3xl font-bold text-gray-900">{credits}</p>
                </div>
              </div>
              <Link
                to="/pricing"
                className="mt-4 block text-center px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
              >
                Buy More Credits
              </Link>
            </div>

            <div className="bg-white rounded-xl p-6 shadow-lg">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <ImageIcon className="w-6 h-6 text-blue-500" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Total Images</p>
                  <p className="text-3xl font-bold text-gray-900">{images.length}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl p-6 shadow-lg">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                  <Download className="w-6 h-6 text-green-500" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Current Plan</p>
                  <p className="text-xl font-bold text-gray-900">{user?.subscription?.planType || 'FREE'}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Images Grid */}
          <div className="bg-white rounded-xl p-8 shadow-lg">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Your Images</h2>
              <Link
                to="/editor"
                className="px-6 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
              >
                Upload New
              </Link>
            </div>

            {images.length === 0 ? (
              <div className="text-center py-12">
                <ImageIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-600 mb-4">No images yet</p>
                <Link
                  to="/editor"
                  className="inline-block px-6 py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
                >
                  Upload Your First Image
                </Link>
              </div>
            ) : (
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {images.map((image) => (
                  <div key={image.id} className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
                    <div
                      className="aspect-square bg-gray-100 overflow-hidden"
                      style={{
                        backgroundImage:
                          'repeating-conic-gradient(#e5e7eb 0% 25%, transparent 0% 50%) 50% / 20px 20px',
                      }}
                    >
                      {image.processedSmallUrl ? (
                        <img
                          src={image.processedSmallUrl}
                          alt="Processed"
                          className="w-full h-full object-contain"
                        />
                      ) : (
                        <img
                          src={image.originalUrl}
                          alt="Original"
                          className="w-full h-full object-cover"
                        />
                      )}
                    </div>

                    <div className="p-4">
                      <div className="flex items-center gap-2 text-sm text-gray-600 mb-3">
                        <Calendar className="w-4 h-4" />
                        {new Date(image.createdAt).toLocaleDateString()}
                      </div>

                      <div className="flex items-center justify-between gap-2">
                        <span
                          className={`px-2 py-1 text-xs rounded-full ${
                            image.status === 'COMPLETED'
                              ? 'bg-green-100 text-green-800'
                              : image.status === 'PROCESSING'
                              ? 'bg-blue-100 text-blue-800'
                              : image.status === 'FAILED'
                              ? 'bg-red-100 text-red-800'
                              : 'bg-gray-100 text-gray-800'
                          }`}
                        >
                          {image.status}
                        </span>

                        <div className="flex gap-2">
                          {image.status === 'COMPLETED' && (
                            <button
                              onClick={() => handleDownload(image.id, 'SMALL')}
                              className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                              title="Download"
                            >
                              <Download className="w-4 h-4" />
                            </button>
                          )}
                          <button
                            onClick={() => handleDelete(image.id)}
                            className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                            title="Delete"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
