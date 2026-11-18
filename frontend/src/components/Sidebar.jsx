import { NavLink } from 'react-router-dom'
import styles from './Sidebar.module.css'

const NAV_ITEMS = [
  { to: '/', label: 'Inbox' },
  { to: '/tasks', label: 'Tasks' },
  { to: '/activity', label: 'Activity' },
  { to: '/settings', label: 'Settings' },
]

export default function Sidebar() {
  return (
    <aside className={styles.sidebar}>
      <div className={styles.brand}>Correspond</div>
      <nav className={styles.nav}>
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === '/'}
            className={({ isActive }) => `${styles.navItem} ${isActive ? styles.navItemActive : ''}`}
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
