import { useEffect, useState } from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import { MenuIcon } from './icons'
import styles from './Layout.module.css'

const COLLAPSE_STORAGE_KEY = 'correspond:sidebar-collapsed'

function readStoredCollapsed() {
  try {
    return localStorage.getItem(COLLAPSE_STORAGE_KEY) === 'true'
  } catch {
    return false
  }
}

export default function Layout() {
  const [collapsed, setCollapsed] = useState(readStoredCollapsed)
  const [mobileOpen, setMobileOpen] = useState(false)

  useEffect(() => {
    try {
      localStorage.setItem(COLLAPSE_STORAGE_KEY, String(collapsed))
    } catch {
      // Per-viewer convenience only — fine to lose this if storage is unavailable.
    }
  }, [collapsed])

  return (
    <div className={styles.shell}>
      <button
        type="button"
        className={styles.mobileTrigger}
        onClick={() => setMobileOpen(true)}
        aria-label="Open navigation"
      >
        <MenuIcon />
      </button>

      {mobileOpen && <div className={styles.backdrop} onClick={() => setMobileOpen(false)} />}

      <Sidebar
        collapsed={collapsed}
        onToggleCollapsed={() => setCollapsed((prev) => !prev)}
        mobileOpen={mobileOpen}
        onCloseMobile={() => setMobileOpen(false)}
      />

      <main className={styles.main}>
        <Outlet />
      </main>
    </div>
  )
}
