/**
 * API Service Layer
 * Real API integration with backend services
 */

import axios, { AxiosInstance, AxiosError } from 'axios'
import toast from 'react-hot-toast'

// API Configuration - Remove trailing slashes to prevent malformed URLs
const API_BASE_URL = (import.meta.env.VITE_API_URL || 'http://localhost:3001').replace(/\/$/, '')
const API_VERSION = 'v1'
const API_PREFIX = `/api/${API_VERSION}`

/**
 * Create axios instance with default configuration
 */
const apiClient: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}${API_PREFIX}`,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Include cookies for CORS
})

console.log('🔧 API Client initialized:', {
  baseURL: `${API_BASE_URL}${API_PREFIX}`,
  timeout: 30000,
  withCredentials: true
})

/**
 * Request interceptor - Add auth token to requests
 */
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

/**
 * Response interceptor - Handle errors and token refresh
 */
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as any

    // Enhanced error logging for debugging
    console.error('❌ API Error:', {
      url: error.config?.url,
      method: error.config?.method,
      baseURL: error.config?.baseURL,
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      message: error.message,
    })

    // Handle 401 Unauthorized - Token expired
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        // Try to refresh the token
        const refreshToken = localStorage.getItem('refreshToken')
        if (refreshToken) {
          const response = await axios.post(
            `${API_BASE_URL}${API_PREFIX}/auth/refresh`,
            { refreshToken }
          )

          const { accessToken } = response.data.data
          localStorage.setItem('accessToken', accessToken)

          // Retry the original request with new token
          originalRequest.headers.Authorization = `Bearer ${accessToken}`
          return apiClient(originalRequest)
        }
      } catch (refreshError) {
        // Refresh failed - logout user
        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

/**
 * Authentication API
 */
export const authApi = {
  /**
   * Login user
   */
  login: async (credentials: { email: string; password: string }) => {
    try {
      const response = await apiClient.post('/auth/login', credentials)
      const { accessToken, refreshToken, user } = response.data.data

      // Store tokens
      localStorage.setItem('accessToken', accessToken)
      localStorage.setItem('refreshToken', refreshToken)

      return { success: true, data: { user, accessToken, refreshToken } }
    } catch (error: any) {
      const message = error.response?.data?.message || 'Login failed'
      toast.error(message)
      return { success: false, data: { user: null, accessToken: '', refreshToken: '' }, error: message }
    }
  },

  /**
   * Register new user
   */
  register: async (data: {
    email: string
    password: string
    fullName: string
  }) => {
    try {
      const response = await apiClient.post('/auth/register', data)
      const { accessToken, refreshToken, user } = response.data.data

      // Store tokens
      localStorage.setItem('accessToken', accessToken)
      localStorage.setItem('refreshToken', refreshToken)

      return { success: true, data: { user, accessToken, refreshToken } }
    } catch (error: any) {
      const message = error.response?.data?.message || 'Registration failed'
      toast.error(message)
      return { success: false, data: { user: null, accessToken: '', refreshToken: '' }, error: message }
    }
  },

  /**
   * Logout user
   */
  logout: async () => {
    try {
      await apiClient.post('/auth/logout')
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      return { success: true }
    } catch (error: any) {
      // Still clear local storage even if API call fails
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      return { success: true }
    }
  },
}

/**
 * User API
 */
export const userApi = {
  /**
   * Get user profile
   */
  getProfile: async () => {
    try {
      const response = await apiClient.get('/users/profile')
      return { success: true, data: response.data.data }
    } catch (error: any) {
      const message = error.response?.data?.message || 'Failed to fetch profile'
      return { success: false, error: message }
    }
  },

  /**
   * Get user credits
   */
  getCredits: async () => {
    try {
      const response = await apiClient.get('/users/credits')
      return { success: true, data: response.data.data }
    } catch (error: any) {
      const message = error.response?.data?.message || 'Failed to fetch credits'
      return { success: false, error: message }
    }
  },
}

/**
 * Image API
 */
export const imageApi = {
  /**
   * Upload and process image
   */
  upload: async (formData: FormData) => {
    try {
      const response = await apiClient.post('/images/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 60000, // 60 seconds for upload
      })
      return { success: true, data: response.data.data }
    } catch (error: any) {
      const message = error.response?.data?.message || 'Upload failed'
      return { success: false, data: null, error: message }
    }
  },

  /**
   * Get all user images
   */
  getImages: async (params?: {
    page?: number
    limit?: number
    status?: string
  }) => {
    try {
      const response = await apiClient.get('/images', { params })
      return { success: true, data: response.data.data }
    } catch (error: any) {
      const message = error.response?.data?.message || 'Failed to fetch images'
      return { success: false, data: [], error: message }
    }
  },

  /**
   * Alias for getImages
   */
  getAll: async (params?: {
    page?: number
    limit?: number
    status?: string
  }) => {
    return imageApi.getImages(params)
  },

  /**
   * Get single image by ID
   */
  getById: async (id: string) => {
    try {
      const response = await apiClient.get(`/images/${id}`)
      return { success: true, data: response.data.data }
    } catch (error: any) {
      const message = error.response?.data?.message || 'Failed to fetch image'
      return { success: false, data: null, error: message }
    }
  },

  /**
   * Download processed image
   */
  download: async (id: string, tier: 'SMALL' | 'MEDIUM' | 'LARGE' = 'SMALL') => {
    try {
      const response = await apiClient.get(`/images/${id}/download`, {
        params: { tier },
        responseType: 'blob',
      })
      return { success: true, data: response.data }
    } catch (error: any) {
      const message = error.response?.data?.message || 'Download failed'
      return { success: false, data: null, error: message }
    }
  },

  /**
   * Alias for download
   */
  downloadImage: async (id: string, tier: 'SMALL' | 'MEDIUM' | 'LARGE' = 'SMALL') => {
    return imageApi.download(id, tier)
  },

  /**
   * Delete image
   */
  delete: async (id: string) => {
    try {
      const response = await apiClient.delete(`/images/${id}`)
      return { success: true, data: response.data.data }
    } catch (error: any) {
      const message = error.response?.data?.message || 'Delete failed'
      return { success: false, error: message }
    }
  },

  /**
   * Alias for delete
   */
  deleteImage: async (id: string) => {
    return imageApi.delete(id)
  },

  /**
   * Apply background to processed image
   * Note: This is a frontend-only feature for now
   * In the future, this could be a backend API endpoint
   */
  applyBackground: async (
    id: string,
    config: {
      backgroundType: string
      solidColor?: string
      gradientColor1?: string
      gradientColor2?: string
      textureType?: string
    }
  ) => {
    try {
      // For now, this is just a placeholder
      // In a real implementation, you might have a backend endpoint like:
      // const response = await apiClient.post(`/images/${id}/background`, config)
      // return { success: true, data: response.data.data }

      // Simulate success for frontend background application
      return { success: true, data: { id, config } }
    } catch (error: any) {
      const message = error.response?.data?.message || 'Failed to apply background'
      return { success: false, data: null, error: message }
    }
  },
}

export default apiClient
