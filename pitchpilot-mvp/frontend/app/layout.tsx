import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'PitchPilot AI | Strategic Pitch Deck Architect',
  description: 'AI-powered pitch deck generation with market verification',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-background text-on-surface">
        {children}
      </body>
    </html>
  )
}