import styles from './ComingSoon.module.css'

export default function ComingSoon({ title, body }) {
  return (
    <div className={styles.page}>
      <div className={styles.inner}>
        <h2 className={styles.title}>{title}</h2>
        <p className={styles.body}>{body}</p>
      </div>
    </div>
  )
}
