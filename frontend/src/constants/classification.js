// Mirrors the backend's EmailCategory / PriorityLevel enums (app/models/enums.py).
export const CATEGORY_CHOICES = [
  { value: 'important', label: 'Important' },
  { value: 'requires_action', label: 'Requires Action' },
  { value: 'informational', label: 'Informational' },
  { value: 'promotional', label: 'Promotional' },
  { value: 'potentially_suspicious', label: 'Potentially Suspicious' },
]

export const PRIORITY_CHOICES = [
  { value: 'high', label: 'High' },
  { value: 'medium', label: 'Medium' },
  { value: 'low', label: 'Low' },
]
