import { useCallback, useEffect, useState } from 'react'
import { fetchEmailDetail, fetchEmails, seedDemoEmails, updateClassification, updateReadStatus } from '../api/client'
import { CATEGORY_CHOICES, PRIORITY_CHOICES } from '../constants/classification'
import EmailDetailPanel from '../components/EmailDetailPanel'
import EmailList from '../components/EmailList'
import styles from './Inbox.module.css'

const CATEGORY_OPTIONS = [{ value: '', label: 'All categories' }, ...CATEGORY_CHOICES]
const PRIORITY_OPTIONS = [{ value: '', label: 'All priorities' }, ...PRIORITY_CHOICES]

export default function Inbox() {
  const [emails, setEmails] = useState([])
  const [listLoading, setListLoading] = useState(true)
  const [listError, setListError] = useState(null)
  const [seeding, setSeeding] = useState(false)
  const [seedError, setSeedError] = useState(null)
  const [hasSampleData, setHasSampleData] = useState(false)

  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')
  const [priority, setPriority] = useState('')
  const [unreadOnly, setUnreadOnly] = useState(false)
  const [sort, setSort] = useState('date')

  const [selectedId, setSelectedId] = useState(null)
  const [selectedEmail, setSelectedEmail] = useState(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const [detailError, setDetailError] = useState(null)
  const [classificationSaving, setClassificationSaving] = useState(false)
  const [classificationError, setClassificationError] = useState(null)

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

  // Checked once, unfiltered, so the seed button's state doesn't flicker back
  // to "Load sample emails" just because the current filters hide every
  // sample row (e.g. an active category filter with no matches).
  useEffect(() => {
    let isMounted = true
    fetchEmails({})
      .then((data) => {
        if (isMounted && data.some((email) => email.source === 'sample')) {
          setHasSampleData(true)
        }
      })
      .catch(() => {})
    return () => {
      isMounted = false
    }
  }, [])

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

  const handleUpdateClassification = useCallback(
    async (changes) => {
      if (!selectedId) return
      setClassificationSaving(true)
      setClassificationError(null)
      try {
        const updated = await updateClassification(selectedId, changes)
        setSelectedEmail(updated)
        setEmails((prev) =>
          prev.map((item) =>
            item.id === selectedId
              ? { ...item, category: updated.analysis?.category ?? null, priority: updated.analysis?.priority ?? null }
              : item,
          ),
        )
      } catch {
        setClassificationError('Could not save this change. Try again.')
      } finally {
        setClassificationSaving(false)
      }
    },
    [selectedId],
  )

  const handleSeed = useCallback(async () => {
    setSeeding(true)
    setSeedError(null)
    try {
      await seedDemoEmails()
      await loadEmails()
      setHasSampleData(true)
    } catch {
      setSeedError('Could not load sample emails. Is the API running?')
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
        {hasSampleData ? (
          <div className={styles.seedStatus}>
            <span className={styles.seedConfirmation}>✓ Sample data loaded</span>
            <button
              type="button"
              className={styles.seedReload}
              onClick={handleSeed}
              disabled={seeding}
              title="Re-run sample data seeding. Safe to repeat — existing sample emails are left as-is."
            >
              {seeding ? 'Reloading…' : 'Reload sample data'}
            </button>
          </div>
        ) : (
          <button type="button" className={styles.seedButton} onClick={handleSeed} disabled={seeding}>
            {seeding ? 'Loading…' : 'Load sample emails'}
          </button>
        )}
        {seedError && <span className={styles.seedError}>{seedError}</span>}
      </div>

      <div className={styles.body}>
        <div className={styles.listPane}>
          <div className={styles.listPaneHeader}>
            Inbox <span className={styles.count}>{unreadCount} unread</span>
          </div>
          <EmailList emails={emails} selectedId={selectedId} onSelect={handleSelect} loading={listLoading} error={listError} />
        </div>
        <div className={styles.detailPane}>
          <EmailDetailPanel
            email={selectedEmail}
            loading={detailLoading}
            error={detailError}
            onToggleRead={handleToggleRead}
            onUpdateClassification={handleUpdateClassification}
            classificationSaving={classificationSaving}
            classificationError={classificationError}
          />
        </div>
      </div>
    </div>
  )
}
