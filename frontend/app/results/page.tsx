"use client";

import React, { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { TextGenerateEffect } from "@/components/ui/text-generate-effect";
import { generateEmail } from "@/lib/api";
import { Particles } from "@/components/ui/particles";
import { useTheme } from "next-themes";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { ArrowLeft, Copy, Check } from "lucide-react";

interface DebugInfo {
  pingError?: unknown;
  fetchError?: unknown;
  manualFetchError?: unknown;
  [key: string]: unknown;
}

export default function ResultsPage() {
  const searchParams = useSearchParams();
  const productUrl = searchParams.get("productUrl") || "";
  const clientUrl = searchParams.get("clientUrl") || "";
  
  const [emailContent, setEmailContent] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [debugInfo, setDebugInfo] = useState<DebugInfo>({});
  const [isCopied, setIsCopied] = useState(false);
  
  const { theme } = useTheme();
  const [color, setColor] = useState("#ffffff");
  
  useEffect(() => {
    setColor(theme === "dark" ? "#ffffff" : "#000000");
  }, [theme]);
  
  useEffect(() => {
    console.log("Results page mounted with URLs:", { productUrl, clientUrl });
    
    if (!productUrl || !clientUrl) {
      setError("Missing product or client URL parameters");
      setIsLoading(false);
      return;
    }
    
    async function fetchEmail() {
      try {
        console.log("Attempting to fetch email with URLs:", { productUrl, clientUrl });
        
        // Check server connectivity first
        try {
          const pingResponse = await fetch("http://localhost:5001/api/health", { 
            method: "GET"
          });
          console.log("Server health check result:", pingResponse);
        } catch (pingErr) {
          console.error("Server health check failed:", pingErr);
          setDebugInfo(prev => ({ ...prev, pingError: pingErr }));
        }
        
        const response = await generateEmail(productUrl, clientUrl);
        console.log("API response:", response);
        setEmailContent(response.email_content);
      } catch (err) {
        console.error("Error generating email:", err);
        setDebugInfo(prev => ({ ...prev, fetchError: err }));
        
        // More detailed error message
        let errorMessage = "Failed to generate email.";
        
        if (err instanceof Error) {
          errorMessage += ` ${err.message}`;
          if (err.message.includes("Failed to fetch")) {
            errorMessage += " - This might be because the API server is not running or unreachable.";
          }
        }
        
        setError(errorMessage);
      } finally {
        setIsLoading(false);
      }
    }
    
    fetchEmail();
  }, [productUrl, clientUrl]);
  
  const handleRetryManually = async () => {
    setIsLoading(true);
    setError("");
    
    // Manually construct and execute the fetch
    try {
      const manualResponse = await fetch("http://localhost:5001/api/generate-email", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          product_url: productUrl,
          client_url: clientUrl,
        }),
      });
      
      const data = await manualResponse.json();
      console.log("Manual fetch response:", data);
      
      if (data.email_content) {
        setEmailContent(data.email_content);
      } else {
        setError("Received response but no email content found.");
      }
    } catch (err) {
      console.error("Manual fetch error:", err);
      setError(`Manual fetch failed: ${err instanceof Error ? err.message : String(err)}`);
      setDebugInfo(prev => ({ ...prev, manualFetchError: err }));
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleCopyToClipboard = () => {
    if (emailContent) {
      navigator.clipboard.writeText(emailContent);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    }
  };
  
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
      
      <div className="relative z-10 container mx-auto px-4 md:px-6 py-12">
        <div className="max-w-4xl mx-auto">
          <div className="mb-10 flex items-center justify-between">
            <Link href="/">
              <Button
                variant="outline"
                className="bg-white/20 backdrop-blur-sm border-black dark:border-white text-black dark:text-white"
              >
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back to Generator
              </Button>
            </Link>
            
            {!isLoading && !error && emailContent && (
              <Button
                variant="outline"
                className="bg-white/20 backdrop-blur-sm border-black dark:border-white text-black dark:text-white"
                onClick={handleCopyToClipboard}
              >
                {isCopied ? (
                  <>
                    <Check className="mr-2 h-4 w-4" />
                    Copied!
                  </>
                ) : (
                  <>
                    <Copy className="mr-2 h-4 w-4" />
                    Copy Email
                  </>
                )}
              </Button>
            )}
          </div>
          
          <div className="bg-white/20 backdrop-blur-md rounded-lg p-8 border border-black dark:border-white">
            <h1 className="text-4xl font-bold mb-8 text-center text-transparent bg-clip-text bg-gradient-to-r from-neutral-900 to-neutral-700/80 dark:from-white dark:to-white/80">
              Your Generated Email
            </h1>
            
            {isLoading ? (
              <div className="flex justify-center items-center h-64">
                <div className="animate-pulse text-2xl text-black dark:text-white">
                  Generating your email...
                </div>
              </div>
            ) : error ? (
              <div className="bg-red-100 dark:bg-red-900/30 border border-red-400 text-red-700 dark:text-red-300 px-4 py-3 rounded">
                <p>{error}</p>
                
                <div className="mt-6 space-y-3">
                  <Button 
                    onClick={handleRetryManually}
                    className="bg-blue-600 hover:bg-blue-700 text-white"
                  >
                    Retry Manually
                  </Button>
                  
                  <Link href="/" className="block">
                    <Button 
                      variant="outline"
                      className="w-full"
                    >
                      Go back and try again
                    </Button>
                  </Link>
                </div>
                
                {Object.keys(debugInfo).length > 0 && (
                  <div className="mt-6 p-4 bg-gray-100 dark:bg-gray-800 rounded text-xs overflow-auto max-h-40">
                    <h3 className="font-bold mb-2">Debug Information:</h3>
                    <pre>{JSON.stringify(debugInfo, null, 2)}</pre>
                  </div>
                )}
              </div>
            ) : (
              <div className="bg-white dark:bg-black/70 p-6 md:p-8 rounded shadow-inner">
                <div className="prose dark:prose-invert prose-sm md:prose-base max-w-none">
                  <TextGenerateEffect words={emailContent} className="text-left" duration={0.3} />
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
} 