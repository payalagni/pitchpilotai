'use client'

import { useState, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Upload, FileText, Brain, Layout, Download, 
  CheckCircle, AlertCircle, Loader2, Sparkles,
  ChevronRight, X, Plus, Trash2, Search
} from 'lucide-react'
import clsx from 'clsx'

// Types
interface DeckData {
  company_name: string
  founder_name: string
  slide_1_hook: string
  slide_2_empathy: string
  slide_3_opportunity: string
  slide_4_solution: string
  slide_5_market: string
  slide_6_model: string
  slide_7_competition: string
  slide_8_tech: string
  slide_9_traction: string
  slide_10_ask: string
}

interface ProcessingStatus {
  step: 'intake' | 'verification' | 'blueprint' | 'export' | 'complete' | 'error'
  message: string
  progress: number
}

// Steps configuration
const STEPS = [
  { id: 1, name: 'File Intake', icon: Upload },
  { id: 2, name: 'AI Verification', icon: Brain },
  { id: 3, name: 'Deck Blueprint', icon: Layout },
  { id: 4, name: 'Export', icon: Download },
]

// API functions
const API_BASE = 'http://localhost:8000'

async function uploadFile(file: File): Promise<{ content: string }> {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await fetch(`${API_BASE}/api/upload`, {
    method: 'POST',
    body: formData,
  })
  
  return response.json()
}

async function generateDeck(data: {
  company_name: string
  founder_name: string
  raw_content: string
  target_audience: string
  funding_amount: string
  deck_purpose: string
}): Promise<{ deck_id: string; deck_data: DeckData; pptx_path: string }> {
  const response = await fetch(`${API_BASE}/api/deck/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  
  return response.json()
}

async function downloadDeck(deckId: string): Promise<Blob> {
  const response = await fetch(`${API_BASE}/api/deck/${deckId}/download`)
  return response.blob()
}

// Components
function StepIndicator({ currentStep }: { currentStep: number }) {
  return (
    <div className="flex items-center justify-center gap-2 mb-8">
      {STEPS.map((step, index) => {
        const Icon = step.icon
        const isActive = currentStep === step.id
        const isCompleted = currentStep > step.id
        
        return (
          <motion.div
            key={step.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className={clsx(
              'flex items-center gap-2 px-4 py-2 rounded-full transition-all',
              isActive && 'step-active',
              isCompleted && 'step-completed',
              !isActive && !isCompleted && 'step-pending'
            )}
          >
            <Icon className="w-4 h-4" />
            <span className="text-sm font-medium">{step.name}</span>
            {index < STEPS.length - 1 && (
              <ChevronRight className="w-4 h-4 opacity-50" />
            )}
          </motion.div>
        )
      })}
    </div>
  )
}

function ThinkingPulse({ status }: { status: ProcessingStatus }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col items-center gap-4 py-12"
    >
      <div className="flex gap-3">
        <div className="thinking-dot w-3 h-3 rounded-full bg-primary" />
        <div className="thinking-dot w-3 h-3 rounded-full bg-primary" />
        <div className="thinking-dot w-3 h-3 rounded-full bg-primary" />
      </div>
      <p className="text-on-surface-variant">{status.message}</p>
      <div className="w-64 h-2 bg-surface-container-high rounded-full overflow-hidden">
        <motion.div
          className="h-full bg-primary rounded-full"
          initial={{ width: 0 }}
          animate={{ width: `${status.progress}%` }}
          transition={{ duration: 0.5 }}
        />
      </div>
      <p className="text-label-caps text-on-surface-variant">
        {status.progress}% complete
      </p>
    </motion.div>
  )
}

function FileUploadZone({ 
  onFilesAdded 
}: { 
  onFilesAdded: (files: File[], content: string) => void 
}) {
  const [isDragging, setIsDragging] = useState(false)
  const [files, setFiles] = useState<File[]>([])
  const [extractedContent, setExtractedContent] = useState('')
  
  const handleDrop = useCallback(async (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    
    const droppedFiles = Array.from(e.dataTransfer.files)
    setFiles(prev => [...prev, ...droppedFiles])
    
    // Process files
    for (const file of droppedFiles) {
      try {
        const result = await uploadFile(file)
        setExtractedContent(prev => prev + '\n\n' + result.content)
      } catch (error) {
        console.error('Error processing file:', error)
      }
    }
  }, [])
  
  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const newFiles = Array.from(e.target.files)
      setFiles(prev => [...prev, ...newFiles])
      
      for (const file of newFiles) {
        try {
          const result = await uploadFile(file)
          setExtractedContent(prev => prev + '\n\n' + result.content)
        } catch (error) {
          console.error('Error processing file:', error)
        }
      }
    }
  }
  
  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index))
  }
  
  useEffect(() => {
    if (files.length > 0 && extractedContent) {
      onFilesAdded(files, extractedContent)
    }
  }, [files, extractedContent, onFilesAdded])
  
  return (
    <div className="space-y-6">
      <div
        className={clsx(
          'drop-zone p-12 rounded-xl text-center cursor-pointer',
          isDragging && 'active'
        )}
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true) }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        onClick={() => document.getElementById('file-input')?.click()}
      >
        <Upload className="w-12 h-12 mx-auto mb-4 text-primary" />
        <h3 className="text-h2 mb-2">Drop files here</h3>
        <p className="text-on-surface-variant">
          or click to browse • PDF, DOCX, TXT, Images
        </p>
        <input
          id="file-input"
          type="file"
          multiple
          accept=".pdf,.docx,.txt,.png,.jpg,.jpeg"
          className="hidden"
          onChange={handleFileSelect}
        />
      </div>
      
      {files.length > 0 && (
        <div className="space-y-2">
          <h4 className="text-label-caps text-on-surface-variant">UPLOADED FILES</h4>
          {files.map((file, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-3 bg-surface-container rounded-lg"
            >
              <div className="flex items-center gap-3">
                <FileText className="w-5 h-5 text-primary" />
                <span>{file.name}</span>
                <span className="text-on-surface-variant text-sm">
                  ({(file.size / 1024).toFixed(1)} KB)
                </span>
              </div>
              <button
                onClick={() => removeFile(index)}
                className="p-1 hover:bg-surface-container-high rounded"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

function CompanyForm({ 
  onSubmit 
}: { 
  onSubmit: (data: {
    company_name: string
    founder_name: string
    raw_content: string
    target_audience: string
    funding_amount: string
    deck_purpose: string
  }) => void
}) {
  const [formData, setFormData] = useState({
    company_name: '',
    founder_name: '',
    raw_content: '',
    target_audience: 'VC',
    funding_amount: '',
    deck_purpose: 'Seed Round',
  })
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }
  
  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-label-caps text-on-surface-variant mb-2">
            COMPANY NAME *
          </label>
          <input
            type="text"
            required
            className="input-field"
            placeholder="Acme AI"
            value={formData.company_name}
            onChange={(e) => setFormData({ ...formData, company_name: e.target.value })}
          />
        </div>
        <div>
          <label className="block text-label-caps text-on-surface-variant mb-2">
            FOUNDER NAME
          </label>
          <input
            type="text"
            className="input-field"
            placeholder="John Doe"
            value={formData.founder_name}
            onChange={(e) => setFormData({ ...formData, founder_name: e.target.value })}
          />
        </div>
      </div>
      
      <div>
        <label className="block text-label-caps text-on-surface-variant mb-2">
          PITCH NOTES / DESCRIPTION
        </label>
        <textarea
          className="input-field min-h-[150px]"
          placeholder="Describe your startup, product, target market, competitive advantage..."
          value={formData.raw_content}
          onChange={(e) => setFormData({ ...formData, raw_content: e.target.value })}
        />
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="block text-label-caps text-on-surface-variant mb-2">
            TARGET AUDIENCE
          </label>
          <select
            className="input-field"
            value={formData.target_audience}
            onChange={(e) => setFormData({ ...formData, target_audience: e.target.value })}
          >
            <option value="VC">VC</option>
            <option value="Angel">Angel Investor</option>
            <option value="Corporate">Corporate</option>
            <option value="Accelerator">Accelerator</option>
          </select>
        </div>
        <div>
          <label className="block text-label-caps text-on-surface-variant mb-2">
            FUNDING AMOUNT
          </label>
          <input
            type="text"
            className="input-field"
            placeholder="$2M"
            value={formData.funding_amount}
            onChange={(e) => setFormData({ ...formData, funding_amount: e.target.value })}
          />
        </div>
        <div>
          <label className="block text-label-caps text-on-surface-variant mb-2">
            DECK PURPOSE
          </label>
          <select
            className="input-field"
            value={formData.deck_purpose}
            onChange={(e) => setFormData({ ...formData, deck_purpose: e.target.value })}
          >
            <option value="Seed Round">Seed Round</option>
            <option value="Series A">Series A</option>
            <option value="Series B">Series B</option>
            <option value="Bridge Round">Bridge Round</option>
          </select>
        </div>
      </div>
      
      <button
        type="submit"
        className="btn-primary w-full flex items-center justify-center gap-2"
      >
        <Sparkles className="w-5 h-5" />
        Generate Pitch Deck
      </button>
    </form>
  )
}

function DeckPreview({ deckData }: { deckData: DeckData }) {
  const slideTitles = [
    { key: 'slide_1_hook', title: 'The Hook' },
    { key: 'slide_2_empathy', title: 'Empathy' },
    { key: 'slide_3_opportunity', title: 'Opportunity' },
    { key: 'slide_4_solution', title: 'Solution' },
    { key: 'slide_5_market', title: 'Market' },
    { key: 'slide_6_model', title: 'Business Model' },
    { key: 'slide_7_competition', title: 'Competition' },
    { key: 'slide_8_tech', title: 'Technology' },
    { key: 'slide_9_traction', title: 'Traction' },
    { key: 'slide_10_ask', title: 'The Ask' },
  ]
  
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {slideTitles.map((slide, index) => (
          <motion.div
            key={slide.key}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            className="p-4 bg-surface-container rounded-lg"
          >
            <div className="flex items-center gap-2 mb-2">
              <span className="text-label-caps text-primary">{index + 1}</span>
              <h4 className="font-semibold">{slide.title}</h4>
            </div>
            <p className="text-on-surface-variant text-sm">
              {deckData[slide.key as keyof DeckData]}
            </p>
          </motion.div>
        ))}
      </div>
    </div>
  )
}

function ExportSection({ 
  deckId, 
  onDownload 
}: { 
  deckId: string
  onDownload: () => void
}) {
  return (
    <div className="text-center py-12">
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        className="w-20 h-20 mx-auto mb-6 rounded-full bg-primary-container flex items-center justify-center"
      >
        <CheckCircle className="w-10 h-10 text-primary" />
      </motion.div>
      
      <h2 className="text-h1 mb-2">Your Pitch Deck is Ready!</h2>
      <p className="text-on-surface-variant mb-8">
        Your 10-slide investor deck has been generated with AI-verified market data.
      </p>
      
      <button
        onClick={onDownload}
        className="btn-primary inline-flex items-center gap-2"
      >
        <Download className="w-5 h-5" />
        Download PowerPoint
      </button>
      
      <p className="text-label-caps text-on-surface-variant mt-4">
        Deck ID: {deckId}
      </p>
    </div>
  )
}

// Main Page Component
export default function Home() {
  const [currentStep, setCurrentStep] = useState(1)
  const [files, setFiles] = useState<File[]>([])
  const [extractedContent, setExtractedContent] = useState('')
  const [status, setStatus] = useState<ProcessingStatus>({
    step: 'intake',
    message: 'Ready to process',
    progress: 0
  })
  const [deckData, setDeckData] = useState<DeckData | null>(null)
  const [deckId, setDeckId] = useState<string>('')
  
  const handleFilesAdded = (newFiles: File[], content: string) => {
    setFiles(newFiles)
    setExtractedContent(content)
  }
  
  const handleGenerate = async (formData: {
    company_name: string
    founder_name: string
    raw_content: string
    target_audience: string
    funding_amount: string
    deck_purpose: string
  }) => {
    // Combine extracted content with form data
    const fullContent = extractedContent 
      ? `${extractedContent}\n\n${formData.raw_content}`
      : formData.raw_content
    
    setCurrentStep(2)
    setStatus({ step: 'verification', message: 'Analyzing and verifying data...', progress: 30 })
    
    try {
      const result = await generateDeck({
        ...formData,
        raw_content: fullContent,
      })
      
      setDeckData(result.deck_data)
      setDeckId(result.deck_id)
      setStatus({ step: 'blueprint', message: 'Building slide structure...', progress: 60 })
      
      setTimeout(() => {
        setStatus({ step: 'export', message: 'Generating PowerPoint...', progress: 80 })
        
        setTimeout(() => {
          setStatus({ step: 'complete', message: 'Deck ready!', progress: 100 })
          setCurrentStep(4)
        }, 1000)
      }, 1000)
      
    } catch (error) {
      console.error('Error generating deck:', error)
      setStatus({ step: 'error', message: 'Failed to generate deck', progress: 0 })
    }
  }
  
  const handleDownload = async () => {
    try {
      const blob = await downloadDeck(deckId)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${deckData?.company_name || 'pitch'}_deck.pptx`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Error downloading deck:', error)
    }
  }
  
  const handleReset = () => {
    setCurrentStep(1)
    setFiles([])
    setExtractedContent('')
    setDeckData(null)
    setDeckId('')
    setStatus({ step: 'intake', message: 'Ready to process', progress: 0 })
  }
  
  return (
    <main className="min-h-screen p-6 md:p-12">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-display gradient-text mb-2">
            PitchPilot AI
          </h1>
          <p className="text-on-surface-variant">
            Strategic Pitch Deck Architect
          </p>
        </motion.div>
        
        {/* Step Indicator */}
        <StepIndicator currentStep={currentStep} />
        
        {/* Main Content */}
        <div className="glass rounded-xl p-8">
          <AnimatePresence mode="wait">
            {currentStep === 1 && (
              <motion.div
                key="step1"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-6"
              >
                <div className="text-center mb-8">
                  <h2 className="text-h2 mb-2">Step 1: File Intake</h2>
                  <p className="text-on-surface-variant">
                    Upload your pitch materials or enter details manually
                  </p>
                </div>
                
                <FileUploadZone onFilesAdded={handleFilesAdded} />
                
                <div className="relative py-4">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-outline-variant" />
                  </div>
                  <div className="relative flex justify-center text-sm">
                    <span className="px-4 bg-surface-container text-on-surface-variant">
                      OR
                    </span>
                  </div>
                </div>
                
                <CompanyForm onSubmit={handleGenerate} />
              </motion.div>
            )}
            
            {currentStep === 2 && (
              <motion.div
                key="step2"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
              >
                <div className="text-center mb-8">
                  <h2 className="text-h2 mb-2">Step 2: AI Verification</h2>
                  <p className="text-on-surface-variant">
                    Analyzing your inputs and verifying market data
                  </p>
                </div>
                
                <ThinkingPulse status={status} />
              </motion.div>
            )}
            
            {currentStep === 3 && (
              <motion.div
                key="step3"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
              >
                <div className="text-center mb-8">
                  <h2 className="text-h2 mb-2">Step 3: Deck Blueprint</h2>
                  <p className="text-on-surface-variant">
                    Your 10-slide Farmeal-Standard deck
                  </p>
                </div>
                
                {deckData && <DeckPreview deckData={deckData} />}
                
                <div className="mt-8 flex justify-center gap-4">
                  <button onClick={handleReset} className="btn-secondary">
                    Start Over
                  </button>
                  <button 
                    onClick={() => setCurrentStep(4)}
                    className="btn-primary"
                  >
                    Continue to Export
                  </button>
                </div>
              </motion.div>
            )}
            
            {currentStep === 4 && (
              <motion.div
                key="step4"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
              >
                <ExportSection deckId={deckId} onDownload={handleDownload} />
                
                <div className="mt-8 flex justify-center">
                  <button onClick={handleReset} className="btn-secondary">
                    Create Another Deck
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
        
        {/* Footer */}
        <p className="text-center text-on-surface-variant text-sm mt-8">
          Powered by Gemini 1.5 Pro • Farmeal-Standard 10-Slide Methodology
        </p>
      </div>
    </main>
  )
}