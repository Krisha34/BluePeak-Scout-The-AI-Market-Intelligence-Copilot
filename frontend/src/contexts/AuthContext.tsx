'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { useRouter, usePathname } from 'next/navigation'

interface User {
  email: string
  name: string
  loginTime: string
}

interface AuthContextType {
  user: User | null
  login: (user: User) => void
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()
  const pathname = usePathname()

  useEffect(() => {
    // Check if user is logged in on mount
    const storedUser = localStorage.getItem('bluepeak_user')
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser))
      } catch (e) {
        localStorage.removeItem('bluepeak_user')
      }
    }
    setLoading(false)
  }, [])

  useEffect(() => {
    // Redirect to login if not authenticated
    if (!loading && !user && pathname !== '/login') {
      router.push('/login')
    }
    // Redirect to home if authenticated and on login page
    if (!loading && user && pathname === '/login') {
      router.push('/')
    }
  }, [user, loading, pathname, router])

  const login = (user: User) => {
    setUser(user)
    localStorage.setItem('bluepeak_user', JSON.stringify(user))
  }

  const logout = () => {
    setUser(null)
    localStorage.removeItem('bluepeak_user')
    router.push('/login')
  }

  const value = {
    user,
    login,
    logout,
    isAuthenticated: !!user
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
