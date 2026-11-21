import styles from './Badge.module.css'

const CATEGORY_LABELS = {
  important: 'Important',
  requires_action: 'Requires Action',
  informational: 'Informational',
  promotional: 'Promotional',
  potentially_suspicious: 'Potentially Suspicious',
}

const PRIORITY_LABELS = {
  high: 'High',
  medium: 'Medium',
  low: 'Low',
}

export function CategoryBadge({ category }) {
  if (!category) return null
  return <span className={`${styles.badge} ${styles[category]}`}>{CATEGORY_LABELS[category] ?? category}</span>
}

export function PriorityBadge({ priority }) {
  if (!priority) return null
  return (
    <span className={`${styles.badge} ${styles[`priority_${priority}`]}`}>{PRIORITY_LABELS[priority] ?? priority}</span>
  )
}
