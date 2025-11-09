'use client'

import { usePathname } from 'next/navigation'
import Sidebar from '@/components/common/Sidebar'

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const isLoginPage = pathname === '/login'

  if (isLoginPage) {
    // Login page - no sidebar
    return <>{children}</>
  }

  // Regular pages - with sidebar
  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
        {children}
      </main>
    </div>
  )
}
