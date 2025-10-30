import type React from "react"
import type { Metadata } from "next"
import { Lora, Lato } from "next/font/google"
import { Analytics } from "@vercel/analytics/next"
import "./globals.css"

const lora = Lora({ subsets: ["latin"], variable: "--font-serif" })
const lato = Lato({ weight: ["400", "700"], subsets: ["latin"], variable: "--font-sans" })

export const metadata: Metadata = {
  title: "Daudi's Perspective",
  description: "Engineering, Aviation, and Technology from an African Perspective",
    generator: 'v0.app'
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`${lora.variable} ${lato.variable}`}>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
