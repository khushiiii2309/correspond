import { CategoryBadge, PriorityBadge, UnprocessedBadge } from './Badge'
import styles from './EmailDetailPanel.module.css'

function formatFullTimestamp(isoString) {
  return new Date(isoString).toLocaleString(undefined, {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  })
}

export default function EmailDetailPanel({ email, loading, error, onToggleRead }) {
  if (loading) {
    return <div className={styles.state}>Loading email…</div>
  }

  if (error) {
    return <div className={`${styles.state} ${styles.stateError}`}>{error}</div>
  }

  if (!email) {
    return (
      <div className={styles.empty}>
        <p>Select an email to read it here.</p>
      </div>
    )
  }

  return (
    <div className={styles.panel}>
      <header className={styles.header}>
        <h2 className={styles.subject}>{email.subject}</h2>
        <div className={styles.metaRow}>
          <div className={styles.metaText}>
            <div>
              <strong>{email.sender}</strong>
            </div>
            <div className={styles.toLine}>to {email.recipient}</div>
          </div>
          <div className={styles.metaRight}>
            <span className={styles.timestamp}>{formatFullTimestamp(email.received_at)}</span>
            <button type="button" className={styles.readToggle} onClick={() => onToggleRead(!email.is_read)}>
              Mark as {email.is_read ? 'unread' : 'read'}
            </button>
          </div>
        </div>
      </header>

      <section className={styles.insights}>
        <div className={styles.insightsHeader}>
          <h3>AI Insights</h3>
          <span className={styles.insightsHint}>AI-generated — verify before acting</span>
        </div>
        {email.analysis ? (
          <div className={styles.insightsBody}>
            <div className={styles.badgeRow}>
              <CategoryBadge category={email.analysis.category} />
              <PriorityBadge priority={email.analysis.priority} />
            </div>
            <p className={styles.summary}>{email.analysis.summary}</p>
          </div>
        ) : (
          <div className={styles.insightsBody}>
            <UnprocessedBadge />
            <p className={styles.summaryPlaceholder}>
              This email hasn't been analyzed yet. Summaries, priority and task suggestions arrive in a later phase.
            </p>
          </div>
        )}
      </section>

      <section className={styles.body}>
        {email.body_text.split('\n').map((line, index) => (
          <p key={index}>{line.length > 0 ? line : ' '}</p>
        ))}
      </section>
    </div>
  )
}
