'use client'

import { useState, useEffect, useRef } from 'react'
import { apiClient } from '@/lib/api'
import { ChatMessage, Source } from '@/types'
import { Send, Lightbulb, FileText, Share2, Download } from 'lucide-react'
import toast from 'react-hot-toast'

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [conversationId, setConversationId] = useState<string | undefined>()
  const [allSources, setAllSources] = useState<Source[]>([])
  const [suggestedQuestions, setSuggestedQuestions] = useState<string[]>([
    'What AI features have been added to competitor products?',
    'How are competitors pricing their services?',
    'What are the latest market trends?',
    'Which competitors are gaining market share?'
  ])
  const [showFilters, setShowFilters] = useState(false)
  const [selectedFilter, setSelectedFilter] = useState<string>('all')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const filterOptions = [
    { value: 'all', label: 'All Topics', icon: '🔍' },
    { value: 'ai_features', label: 'AI Features', icon: '🤖' },
    { value: 'pricing', label: 'Pricing', icon: '💰' },
    { value: 'content', label: 'Content Strategy', icon: '📝' },
    { value: 'trends', label: 'Market Trends', icon: '📈' },
    { value: 'competitors', label: 'Competitors', icon: '🏢' }
  ]

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async (messageText?: string) => {
    const textToSend = messageText || input
    if (!textToSend.trim() || loading) return

    const userMessage: ChatMessage = {
      role: 'user',
      content: textToSend,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await apiClient.sendChatMessage(textToSend, conversationId)

      setConversationId(response.conversation_id)

      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.message,
        timestamp: new Date().toISOString(),
        sources: response.sources || [],
        suggested_actions: response.suggested_actions || []
      }

      setMessages(prev => [...prev, assistantMessage])

      // Add sources to the global sources list
      if (response.sources && response.sources.length > 0) {
        setAllSources(prev => {
          const newSources = response.sources.filter(
            (newSource: Source) => !prev.some(s => s.title === newSource.title)
          )
          return [...prev, ...newSources]
        })
      }

      // Update suggested questions if available
      if (response.suggested_actions && response.suggested_actions.length > 0) {
        setSuggestedQuestions(response.suggested_actions)
      }
    } catch (error) {
      console.error('Error sending message:', error)
      toast.error('Failed to send message')
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const handleExport = () => {
    toast.success('Export feature coming soon!')
  }

  const handleShare = () => {
    toast.success('Share feature coming soon!')
  }

  const formatContent = (content: string) => {
    // Split content into lines and format
    const lines = content.split('\n')
    return lines.map((line, index) => {
      // Check if line is a numbered list item
      if (line.match(/^\d+\.\s/)) {
        return (
          <div key={index} className="mb-2">
            <p className="font-medium text-gray-900">{line}</p>
          </div>
        )
      }
      // Check if line contains a URL
      else if (line.includes('http')) {
        const urlMatch = line.match(/(https?:\/\/[^\s]+)/)
        if (urlMatch) {
          const url = urlMatch[1]
          const beforeUrl = line.substring(0, line.indexOf(url))
          const afterUrl = line.substring(line.indexOf(url) + url.length)
          return (
            <p key={index} className="text-gray-700 mb-1">
              {beforeUrl}
              <a href={url} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline hover:text-blue-800">
                {url}
              </a>
              {afterUrl}
            </p>
          )
        }
      }
      // Regular text
      return line.trim() ? (
        <p key={index} className="text-gray-700 mb-1">{line}</p>
      ) : (
        <br key={index} />
      )
    })
  }

  return (
    <div className="flex flex-col h-full bg-gradient-to-br from-blue-50 to-indigo-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-900 to-indigo-900 px-8 py-6 shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center">
              <FileText className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-white">Research Assistant</h1>
          </div>
          <div className="flex gap-3">
            <button
              onClick={handleExport}
              className="px-4 py-2 border-2 border-blue-400 text-white rounded-lg hover:bg-blue-800 transition-colors flex items-center gap-2"
            >
              <Download className="w-4 h-4" />
              Export
            </button>
            <button
              onClick={handleShare}
              className="px-4 py-2 border-2 border-blue-400 text-white rounded-lg hover:bg-blue-800 transition-colors flex items-center gap-2"
            >
              <Share2 className="w-4 h-4" />
              Share
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto px-8 py-6">
        <div className="max-w-5xl mx-auto">
          {/* Filters */}
          <div className="mb-6">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                </svg>
                <h3 className="font-semibold text-gray-900">Filter Topics</h3>
              </div>
              <button
                onClick={() => setShowFilters(!showFilters)}
                className="text-sm text-blue-600 hover:text-blue-700 font-medium"
              >
                {showFilters ? 'Hide' : 'Show'} Filters
              </button>
            </div>

            {showFilters && (
              <div className="flex flex-wrap gap-2 p-4 bg-white rounded-lg border border-gray-200">
                {filterOptions.map((option) => (
                  <button
                    key={option.value}
                    onClick={() => setSelectedFilter(option.value)}
                    className={`px-4 py-2 rounded-full text-sm font-medium transition-colors flex items-center gap-2 ${
                      selectedFilter === option.value
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    <span>{option.icon}</span>
                    {option.label}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Suggested Questions */}
          {messages.length === 0 && (
            <div className="mb-6">
              <div className="flex items-center gap-2 mb-4">
                <Lightbulb className="w-5 h-5 text-blue-600" />
                <h2 className="text-lg font-semibold text-gray-900">Suggested Questions</h2>
              </div>
              <div className="flex flex-wrap gap-3">
                {suggestedQuestions.map((question, i) => (
                  <button
                    key={i}
                    onClick={() => sendMessage(question)}
                    className="px-4 py-2 bg-blue-100 text-blue-800 rounded-full hover:bg-blue-200 transition-colors text-sm font-medium"
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Messages */}
          {messages.length > 0 && (
            <div className="space-y-6">
              {messages.map((message, index) => (
                <div key={index}>
                  {message.role === 'user' ? (
                    <div className="flex justify-end mb-4">
                      <div className="bg-gray-100 rounded-lg px-6 py-3 max-w-2xl">
                        <p className="text-gray-900 font-medium">You: {message.content}</p>
                      </div>
                    </div>
                  ) : (
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-4">
                      <div className="flex items-start gap-3 mb-4">
                        <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
                          <FileText className="w-5 h-5 text-white" />
                        </div>
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-900 mb-2">Assistant:</h3>
                          <div className="prose max-w-none">
                            {formatContent(message.content)}
                          </div>

                          {/* Suggested Actions */}
                          {message.suggested_actions && message.suggested_actions.length > 0 && (
                            <div className="mt-4 pt-4 border-t border-gray-200">
                              <p className="text-sm font-semibold text-gray-700 mb-2">Suggested next steps:</p>
                              <div className="flex flex-wrap gap-2">
                                {message.suggested_actions.map((action, i) => (
                                  <button
                                    key={i}
                                    onClick={() => sendMessage(action)}
                                    className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full hover:bg-blue-100 transition-colors text-sm"
                                  >
                                    {action}
                                  </button>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
              {loading && (
                <div className="flex justify-start">
                  <div className="bg-white rounded-lg px-6 py-4 shadow-sm border border-gray-200">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                      <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                      <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}

          {/* Sources Section */}
          {allSources.length > 0 && (
            <div className="mt-8 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center gap-2 mb-4">
                <FileText className="w-5 h-5 text-gray-600" />
                <h3 className="font-semibold text-gray-900">Sources ({allSources.length})</h3>
              </div>
              <div className="space-y-3">
                {allSources.map((source, index) => (
                  <div key={index} className="border-l-4 border-blue-500 pl-4 py-2">
                    <a
                      href={source.url || '#'}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800 font-medium hover:underline"
                    >
                      {source.title}
                    </a>
                    {source.excerpt && (
                      <p className="text-sm text-gray-600 mt-1">{source.excerpt}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 px-8 py-6 shadow-lg">
        <div className="max-w-5xl mx-auto">
          <div className="flex gap-4 items-center">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your question..."
              className="flex-1 px-6 py-4 bg-gray-50 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 placeholder-gray-500"
            />
            <button
              onClick={() => sendMessage()}
              disabled={!input.trim() || loading}
              className="w-14 h-14 bg-blue-600 text-white rounded-full hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center shadow-lg"
            >
              <Send className="w-6 h-6" />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
