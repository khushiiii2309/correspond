import { useCallback, useEffect, useState } from 'react'
import { fetchEmailDetail, fetchEmails, seedDemoEmails, updateReadStatus } from '../api/client'
import EmailDetailPanel from '../components/EmailDetailPanel'
import EmailList from '../components/EmailList'
import styles from './Inbox.module.css'

const CATEGORY_OPTIONS = [
  { value: '', label: 'All categories' },
  { value: 'important', label: 'Important' },
  { value: 'requires_action', label: 'Requires Action' },
  { value: 'informational', label: 'Informational' },
  { value: 'promotional', label: 'Promotional' },
  { value: 'potentially_suspicious', label: 'Potentially Suspicious' },
]

const PRIORITY_OPTIONS = [
  { value: '', label: 'All priorities' },
  { value: 'high', label: 'High' },
  { value: 'medium', label: 'Medium' },
  { value: 'low', label: 'Low' },
]

export default function Inbox() {
  const [emails, setEmails] = useState([])
  const [listLoading, setListLoading] = useState(true)
  const [listError, setListError] = useState(null)
  const [seeding, setSeeding] = useState(false)

  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')
  const [priority, setPriority] = useState('')
  const [unreadOnly, setUnreadOnly] = useState(false)
  const [sort, setSort] = useState('date')

  const [selectedId, setSelectedId] = useState(null)
  const [selectedEmail, setSelectedEmail] = useState(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const [detailError, setDetailError] = useState(null)

  const loadEmails = useCallback(async () => {
    setListLoading(true)
    setListError(null)
    try {
      const params = { sort }
      if (search) params.search = search
      if (category) params.category = category
      if (priority) params.priority = priority
      if (unreadOnly) params.unread_only = true

      const data = await fetchEmails(params)
      setEmails(data)
    } catch {
      setListError('Could not load emails. Is the API running?')
    } finally {
      setListLoading(false)
    }
  }, [search, category, priority, unreadOnly, sort])

  useEffect(() => {
    loadEmails()
  }, [loadEmails])

  const loadDetail = useCallback(async (emailId) => {
    setDetailLoading(true)
    setDetailError(null)
    try {
      const data = await fetchEmailDetail(emailId)
      setSelectedEmail(data)
    } catch {
      setDetailError('Could not load this email.')
    } finally {
      setDetailLoading(false)
    }
  }, [])

  const handleSelect = useCallback(
    async (emailId) => {
      setSelectedId(emailId)
      await loadDetail(emailId)

      const email = emails.find((item) => item.id === emailId)
      if (email && !email.is_read) {
        await updateReadStatus(emailId, true)
        setEmails((prev) => prev.map((item) => (item.id === emailId ? { ...item, is_read: true } : item)))
      }
    },
    [emails, loadDetail],
  )

  const handleToggleRead = useCallback(
    async (isRead) => {
      if (!selectedId) return
      const updated = await updateReadStatus(selectedId, isRead)
      setSelectedEmail(updated)
      setEmails((prev) => prev.map((item) => (item.id === selectedId ? { ...item, is_read: isRead } : item)))
    },
    [selectedId],
  )

  const handleSeed = useCallback(async () => {
    setSeeding(true)
    try {
      await seedDemoEmails()
      await loadEmails()
    } catch {
      setListError('Could not load sample emails. Is the API running?')
    } finally {
      setSeeding(false)
    }
  }, [loadEmails])

  const unreadCount = emails.filter((email) => !email.is_read).length

  return (
    <div className={styles.page}>
      <div className={styles.toolbar}>
        <input
          className={styles.search}
          type="text"
          placeholder="Search emails…"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
        <select value={category} onChange={(event) => setCategory(event.target.value)}>
          {CATEGORY_OPTIONS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        <select value={priority} onChange={(event) => setPriority(event.target.value)}>
          {PRIORITY_OPTIONS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        <label className={styles.checkboxLabel}>
          <input type="checkbox" checked={unreadOnly} onChange={(event) => setUnreadOnly(event.target.checked)} />
          Unread only
        </label>
        <select value={sort} onChange={(event) => setSort(event.target.value)}>
          <option value="date">Sort by date</option>
          <option value="priority">Sort by priority</option>
        </select>
        <button type="button" className={styles.seedButton} onClick={handleSeed} disabled={seeding}>
          {seeding ? 'Loading…' : 'Load sample emails'}
        </button>
      </div>

      <div className={styles.body}>
        <div className={styles.listPane}>
          <div className={styles.listPaneHeader}>
            Inbox <span className={styles.count}>{unreadCount} unread</span>
          </div>
          <EmailList emails={emails} selectedId={selectedId} onSelect={handleSelect} loading={listLoading} error={listError} />
        </div>
        <div className={styles.detailPane}>
          <EmailDetailPanel email={selectedEmail} loading={detailLoading} error={detailError} onToggleRead={handleToggleRead} />
        </div>
      </div>
    </div>
  )
}
