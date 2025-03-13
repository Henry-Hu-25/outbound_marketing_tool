"use client"

import { useEffect, useState, useRef, FormEvent } from "react"
import { useTheme } from "next-themes"
import { motion } from "framer-motion"
import { Particles } from "@/components/ui/particles"
import { UrlInput } from "@/components/UrlInput"
import { ParticleButton } from "@/components/ui/particle-button"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export function ParticlesBackground({
  title = "Particles Background",
}: {
  title?: string;
}) {
  const { theme } = useTheme()
  const [color, setColor] = useState("#ffffff")
  const words = title.split(" ")
  
  // Form state
  const [productUrl, setProductUrl] = useState("")
  const [clientUrl, setClientUrl] = useState("")
  const [error, setError] = useState("")
  
  // Refs for URL inputs
  const productUrlRef = useRef<HTMLInputElement>(null)
  const clientUrlRef = useRef<HTMLInputElement>(null)
  
  // Router for navigation
  const router = useRouter()

  useEffect(() => {
    setColor(theme === "dark" ? "#ffffff" : "#000000")
  }, [theme])
  
  function validateAndGetUrls() {
    if (!productUrl) {
      setError("Please enter a product URL")
      productUrlRef.current?.focus()
      return null
    }
    
    if (!clientUrl) {
      setError("Please enter a client URL")
      clientUrlRef.current?.focus()
      return null
    }
    
    // Format URLs if they don't include https://
    const formattedProductUrl = productUrl.startsWith('http') ? productUrl : `https://${productUrl}`
    const formattedClientUrl = clientUrl.startsWith('http') ? clientUrl : `https://${clientUrl}`
    
    return {
      productUrl: formattedProductUrl,
      clientUrl: formattedClientUrl
    }
  }
  
  // Handle form submission
  const handleSubmit = (e?: FormEvent) => {
    // Prevent default form submission if event is provided
    if (e) e.preventDefault()
    
    console.log("Submit handler called")
    
    // Reset error state
    setError("")
    
    // Validate inputs and get formatted URLs
    const urls = validateAndGetUrls()
    if (!urls) return
    
    console.log("Validated URLs:", urls)
    
    // Construct the URL for navigation
    const navigateUrl = `/results?productUrl=${encodeURIComponent(urls.productUrl)}&clientUrl=${encodeURIComponent(urls.clientUrl)}`
    console.log("Navigating to:", navigateUrl)
    
    // Navigate using router
    router.push(navigateUrl)
  }
  
  // Direct navigation fallback
  const handleDirectNavigate = () => {
    const urls = validateAndGetUrls()
    if (!urls) return
    
    const navigateUrl = `/results?productUrl=${encodeURIComponent(urls.productUrl)}&clientUrl=${encodeURIComponent(urls.clientUrl)}`
    window.location.href = navigateUrl
  }

  return (
    <div className="relative min-h-screen w-full flex items-center justify-center overflow-hidden bg-white dark:bg-neutral-950">
      <Particles
        className="absolute inset-0"
        quantity={100}
        staticity={50}
        ease={50}
        size={1}
        color={color}
        refresh={false}
      />

      <div className="relative z-10 container mx-auto px-4 md:px-6 text-center">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 2 }}
          className="max-w-4xl mx-auto"
        >
          <h1 className="text-5xl sm:text-6xl md:text-7xl font-bold mb-12 tracking-tighter">
            {words.map((word, wordIndex) => (
              <span
                key={wordIndex}
                className="inline-block mr-4 last:mr-0"
              >
                {word.split("").map((letter, letterIndex) => (
                  <motion.span
                    key={`${wordIndex}-${letterIndex}`}
                    initial={{ y: 100, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{
                      delay:
                        wordIndex * 0.1 +
                        letterIndex * 0.03,
                      type: "spring",
                      stiffness: 150,
                      damping: 25,
                    }}
                    className="inline-block text-transparent bg-clip-text 
                    bg-gradient-to-r from-neutral-900 to-neutral-700/80 
                    dark:from-white dark:to-white/80"
                  >
                    {letter}
                  </motion.span>
                ))}
              </span>
            ))}
          </h1>

          <form onSubmit={handleSubmit} className="flex flex-col gap-6 mt-10 items-center">
            <UrlInput 
              label="Input client product info (online product url)" 
              placeholder="product-page.com"
              onChange={(e) => setProductUrl(e.target.value)}
              value={productUrl}
              ref={productUrlRef}
            />
            <UrlInput 
              label="Input client info (client about us)" 
              placeholder="company-about.com"
              onChange={(e) => setClientUrl(e.target.value)}
              value={clientUrl}
              ref={clientUrlRef}
            />
            
            {error && (
              <p className="text-red-600 dark:text-red-400 mt-2">{error}</p>
            )}
            
            <div className="mt-6 flex flex-wrap gap-4 justify-center">
              {/* Primary submission button with particles effect */}
              <ParticleButton 
                type="button"
                className="px-8 py-3 text-lg bg-black text-white hover:bg-black/90 dark:bg-white dark:text-black dark:hover:bg-white/90"
                onClick={handleSubmit}
              >
                Generate Email
              </ParticleButton>
              
              {/* Debug navigation buttons - hidden by default */}
              <div className="hidden">
                <Button
                  type="submit"
                  className="px-8 py-3 text-lg bg-blue-500 text-white"
                >
                  Form Submit
                </Button>
                
                <Button
                  type="button"
                  onClick={handleDirectNavigate}
                  className="px-8 py-3 text-lg bg-green-500 text-white"
                >
                  Direct Navigate
                </Button>
                
                <Link 
                  href="/debug" 
                  className="px-8 py-3 text-lg bg-purple-500 text-white rounded"
                >
                  Debug Page
                </Link>
              </div>
            </div>
          </form>
        </motion.div>
      </div>
    </div>
  )
} 