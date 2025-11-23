import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Toaster } from 'react-hot-toast'
import { AuthProvider } from '@/contexts/AuthContext'
import AuthLayout from '@/components/AuthLayout'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'BluePeak Compass - Competitive Intelligence Platform',
  description: 'Multi-agent AI platform for competitive intelligence and market research',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          <AuthLayout>
            {children}
          </AuthLayout>
        </AuthProvider>
        <Toaster position="top-right" />
      </body>
    </html>
  )
}
