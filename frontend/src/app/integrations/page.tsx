'use client'

import { useState, useEffect } from 'react'
import { apiClient } from '@/lib/api'
import { IntegrationSettings } from '@/types'
import { Slack, Mail, Settings as SettingsIcon, Check, X } from 'lucide-react'
import toast from 'react-hot-toast'

export default function IntegrationsPage() {
  const [settings, setSettings] = useState<IntegrationSettings | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    loadSettings()
  }, [])

  const loadSettings = async () => {
    try {
      setLoading(true)
      const data = await apiClient.getIntegrationSettings()
      setSettings(data)
    } catch (error) {
      console.error('Error loading settings:', error)
      toast.error('Failed to load integration settings')
    } finally {
      setLoading(false)
    }
  }

  const handleSaveSettings = async () => {
    if (!settings) return

    try {
      setSaving(true)
      await apiClient.updateIntegrationSettings(settings)
      toast.success('Settings saved successfully')
    } catch (error) {
      console.error('Error saving settings:', error)
      toast.error('Failed to save settings')
    } finally {
      setSaving(false)
    }
  }

  const handleTestSlack = async () => {
    try {
      toast.loading('Testing Slack integration...')
      const result = await apiClient.testSlackIntegration()
      toast.dismiss()
      toast.success(result.message || 'Slack test successful')
    } catch (error) {
      toast.dismiss()
      console.error('Error testing Slack:', error)
      toast.error('Slack test failed')
    }
  }

  const handleTestEmail = async () => {
    try {
      toast.loading('Testing email integration...')
      const result = await apiClient.testEmailIntegration()
      toast.dismiss()
      toast.success(result.message || 'Email test successful')
    } catch (error) {
      toast.dismiss()
      console.error('Error testing email:', error)
      toast.error('Email test failed')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading settings...</p>
        </div>
      </div>
    )
  }

  if (!settings) {
    return (
      <div className="p-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">Failed to load integration settings</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Integrations</h1>
        <p className="text-gray-600 mt-2">Configure external integrations for notifications and data sync</p>
      </div>

      <div className="space-y-6">
        {/* Slack Integration */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-start justify-between mb-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-purple-100 rounded-lg">
                <Slack className="w-8 h-8 text-purple-600" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-gray-900">Slack Integration</h2>
                <p className="text-gray-600 text-sm">Send notifications to your Slack workspace</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.slack.enabled}
                  onChange={(e) => setSettings({
                    ...settings,
                    slack: { ...settings.slack, enabled: e.target.checked }
                  })}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
              </label>
              <span className={`text-sm font-medium ${settings.slack.enabled ? 'text-green-600' : 'text-gray-500'}`}>
                {settings.slack.enabled ? 'Enabled' : 'Disabled'}
              </span>
            </div>
          </div>

          {settings.slack.enabled && (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Channel ID</label>
                <input
                  type="text"
                  value={settings.slack.channel_id || ''}
                  onChange={(e) => setSettings({
                    ...settings,
                    slack: { ...settings.slack, channel_id: e.target.value }
                  })}
                  placeholder="e.g., C01234567"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Webhook URL</label>
                <input
                  type="text"
                  value={settings.slack.webhook_url || ''}
                  onChange={(e) => setSettings({
                    ...settings,
                    slack: { ...settings.slack, webhook_url: e.target.value }
                  })}
                  placeholder="https://hooks.slack.com/services/..."
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Notification Types</label>
                <div className="space-y-2">
                  {['new_competitor', 'trend_alert', 'report_ready', 'analysis_complete'].map((type) => (
                    <label key={type} className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={settings.slack.notification_types.includes(type)}
                        onChange={(e) => {
                          const types = e.target.checked
                            ? [...settings.slack.notification_types, type]
                            : settings.slack.notification_types.filter(t => t !== type)
                          setSettings({
                            ...settings,
                            slack: { ...settings.slack, notification_types: types }
                          })
                        }}
                        className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                      />
                      <span className="text-sm text-gray-700 capitalize">
                        {type.replace(/_/g, ' ')}
                      </span>
                    </label>
                  ))}
                </div>
              </div>

              <button
                onClick={handleTestSlack}
                className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
              >
                Test Connection
              </button>
            </div>
          )}
        </div>

        {/* Email Integration */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-start justify-between mb-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-blue-100 rounded-lg">
                <Mail className="w-8 h-8 text-blue-600" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-gray-900">Email Notifications</h2>
                <p className="text-gray-600 text-sm">Receive updates via email</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.email.enabled}
                  onChange={(e) => setSettings({
                    ...settings,
                    email: { ...settings.email, enabled: e.target.checked }
                  })}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
              </label>
              <span className={`text-sm font-medium ${settings.email.enabled ? 'text-green-600' : 'text-gray-500'}`}>
                {settings.email.enabled ? 'Enabled' : 'Disabled'}
              </span>
            </div>
          </div>

          {settings.email.enabled && (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Recipients</label>
                <div className="space-y-2">
                  {settings.email.recipients.map((email, index) => (
                    <div key={index} className="flex items-center gap-2">
                      <input
                        type="email"
                        value={email}
                        onChange={(e) => {
                          const newRecipients = [...settings.email.recipients]
                          newRecipients[index] = e.target.value
                          setSettings({
                            ...settings,
                            email: { ...settings.email, recipients: newRecipients }
                          })
                        }}
                        className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                      <button
                        onClick={() => {
                          const newRecipients = settings.email.recipients.filter((_, i) => i !== index)
                          setSettings({
                            ...settings,
                            email: { ...settings.email, recipients: newRecipients }
                          })
                        }}
                        className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                      >
                        <X className="w-5 h-5" />
                      </button>
                    </div>
                  ))}
                  <button
                    onClick={() => {
                      setSettings({
                        ...settings,
                        email: { ...settings.email, recipients: [...settings.email.recipients, ''] }
                      })
                    }}
                    className="text-sm text-primary-600 hover:text-primary-700"
                  >
                    + Add recipient
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Frequency</label>
                <select
                  value={settings.email.frequency}
                  onChange={(e) => setSettings({
                    ...settings,
                    email: { ...settings.email, frequency: e.target.value }
                  })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="realtime">Real-time</option>
                  <option value="daily">Daily digest</option>
                  <option value="weekly">Weekly summary</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Notification Types</label>
                <div className="space-y-2">
                  {['new_competitor', 'trend_alert', 'report_ready', 'analysis_complete'].map((type) => (
                    <label key={type} className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={settings.email.notification_types.includes(type)}
                        onChange={(e) => {
                          const types = e.target.checked
                            ? [...settings.email.notification_types, type]
                            : settings.email.notification_types.filter(t => t !== type)
                          setSettings({
                            ...settings,
                            email: { ...settings.email, notification_types: types }
                          })
                        }}
                        className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                      />
                      <span className="text-sm text-gray-700 capitalize">
                        {type.replace(/_/g, ' ')}
                      </span>
                    </label>
                  ))}
                </div>
              </div>

              <button
                onClick={handleTestEmail}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Send Test Email
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Save Button */}
      <div className="mt-8 flex justify-end">
        <button
          onClick={handleSaveSettings}
          disabled={saving}
          className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          {saving ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              Saving...
            </>
          ) : (
            <>
              <Check className="w-5 h-5" />
              Save Settings
            </>
          )}
        </button>
      </div>
    </div>
  )
}
