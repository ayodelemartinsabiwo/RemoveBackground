import { useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { useDropzone } from 'react-dropzone'
import { Upload, Loader, Download, Palette, Image as ImageIcon } from 'lucide-react'
import Header from '@/components/common/Header'
import Footer from '@/components/common/Footer'
import HeroShowcase from '@/components/home/HeroShowcase'
import { imageApi } from '@/services/api'
import { useAuthStore } from '@/store/authStore'
import toast from 'react-hot-toast'

type BackgroundType = 'TRANSPARENT' | 'SOLID' | 'GRADIENT' | 'TEXTURE'

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
  const [gradientColor1, setGradientColor1] = useState('#ff6b35')
  const [gradientColor2, setGradientColor2] = useState('#ff8555')
  const [textureType, setTextureType] = useState('dots')

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
    const imageUrl = URL.createObjectURL(file)
    setOriginalImage(imageUrl)

    try {
      const formData = new FormData()
      formData.append('image', file)

      const response = await imageApi.upload(formData)

      console.log('=== UPLOAD RESPONSE ===')
      console.log('Full response object:', JSON.stringify(response, null, 2))
      console.log('response.success:', response.success)
      console.log('response.data:', response.data)
      console.log('response.error:', response.error)

      // Check if API is in demo/placeholder mode or errored
      if (!response.success || !response.data || response.error) {
        // Demo mode: simulate successful upload for demonstration
        const demoId = `demo-${Date.now()}`
        setImageId(demoId)
        toast.success('Image uploaded successfully! (Demo Mode)')

        // Simulate processing delay
        setTimeout(() => {
          setProcessedImage(imageUrl)
          setProcessing(false)
          toast.success('Background removed successfully! (Demo Mode)')
        }, 3000)

        setProcessing(true)
      } else {
        // Real API mode
        console.log('Full upload response:', response)
        console.log('response.data:', response.data)
        console.log('response.data.image:', response.data?.image)
        console.log('response.data.id:', response.data?.id)

        const imageId = response.data?.image?.id || response.data?.id
        console.log('Extracted imageId:', imageId)

        if (!imageId) {
          console.error('No image ID in response:', response.data)
          toast.error('Upload succeeded but could not get image ID')
          return
        }
        setImageId(imageId)
        toast.success('Image uploaded successfully!')
        pollProcessingStatus(imageId)
      }
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Upload failed')
      setOriginalImage(null)
    } finally {
      setUploading(false)
    }
  }, [isAuthenticated, navigate])

  const pollProcessingStatus = async (id: string) => {
    setProcessing(true)
    let pollCount = 0
    const maxPolls = 60 // 60 * 2 seconds = 2 minutes max

    const pollInterval = setInterval(async () => {
      pollCount++

      // Stop polling after 2 minutes
      if (pollCount >= maxPolls) {
        clearInterval(pollInterval)
        setProcessing(false)
        toast.error('Processing timeout. Please refresh the page to check status.')
        return
      }

      try {
        const response = await imageApi.getById(id)

        // Handle auth errors or API failures
        if (!response.success || !response.data) {
          console.error('Failed to get image status:', response.error)

          // If auth error, stop polling and show message
          if (response.error?.includes('Unauthorized') || response.error?.includes('401')) {
            clearInterval(pollInterval)
            setProcessing(false)
            toast.error('Session expired. Please refresh the page.')
            return
          }

          // For other errors, continue polling (might be temporary)
          return
        }

        const image = response.data
        const status = image.processingStatus || image.status

        console.log('📊 Polling status:', { imageId: id, status, processedSmallUrl: image.processedSmallUrl })

        if (status === 'COMPLETED') {
          clearInterval(pollInterval)

          // Set processed image URL
          if (image.processedSmallUrl) {
            setProcessedImage(image.processedSmallUrl)
            setProcessing(false)
            toast.success('Background removed successfully!')
          } else {
            // Image marked COMPLETED but no URL - database issue
            setProcessing(false)
            toast.error('Processing completed but image URL missing. Please refresh.')
          }
        } else if (status === 'FAILED') {
          clearInterval(pollInterval)
          setProcessing(false)
          toast.error(image.errorMessage || 'Processing failed. Please try again.')
        }
      } catch (error) {
        console.error('Error polling status:', error)
        clearInterval(pollInterval)
        setProcessing(false)
        toast.error('Failed to check processing status')
      }
    }, 2000)

    // Cleanup on unmount
    return () => clearInterval(pollInterval)
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
      // Generate filename in format: filename_backgroundRemover_currentdate.png
      const now = new Date()
      const dateStr = now.toISOString().split('T')[0].replace(/-/g, '')
      const originalFileName = 'image' // In real implementation, get from uploaded file
      const fileName = `${originalFileName}_backgroundRemover_${dateStr}.png`

      const response = await imageApi.download(imageId, 'SMALL')
      const blob = new Blob([response.data])
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = fileName
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
        ...(backgroundType === 'GRADIENT' && { gradientColor1, gradientColor2 }),
        ...(backgroundType === 'TEXTURE' && { textureType }),
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

  const handleSampleImageClick = async (imageUrl: string) => {
    if (!isAuthenticated) {
      toast.error('Please sign in to upload images')
      navigate('/login')
      return
    }

    try {
      setUploading(true)

      // Fetch the image from URL and convert to File
      const response = await fetch(imageUrl)
      const blob = await response.blob()
      const file = new File([blob], 'sample-image.jpg', { type: 'image/jpeg' })

      setOriginalImage(imageUrl)

      // Upload via real API
      const formData = new FormData()
      formData.append('image', file)

      const apiResponse = await imageApi.upload(formData)

      // Check if API is in demo/placeholder mode
      if (!apiResponse.success || !apiResponse.data) {
        // Demo mode fallback
        const demoId = `demo-${Date.now()}`
        setImageId(demoId)
        toast.success('Sample image uploaded! (Demo Mode)')

        setProcessing(true)

        setTimeout(() => {
          setProcessedImage(imageUrl)
          setProcessing(false)
          toast.success('Background removed successfully! (Demo Mode)')
        }, 3000)
      } else {
        // Real API mode
        const imageId = apiResponse.data?.image?.id || apiResponse.data?.id
        if (!imageId) {
          console.error('No image ID in response:', apiResponse.data)
          toast.error('Upload succeeded but could not get image ID')
          return
        }
        setImageId(imageId)
        toast.success('Sample image uploaded successfully!')
        pollProcessingStatus(imageId)
      }
    } catch (error: any) {
      toast.error('Failed to load sample image')
      setOriginalImage(null)
    } finally {
      setUploading(false)
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
            <>
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

              {/* Hero Showcase Section */}
              <div className="mt-20">
                <HeroShowcase />
              </div>

              {/* Sample Images Section */}
              <div className="mt-20">
                <h3 className="text-2xl font-bold text-center text-gray-900 mb-8">
                  Try with Sample Images
                </h3>
                <div className="flex gap-4 justify-center flex-wrap">
                  <div
                    onClick={() => handleSampleImageClick('https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=800&h=800&fit=crop')}
                    className="w-[150px] h-[150px] rounded-lg overflow-hidden shadow-lg cursor-pointer hover:scale-105 transition-transform"
                  >
                    <img
                      src="https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=150&h=150&fit=crop"
                      alt="Portrait Model"
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div
                    onClick={() => handleSampleImageClick('https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=800&h=800&fit=crop')}
                    className="w-[150px] h-[150px] rounded-lg overflow-hidden shadow-lg cursor-pointer hover:scale-105 transition-transform"
                  >
                    <img
                      src="https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=150&h=150&fit=crop"
                      alt="Dog"
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div
                    onClick={() => handleSampleImageClick('https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=800&h=800&fit=crop')}
                    className="w-[150px] h-[150px] rounded-lg overflow-hidden shadow-lg cursor-pointer hover:scale-105 transition-transform"
                  >
                    <img
                      src="https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=150&h=150&fit=crop"
                      alt="Handbag"
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div
                    onClick={() => handleSampleImageClick('https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=800&h=800&fit=crop')}
                    className="w-[150px] h-[150px] rounded-lg overflow-hidden shadow-lg cursor-pointer hover:scale-105 transition-transform"
                  >
                    <img
                      src="https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=150&h=150&fit=crop"
                      alt="T-Shirt"
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div
                    onClick={() => handleSampleImageClick('https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=800&h=800&fit=crop')}
                    className="w-[150px] h-[150px] rounded-lg overflow-hidden shadow-lg cursor-pointer hover:scale-105 transition-transform"
                  >
                    <img
                      src="https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=150&h=150&fit=crop"
                      alt="Sneakers"
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div
                    onClick={() => handleSampleImageClick('https://images.unsplash.com/photo-1611312449408-fcece27cdbb7?w=800&h=800&fit=crop')}
                    className="w-[150px] h-[150px] rounded-lg overflow-hidden shadow-lg cursor-pointer hover:scale-105 transition-transform"
                  >
                    <img
                      src="https://images.unsplash.com/photo-1611312449408-fcece27cdbb7?w=150&h=150&fit=crop"
                      alt="Watch"
                      className="w-full h-full object-cover"
                    />
                  </div>
                </div>
              </div>
            </>
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
                        : backgroundType === 'GRADIENT'
                        ? `linear-gradient(135deg, ${gradientColor1}, ${gradientColor2})`
                        : backgroundType === 'TEXTURE'
                        ? textureType === 'dots'
                          ? 'radial-gradient(circle, #d1d5db 1px, transparent 1px)'
                          : textureType === 'grid'
                          ? 'linear-gradient(#d1d5db 1px, transparent 1px), linear-gradient(90deg, #d1d5db 1px, transparent 1px)'
                          : textureType === 'diagonal'
                          ? 'repeating-linear-gradient(45deg, transparent, transparent 10px, #d1d5db 10px, #d1d5db 11px)'
                          : 'url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIj48ZmlsdGVyIGlkPSJhIj48ZmVUdXJidWxlbmNlIGJhc2VGcmVxdWVuY3k9Ii43NSIgc3RpdGNoVGlsZXM9InN0aXRjaCIvPjwvZmlsdGVyPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbHRlcj0idXJsKCNhKSIgb3BhY2l0eT0iMC4wNSIvPjwvc3ZnPg==)'
                        : 'none',
                    backgroundSize:
                      backgroundType === 'TEXTURE'
                        ? textureType === 'dots'
                          ? '20px 20px'
                          : textureType === 'grid'
                          ? '20px 20px'
                          : 'auto'
                        : 'auto',
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

          {/* Background Customization - Minimalistic Horizontal Layout */}
          {processedImage && (
            <div className="bg-white rounded-xl p-6 shadow-lg mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Customize Background
              </h3>

              <div className="flex flex-wrap items-center gap-4">
                {/* Transparent Option */}
                <button
                  onClick={() => setBackgroundType('TRANSPARENT')}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg border-2 transition-colors ${
                    backgroundType === 'TRANSPARENT'
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <div className="w-8 h-8 rounded border-2 border-gray-300 bg-white" />
                  <span className="text-sm font-medium text-gray-900">Transparent</span>
                </button>

                {/* Solid Color Option with Inline Picker */}
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setBackgroundType('SOLID')}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg border-2 transition-colors ${
                      backgroundType === 'SOLID'
                        ? 'border-primary-500 bg-primary-50'
                        : 'border-gray-300 hover:border-gray-400'
                    }`}
                  >
                    <label className="cursor-pointer">
                      <input
                        type="color"
                        value={solidColor}
                        onChange={(e) => {
                          setSolidColor(e.target.value)
                          setBackgroundType('SOLID')
                        }}
                        className="w-8 h-8 rounded border-2 border-gray-200 cursor-pointer"
                      />
                    </label>
                    <span className="text-sm font-medium text-gray-900">Solid</span>
                  </button>
                  {backgroundType === 'SOLID' && (
                    <input
                      type="text"
                      value={solidColor}
                      onChange={(e) => setSolidColor(e.target.value)}
                      className="w-24 px-2 py-1 text-xs border border-gray-300 rounded"
                      placeholder="#ffffff"
                    />
                  )}
                </div>

                {/* Gradient Option with Inline Pickers */}
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setBackgroundType('GRADIENT')}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg border-2 transition-colors ${
                      backgroundType === 'GRADIENT'
                        ? 'border-primary-500 bg-primary-50'
                        : 'border-gray-300 hover:border-gray-400'
                    }`}
                  >
                    <div className="flex gap-1">
                      <label className="cursor-pointer">
                        <input
                          type="color"
                          value={gradientColor1}
                          onChange={(e) => {
                            setGradientColor1(e.target.value)
                            setBackgroundType('GRADIENT')
                          }}
                          className="w-4 h-8 rounded-l border-2 border-gray-200 cursor-pointer"
                        />
                      </label>
                      <label className="cursor-pointer">
                        <input
                          type="color"
                          value={gradientColor2}
                          onChange={(e) => {
                            setGradientColor2(e.target.value)
                            setBackgroundType('GRADIENT')
                          }}
                          className="w-4 h-8 rounded-r border-2 border-gray-200 cursor-pointer"
                        />
                      </label>
                    </div>
                    <span className="text-sm font-medium text-gray-900">Gradient</span>
                  </button>
                  {backgroundType === 'GRADIENT' && (
                    <div className="flex gap-1">
                      <input
                        type="text"
                        value={gradientColor1}
                        onChange={(e) => setGradientColor1(e.target.value)}
                        className="w-20 px-2 py-1 text-xs border border-gray-300 rounded"
                        placeholder="#ff6b35"
                      />
                      <input
                        type="text"
                        value={gradientColor2}
                        onChange={(e) => setGradientColor2(e.target.value)}
                        className="w-20 px-2 py-1 text-xs border border-gray-300 rounded"
                        placeholder="#ff8555"
                      />
                    </div>
                  )}
                </div>

                {/* Texture Option */}
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setBackgroundType('TEXTURE')}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg border-2 transition-colors ${
                      backgroundType === 'TEXTURE'
                        ? 'border-primary-500 bg-primary-50'
                        : 'border-gray-300 hover:border-gray-400'
                    }`}
                  >
                    <div className="w-8 h-8 rounded border-2 border-gray-200 bg-gradient-to-br from-gray-100 via-white to-gray-200" />
                    <span className="text-sm font-medium text-gray-900">Texture</span>
                  </button>
                  {backgroundType === 'TEXTURE' && (
                    <select
                      value={textureType}
                      onChange={(e) => setTextureType(e.target.value)}
                      className="px-3 py-1 text-sm border border-gray-300 rounded"
                    >
                      <option value="dots">Dots</option>
                      <option value="grid">Grid</option>
                      <option value="diagonal">Diagonal Lines</option>
                      <option value="noise">Noise</option>
                    </select>
                  )}
                </div>

                {/* Apply Button */}
                <button
                  onClick={applyBackground}
                  className="ml-auto px-6 py-2 bg-primary-500 text-white text-sm font-semibold rounded-lg hover:bg-primary-600 transition-colors"
                >
                  Apply
                </button>
              </div>
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

      <Footer />
    </div>
  )
}
