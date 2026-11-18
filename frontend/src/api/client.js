import axios from 'axios'

const client = axios.create({
  baseURL: '/api',
})

export async function fetchEmails(params = {}) {
  const { data } = await client.get('/emails', { params })
  return data
}

export async function fetchEmailDetail(emailId) {
  const { data } = await client.get(`/emails/${emailId}`)
  return data
}

export async function seedDemoEmails() {
  const { data } = await client.post('/emails/demo/seed')
  return data
}

export async function updateReadStatus(emailId, isRead) {
  const { data } = await client.patch(`/emails/${emailId}/read-status`, { is_read: isRead })
  return data
}

export default client
