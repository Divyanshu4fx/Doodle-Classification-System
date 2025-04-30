"use client"

import type React from "react"
import { useEffect, useRef, useState } from "react"
import { Sparkles, RefreshCw, Trash2 } from "lucide-react"
import { Slider } from "@/components/ui/slider"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { toast } from "sonner"

interface Recognition {
  label: string
  confidence: number
}

interface TouchCoordinates {
  offsetX: number
  offsetY: number
}

export default function DoodleCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const contextRef = useRef<CanvasRenderingContext2D | null>(null)
  const [isDrawing, setIsDrawing] = useState(false)
  const [brushSize, setBrushSize] = useState(5)
  const [recognizing, setRecognizing] = useState(false)
  const [recognitionResults, setRecognitionResults] = useState<Recognition[]>([])
  const [hasDrawn, setHasDrawn] = useState(false)
  const timerRef = useRef<NodeJS.Timeout | null>(null)

  // Initialize canvas
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    // Set canvas dimensions
    canvas.width = canvas.offsetWidth * 2
    canvas.height = canvas.offsetHeight * 2
    canvas.style.width = `${canvas.offsetWidth}px`
    canvas.style.height = `${canvas.offsetHeight}px`

    // Get context
    const context = canvas.getContext("2d")
    if (!context) return

    context.scale(2, 2)
    context.lineCap = "round"
    context.strokeStyle = "#000"
    context.lineWidth = brushSize
    contextRef.current = context

    // Clear canvas initially
    context.fillStyle = "white"
    context.fillRect(0, 0, canvas.width, canvas.height)

    // Set up recognition timer
    startRecognitionTimer()

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current)
      }
    }
  }, [brushSize])

  const startRecognitionTimer = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current)
    }

    timerRef.current = setInterval(() => {
      if (hasDrawn) {
        void recognizeDoodle()
      }
    }, 5000)
  }

  const getNativeEventCoordinates = (
    event: React.MouseEvent | React.TouchEvent
  ): TouchCoordinates => {
    if ("touches" in event) {
      const canvas = canvasRef.current
      if (!canvas) return { offsetX: 0, offsetY: 0 }

      const rect = canvas.getBoundingClientRect()
      const touch = event.touches[0]
      return {
        offsetX: touch.clientX - rect.left,
        offsetY: touch.clientY - rect.top,
      }
    }
    
    return {
      offsetX: (event as React.MouseEvent).nativeEvent.offsetX,
      offsetY: (event as React.MouseEvent).nativeEvent.offsetY,
    }
  }

  const startDrawing = (event: React.MouseEvent | React.TouchEvent) => {
    const { offsetX, offsetY } = getNativeEventCoordinates(event)
    if (contextRef.current) {
      contextRef.current.beginPath()
      contextRef.current.moveTo(offsetX, offsetY)
      setIsDrawing(true)
      setHasDrawn(true)
    }
  }

  const finishDrawing = () => {
    if (contextRef.current) {
      contextRef.current.closePath()
      setIsDrawing(false)
    }
  }

  const draw = (event: React.MouseEvent | React.TouchEvent) => {
    if (!isDrawing) return

    const { offsetX, offsetY } = getNativeEventCoordinates(event)
    if (contextRef.current) {
      contextRef.current.lineTo(offsetX, offsetY)
      contextRef.current.stroke()
    }
  }

  const clearCanvas = () => {
    const canvas = canvasRef.current
    if (!canvas || !contextRef.current) return

    contextRef.current.fillStyle = "white"
    contextRef.current.fillRect(0, 0, canvas.width, canvas.height)
    setHasDrawn(false)
    setRecognitionResults([])

    toast.success("Canvas cleared")
  }

  const getMockRecognitionResults = (): Recognition[] => {
    const possibleObjects = [
      "cat", "dog", "house", "tree", "car", "bicycle",
      "flower", "sun", "moon", "star", "face", "bird",
    ]

    const mainObject = possibleObjects[Math.floor(Math.random() * possibleObjects.length)]
    const alternatives = possibleObjects
      .filter(obj => obj !== mainObject)
      .sort(() => 0.5 - Math.random())
      .slice(0, 2)

    return [
      { label: mainObject, confidence: Math.random() * 0.3 + 0.7 },
      { label: alternatives[0], confidence: Math.random() * 0.3 + 0.3 },
      { label: alternatives[1], confidence: Math.random() * 0.2 + 0.1 },
    ]
  }

  const recognizeDoodle = async () => {
    if (!hasDrawn) return

    setRecognizing(true)

    try {
      const canvas = canvasRef.current
      if (!canvas) return

      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 1000))

      const mockResults = getMockRecognitionResults()
      setRecognitionResults(mockResults)

      toast.success("Recognition completed")
    } catch (error) {
      console.error("Error recognizing doodle:", error)
      toast.error("Error recognizing doodle")
    } finally {
      setRecognizing(false)
    }
  }

  const handleManualRecognize = () => {
    if (hasDrawn) {
      void recognizeDoodle()
    } else {
      toast.error("Please draw something before recognizing")
    }
  }

  return (
    <div className="flex flex-col lg:flex-row gap-6">
      <div className="flex-1">
        <div className="relative">
          <canvas
            ref={canvasRef}
            onMouseDown={startDrawing}
            onMouseUp={finishDrawing}
            onMouseMove={draw}
            onMouseLeave={finishDrawing}
            onTouchStart={startDrawing}
            onTouchEnd={finishDrawing}
            onTouchMove={draw}
            className="w-full h-[400px] border-2 border-slate-300 dark:border-slate-700 rounded-lg bg-white touch-none"
          />
          {recognizing && (
            <div className="absolute inset-0 flex items-center justify-center bg-black/10 rounded-lg">
              <div className="bg-white dark:bg-slate-800 p-4 rounded-lg shadow-lg flex items-center gap-2">
                <RefreshCw className="animate-spin h-5 w-5" />
                <span>Recognizing your doodle...</span>
              </div>
            </div>
          )}
        </div>

        <div className="mt-4 flex flex-col sm:flex-row gap-4">
          <div className="flex-1 flex items-center gap-2">
            <span className="text-sm font-medium min-w-[80px]">Brush size:</span>
            <Slider
              value={[brushSize]}
              min={1}
              max={20}
              step={1}
              onValueChange={(value) => setBrushSize(value[0])}
              className="flex-1"
            />
            <span className="text-sm font-medium w-6">{brushSize}</span>
          </div>

          <div className="flex gap-2">
            <Button variant="outline" onClick={clearCanvas} className="flex-1 sm:flex-none">
              <Trash2 className="mr-2 h-4 w-4" />
              Clear
            </Button>
            <Button onClick={handleManualRecognize} className="flex-1 sm:flex-none">
              <Sparkles className="mr-2 h-4 w-4" />
              Recognize
            </Button>
          </div>
        </div>
      </div>

      <Card className="w-full lg:w-80">
        <CardContent className="pt-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <Sparkles className="mr-2 h-5 w-5 text-yellow-500" />
            Recognition Results
          </h3>

          {recognitionResults.length > 0 ? (
            <div className="space-y-4">
              {recognitionResults.map((result, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <Badge
                      variant={index === 0 ? "default" : "outline"}
                      className={index === 0 ? "bg-green-500 hover:bg-green-600" : ""}
                    >
                      {(result.confidence * 100).toFixed(0)}%
                    </Badge>
                    <span className="ml-2 font-medium capitalize">{result.label}</span>
                  </div>
                  <div className="w-24 bg-slate-200 dark:bg-slate-700 rounded-full h-2">
                    <div className="bg-green-500 h-2 rounded-full" style={{ width: `${result.confidence * 100}%` }} />
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-slate-500 dark:text-slate-400">
              <p>Draw something on the canvas</p>
              <p className="text-sm mt-1">Recognition results will appear here</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
