import { Navigate } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'

interface ProtectedRouteProps {
  children: React.ReactNode
}

/**
 * Protected Route Component
 * Redirects to login if user is not authenticated
 */
export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, accessToken } = useAuthStore()

  // Check if user is authenticated (has token)
  if (!isAuthenticated || !accessToken) {
    // Redirect to login page if not authenticated
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}
