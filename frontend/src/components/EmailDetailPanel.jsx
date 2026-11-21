import { CategoryBadge, PriorityBadge } from './Badge'
import ClassificationChip from './ClassificationChip'
import { CATEGORY_CHOICES, PRIORITY_CHOICES } from '../constants/classification'
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

export default function EmailDetailPanel({
  email,
  loading,
  error,
  onToggleRead,
  onUpdateClassification,
  classificationSaving,
  classificationError,
}) {
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
        <div className={styles.insightsBody}>
          {email.analysis?.ai_category || email.analysis?.ai_priority ? (
            <div className={styles.aiSuggestionRow}>
              <span className={styles.aiSuggestionLabel}>AI suggested</span>
              <CategoryBadge category={email.analysis.ai_category} />
              <PriorityBadge priority={email.analysis.ai_priority} />
            </div>
          ) : (
            <p className={styles.summaryPlaceholder}>
              Not analyzed yet — summaries and suggestions arrive in a later phase. You can still classify it yourself
              below.
            </p>
          )}

          <div className={styles.classificationRow}>
            <div className={styles.classificationItem}>
              <span className={styles.classificationLabel}>Category</span>
              <ClassificationChip
                value={email.analysis?.category ?? null}
                placeholder="Set category"
                options={CATEGORY_CHOICES}
                variantFor={(categoryValue) => categoryValue}
                disabled={classificationSaving}
                onChange={(categoryValue) => onUpdateClassification({ category: categoryValue })}
              />
            </div>
            <div className={styles.classificationItem}>
              <span className={styles.classificationLabel}>Priority</span>
              <ClassificationChip
                value={email.analysis?.priority ?? null}
                placeholder="Set priority"
                options={PRIORITY_CHOICES}
                variantFor={(priorityValue) => `priority_${priorityValue}`}
                disabled={classificationSaving}
                onChange={(priorityValue) => onUpdateClassification({ priority: priorityValue })}
              />
            </div>
            {classificationSaving && <span className={styles.classificationSaving}>Saving…</span>}
          </div>
          {classificationError && <p className={styles.classificationError}>{classificationError}</p>}

          {email.analysis?.summary && <p className={styles.summary}>{email.analysis.summary}</p>}
        </div>
      </section>

      <section className={styles.body}>
        {email.body_text.split('\n').map((line, index) => (
          <p key={index}>{line.length > 0 ? line : ' '}</p>
        ))}
      </section>
    </div>
  )
}
