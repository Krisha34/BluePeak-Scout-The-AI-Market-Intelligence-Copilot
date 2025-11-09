'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Lock, Mail, ArrowRight } from 'lucide-react'
import toast from 'react-hot-toast'
import { useAuth } from '@/contexts/AuthContext'

// Demo users - no password needed for demo
const DEMO_USERS = [
  'admin@bluepeak.ai',
  'user@bluepeak.ai',
  'demo@bluepeak.ai',
  'moneshrallapalli@gmail.com'
]

export default function LoginPage() {
  const router = useRouter()
  const { login } = useAuth()
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!email) {
      toast.error('Please enter your email')
      return
    }

    setLoading(true)

    // Simulate API call delay
    setTimeout(() => {
      // Check if email is in demo users list (case insensitive)
      const isValidUser = DEMO_USERS.some(
        user => user.toLowerCase() === email.toLowerCase()
      )

      if (isValidUser) {
        // Create user object
        const user = {
          email: email.toLowerCase(),
          name: email.split('@')[0],
          loginTime: new Date().toISOString()
        }

        // Use the login function from AuthContext
        login(user)
        toast.success(`Welcome back, ${user.name}!`)

        // Redirect will happen automatically via AuthContext
        setTimeout(() => {
          router.push('/')
        }, 500)
      } else {
        toast.error('Email not authorized. Please contact admin.')
        setLoading(false)
      }
    }, 800)
  }

  const quickLogin = (demoEmail: string) => {
    setEmail(demoEmail)
    setTimeout(() => {
      const event = new Event('submit', { bubbles: true, cancelable: true })
      document.querySelector('form')?.dispatchEvent(event)
    }, 100)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo & Title */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-2xl mb-4">
            <Lock className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">BluePeak Compass</h1>
          <p className="text-gray-600">AI-Powered Competitive Intelligence</p>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Welcome Back</h2>
            <p className="text-gray-600">Sign in to access your dashboard</p>
          </div>

          <form onSubmit={handleLogin} className="space-y-6">
            {/* Email Input */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                Email Address
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="you@example.com"
                  disabled={loading}
                />
              </div>
            </div>

            {/* Login Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Signing in...
                </>
              ) : (
                <>
                  Sign In
                  <ArrowRight className="w-5 h-5" />
                </>
              )}
            </button>
          </form>

          {/* Demo Users */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <p className="text-sm text-gray-600 mb-3 text-center">Quick Demo Login:</p>
            <div className="grid grid-cols-2 gap-2">
              {DEMO_USERS.slice(0, 4).map((demoEmail) => (
                <button
                  key={demoEmail}
                  onClick={() => quickLogin(demoEmail)}
                  disabled={loading}
                  className="px-3 py-2 text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors disabled:opacity-50"
                >
                  {demoEmail}
                </button>
              ))}
            </div>
          </div>

          {/* Info */}
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <p className="text-sm text-blue-800">
              <strong>Demo Mode:</strong> This is a demonstration login. Use any of the demo emails above or enter an authorized email.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-600">
          <p>© 2025 BluePeak Compass. All rights reserved.</p>
        </div>
      </div>
    </div>
  )
}
