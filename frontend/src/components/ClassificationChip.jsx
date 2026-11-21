import { useEffect, useRef, useState } from 'react'
import { ChevronDownIcon } from './icons'
import styles from './ClassificationChip.module.css'

export default function ClassificationChip({ value, placeholder, options, variantFor, onChange, disabled }) {
  const [open, setOpen] = useState(false)
  const containerRef = useRef(null)

  useEffect(() => {
    if (!open) return

    function handlePointerDown(event) {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setOpen(false)
      }
    }
    function handleKeyDown(event) {
      if (event.key === 'Escape') setOpen(false)
    }

    document.addEventListener('mousedown', handlePointerDown)
    document.addEventListener('keydown', handleKeyDown)
    return () => {
      document.removeEventListener('mousedown', handlePointerDown)
      document.removeEventListener('keydown', handleKeyDown)
    }
  }, [open])

  const selected = options.find((option) => option.value === value)

  return (
    <div className={styles.container} ref={containerRef}>
      <button
        type="button"
        className={`${styles.chip} ${selected ? styles[variantFor(selected.value)] : styles.chipEmpty}`}
        onClick={() => setOpen((prev) => !prev)}
        disabled={disabled}
        aria-haspopup="listbox"
        aria-expanded={open}
      >
        {selected ? (
          <>
            <span className={`${styles.dot} ${styles[variantFor(selected.value)]}`} />
            {selected.label}
          </>
        ) : (
          placeholder
        )}
        <ChevronDownIcon />
      </button>

      {open && (
        <ul className={styles.menu} role="listbox">
          {options.map((option) => (
            <li key={option.value} role="option" aria-selected={option.value === value}>
              <button
                type="button"
                className={`${styles.menuItem} ${option.value === value ? styles.menuItemActive : ''}`}
                onClick={() => {
                  setOpen(false)
                  if (option.value !== value) onChange(option.value)
                }}
              >
                <span className={`${styles.dot} ${styles[variantFor(option.value)]}`} />
                {option.label}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
