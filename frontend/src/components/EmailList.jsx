import { CategoryBadge, PriorityBadge } from './Badge'
import styles from './EmailList.module.css'

function formatTimestamp(isoString) {
  const date = new Date(isoString)
  const now = new Date()
  const isToday = date.toDateString() === now.toDateString()
  if (isToday) {
    return date.toLocaleTimeString(undefined, { hour: 'numeric', minute: '2-digit' })
  }
  return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
}

export default function EmailList({ emails, selectedId, onSelect, loading, error }) {
  if (loading) {
    return <div className={styles.state}>Loading emails…</div>
  }

  if (error) {
    return <div className={`${styles.state} ${styles.stateError}`}>{error}</div>
  }

  if (emails.length === 0) {
    return <div className={styles.state}>No emails match the current filters.</div>
  }

  return (
    <ul className={styles.list}>
      {emails.map((email) => (
        <li key={email.id}>
          <button
            type="button"
            className={`${styles.item} ${email.id === selectedId ? styles.itemSelected : ''} ${!email.is_read ? styles.itemUnread : ''}`}
            onClick={() => onSelect(email.id)}
          >
            <div className={styles.itemTopRow}>
              <span className={styles.sender}>{email.sender}</span>
              <span className={styles.timestamp}>{formatTimestamp(email.received_at)}</span>
            </div>
            <div className={styles.subject}>{email.subject}</div>
            <div className={styles.preview}>{email.preview}</div>
            {(email.category || email.priority) && (
              <div className={styles.badgeRow}>
                <CategoryBadge category={email.category} />
                <PriorityBadge priority={email.priority} />
              </div>
            )}
          </button>
        </li>
      ))}
    </ul>
  )
}
