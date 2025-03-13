"use client";
import { useEffect } from "react";
import { motion, stagger, useAnimate } from "framer-motion";
import { cn } from "@/lib/utils";

export const TextGenerateEffect = ({
  words,
  className,
  filter = true,
  duration = 0.5,
}: {
  words: string;
  className?: string;
  filter?: boolean;
  duration?: number;
}) => {
  const [scope, animate] = useAnimate();
  
  useEffect(() => {
    animate(
      "span",
      {
        opacity: 1,
        filter: filter ? "blur(0px)" : "none",
      },
      {
        duration: duration ? duration : 1,
        delay: stagger(0.1),
      }
    );
  }, [scope.current, animate, duration, filter]);

  const renderFormattedContent = () => {
    // Split the text into paragraphs (based on double newlines)
    const paragraphs = words.split(/\n\s*\n|\n{2,}/);
    
    return (
      <motion.div ref={scope} className="space-y-6">
        {paragraphs.map((paragraph, paragraphIndex) => {
          // Skip empty paragraphs
          if (!paragraph.trim()) return null;
          
          // Split paragraph into words and keep single newlines as separate elements
          const lines = paragraph.split(/\n/);
          
          return (
            <motion.div 
              key={`paragraph-${paragraphIndex}`} 
              className="paragraph"
            >
              {lines.map((line, lineIndex) => {
                const lineWords = line.split(" ");
                
                return (
                  <motion.div key={`line-${paragraphIndex}-${lineIndex}`} className="leading-relaxed">
                    {lineWords.map((word, wordIndex) => (
                      <motion.span
                        key={`word-${paragraphIndex}-${lineIndex}-${wordIndex}`}
                        className="dark:text-white text-black opacity-0"
                        style={{
                          filter: filter ? "blur(10px)" : "none",
                        }}
                      >
                        {word}{wordIndex < lineWords.length - 1 ? " " : ""}
                      </motion.span>
                    ))}
                  </motion.div>
                );
              })}
            </motion.div>
          );
        })}
      </motion.div>
    );
  };

  return (
    <div className={cn("font-normal", className)}>
      <div className="mt-4">
        <div className="dark:text-white text-black text-base md:text-lg leading-relaxed tracking-normal">
          {renderFormattedContent()}
        </div>
      </div>
    </div>
  );
}; 