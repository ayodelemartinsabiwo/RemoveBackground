import { useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { useDropzone } from 'react-dropzone'
import { Upload, Loader, Download, Palette, Image as ImageIcon } from 'lucide-react'
import Header from '@/components/common/Header'
import { imageApi } from '@/services/api'
import { useAuthStore } from '@/store/authStore'
import toast from 'react-hot-toast'

type BackgroundType = 'TRANSPARENT' | 'SOLID' | 'GRADIENT'

export default function EditorPage() {
  const navigate = useNavigate()
  const { isAuthenticated } = useAuthStore()
  const [uploading, setUploading] = useState(false)
  const [processing, setProcessing] = useState(false)
  const [originalImage, setOriginalImage] = useState<string | null>(null)
  const [processedImage, setProcessedImage] = useState<string | null>(null)
  const [imageId, setImageId] = useState<string | null>(null)
  const [backgroundType, setBackgroundType] = useState<BackgroundType>('TRANSPARENT')
  const [solidColor, setSolidColor] = useState('#ffffff')

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (!isAuthenticated) {
      toast.error('Please sign in to upload images')
      navigate('/login')
      return
    }

    const file = acceptedFiles[0]
    if (!file) return

    // Validate file size (10MB max)
    if (file.size > 10 * 1024 * 1024) {
      toast.error('File size must be less than 10MB')
      return
    }

    // Validate file type
    if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) {
      toast.error('Only JPG, PNG, and WEBP formats are supported')
      return
    }

    setUploading(true)
    setOriginalImage(URL.createObjectURL(file))

    try {
      const formData = new FormData()
      formData.append('image', file)

      const response = await imageApi.upload(formData)
      setImageId(response.data.id)
      toast.success('Image uploaded successfully!')

      // Start polling for processing status
      pollProcessingStatus(response.data.id)
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Upload failed')
      setOriginalImage(null)
    } finally {
      setUploading(false)
    }
  }, [isAuthenticated, navigate])

  const pollProcessingStatus = async (id: string) => {
    setProcessing(true)
    const pollInterval = setInterval(async () => {
      try {
        const response = await imageApi.getById(id)
        const image = response.data

        if (image.status === 'COMPLETED') {
          clearInterval(pollInterval)
          setProcessedImage(image.processedSmallUrl || '')
          setProcessing(false)
          toast.success('Background removed successfully!')
        } else if (image.status === 'FAILED') {
          clearInterval(pollInterval)
          setProcessing(false)
          toast.error('Processing failed. Please try again.')
        }
      } catch (error) {
        clearInterval(pollInterval)
        setProcessing(false)
        toast.error('Failed to check processing status')
      }
    }, 2000)
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
      'image/webp': ['.webp'],
    },
    maxFiles: 1,
    disabled: uploading || processing,
  })

  const handleDownload = async () => {
    if (!processedImage || !imageId) return

    try {
      const response = await imageApi.download(imageId, 'SMALL')
      const blob = new Blob([response.data])
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `palmar-bg-removed-${Date.now()}.png`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      toast.success('Image downloaded!')
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Download failed')
    }
  }

  const applyBackground = async () => {
    if (!imageId) return

    try {
      const options = {
        backgroundType,
        ...(backgroundType === 'SOLID' && { solidColor }),
      }

      await imageApi.applyBackground(imageId, options)
      toast.success('Background applied!')

      // Refresh the processed image
      const response = await imageApi.getById(imageId)
      setProcessedImage(response.data.processedSmallUrl || '')
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to apply background')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <div className="container mx-auto px-4 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Remove Background with AI
            </h1>
            <p className="text-xl text-gray-600">
              Upload your image and let our AI do the magic
            </p>
          </div>

          {/* Upload Area */}
          {!originalImage && (
            <div
              {...getRootProps()}
              className={`border-4 border-dashed rounded-2xl p-16 text-center cursor-pointer transition-colors ${
                isDragActive
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-gray-300 bg-white hover:border-primary-400'
              } ${(uploading || processing) && 'opacity-50 cursor-not-allowed'}`}
            >
              <input {...getInputProps()} />
              <Upload className="w-20 h-20 text-gray-400 mx-auto mb-6" />
              <h3 className="text-2xl font-semibold text-gray-900 mb-2">
                {isDragActive ? 'Drop your image here' : 'Upload an Image'}
              </h3>
              <p className="text-gray-600 mb-4">
                Drag and drop or click to browse
              </p>
              <p className="text-sm text-gray-500">
                Supports JPG, PNG, WEBP (Max 10MB)
              </p>
            </div>
          )}

          {/* Image Comparison */}
          {originalImage && (
            <div className="grid md:grid-cols-2 gap-8 mb-8">
              <div className="bg-white rounded-xl p-6 shadow-lg">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                  <ImageIcon className="w-5 h-5" />
                  Original Image
                </h3>
                <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden">
                  <img
                    src={originalImage}
                    alt="Original"
                    className="w-full h-full object-contain"
                  />
                </div>
              </div>

              <div className="bg-white rounded-xl p-6 shadow-lg">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                  <Palette className="w-5 h-5" />
                  Processed Image
                </h3>
                <div
                  className="aspect-square rounded-lg overflow-hidden"
                  style={{
                    backgroundColor: backgroundType === 'SOLID' ? solidColor : '#f3f4f6',
                    backgroundImage:
                      backgroundType === 'TRANSPARENT'
                        ? 'repeating-conic-gradient(#e5e7eb 0% 25%, transparent 0% 50%) 50% / 20px 20px'
                        : 'none',
                  }}
                >
                  {processing ? (
                    <div className="w-full h-full flex items-center justify-center">
                      <div className="text-center">
                        <Loader className="w-12 h-12 text-primary-500 animate-spin mx-auto mb-4" />
                        <p className="text-gray-600">Processing image...</p>
                      </div>
                    </div>
                  ) : processedImage ? (
                    <img
                      src={processedImage}
                      alt="Processed"
                      className="w-full h-full object-contain"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-gray-400">
                      Processing will appear here
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Background Customization */}
          {processedImage && (
            <div className="bg-white rounded-xl p-8 shadow-lg mb-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">
                Customize Background
              </h3>

              <div className="grid md:grid-cols-3 gap-6">
                <button
                  onClick={() => setBackgroundType('TRANSPARENT')}
                  className={`p-6 rounded-lg border-2 transition-colors ${
                    backgroundType === 'TRANSPARENT'
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <div className="text-center">
                    <div className="w-16 h-16 mx-auto mb-3 rounded-lg bg-white border-2 border-gray-200" />
                    <div className="font-semibold text-gray-900">Transparent</div>
                  </div>
                </button>

                <button
                  onClick={() => setBackgroundType('SOLID')}
                  className={`p-6 rounded-lg border-2 transition-colors ${
                    backgroundType === 'SOLID'
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <div className="text-center">
                    <div
                      className="w-16 h-16 mx-auto mb-3 rounded-lg border-2 border-gray-200"
                      style={{ backgroundColor: solidColor }}
                    />
                    <div className="font-semibold text-gray-900">Solid Color</div>
                  </div>
                </button>

                <button
                  onClick={() => setBackgroundType('GRADIENT')}
                  className={`p-6 rounded-lg border-2 transition-colors ${
                    backgroundType === 'GRADIENT'
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <div className="text-center">
                    <div className="w-16 h-16 mx-auto mb-3 rounded-lg bg-gradient-to-br from-primary-500 to-orange-500 border-2 border-gray-200" />
                    <div className="font-semibold text-gray-900">Gradient</div>
                  </div>
                </button>
              </div>

              {backgroundType === 'SOLID' && (
                <div className="mt-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Choose Color
                  </label>
                  <div className="flex gap-4 items-center">
                    <input
                      type="color"
                      value={solidColor}
                      onChange={(e) => setSolidColor(e.target.value)}
                      className="w-20 h-12 rounded-lg cursor-pointer"
                    />
                    <input
                      type="text"
                      value={solidColor}
                      onChange={(e) => setSolidColor(e.target.value)}
                      className="flex-1 px-4 py-2 border border-gray-300 rounded-lg"
                      placeholder="#ffffff"
                    />
                  </div>
                </div>
              )}

              <button
                onClick={applyBackground}
                className="mt-6 px-6 py-3 bg-primary-500 text-white font-semibold rounded-lg hover:bg-primary-600 transition-colors"
              >
                Apply Background
              </button>
            </div>
          )}

          {/* Actions */}
          {processedImage && (
            <div className="flex gap-4 justify-center">
              <button
                onClick={handleDownload}
                className="flex items-center gap-2 px-8 py-4 bg-primary-500 text-white font-semibold rounded-lg hover:bg-primary-600 transition-colors shadow-lg text-lg"
              >
                <Download className="w-6 h-6" />
                Download Image
              </button>

              <button
                onClick={() => {
                  setOriginalImage(null)
                  setProcessedImage(null)
                  setImageId(null)
                }}
                className="px-8 py-4 bg-white text-gray-700 font-semibold rounded-lg border-2 border-gray-300 hover:bg-gray-50 transition-colors text-lg"
              >
                Upload Another
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
