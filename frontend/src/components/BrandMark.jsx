// Standalone brand mark for collapsed/icon-only contexts. A bold geometric "C"
// (a circle with a calculated gap, not a clipped letterform) inside a rounded
// accent badge — reads clearly at 18-22px, unlike the full "Correspond" wordmark.
const RADIUS = 6.5
const CIRCUMFERENCE = 2 * Math.PI * RADIUS
const GAP_DEGREES = 64
const GAP_LENGTH = CIRCUMFERENCE * (GAP_DEGREES / 360)
const DASH_LENGTH = CIRCUMFERENCE - GAP_LENGTH

export default function BrandMark({ size = 22 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" role="img" aria-label="Correspond">
      <rect x="0.5" y="0.5" width="23" height="23" rx="6" fill="var(--color-accent)" />
      <circle
        cx="12"
        cy="12"
        r={RADIUS}
        fill="none"
        stroke="white"
        strokeWidth="2.4"
        strokeLinecap="round"
        strokeDasharray={`${DASH_LENGTH} ${GAP_LENGTH}`}
        strokeDashoffset={-GAP_LENGTH / 2}
      />
    </svg>
  )
}
