import { NavLink } from 'react-router-dom'
import styles from './Sidebar.module.css'
import BrandMark from './BrandMark'
import { ActivityIcon, InboxIcon, MenuIcon, SettingsIcon, TasksIcon } from './icons'

const NAV_ITEMS = [
  { to: '/', label: 'Inbox', icon: InboxIcon, end: true },
  { to: '/tasks', label: 'Tasks', icon: TasksIcon, end: false },
  { to: '/activity', label: 'Activity', icon: ActivityIcon, end: false },
  { to: '/settings', label: 'Settings', icon: SettingsIcon, end: false },
]

export default function Sidebar({ collapsed, onToggleCollapsed, mobileOpen, onCloseMobile }) {
  return (
    <aside
      className={`${styles.sidebar} ${collapsed ? styles.collapsed : ''} ${mobileOpen ? styles.mobileOpen : ''}`}
    >
      <div className={styles.topRow}>
        <span className={styles.brand}>
          <span className={styles.brandMark}>
            <BrandMark />
          </span>
          <span className={styles.brandWordmark}>Correspond</span>
        </span>
        <button
          type="button"
          className={styles.collapseToggle}
          onClick={onToggleCollapsed}
          aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          <MenuIcon />
        </button>
      </div>
      <nav className={styles.nav}>
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              title={item.label}
              onClick={onCloseMobile}
              className={({ isActive }) => `${styles.navItem} ${isActive ? styles.navItemActive : ''}`}
            >
              <span className={styles.iconSlot}>
                <Icon />
              </span>
              <span className={styles.label}>{item.label}</span>
            </NavLink>
          )
        })}
      </nav>
    </aside>
  )
}
