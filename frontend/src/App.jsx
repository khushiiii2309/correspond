import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import ComingSoon from './pages/ComingSoon'
import Inbox from './pages/Inbox'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Inbox />} />
          <Route
            path="tasks"
            element={
              <ComingSoon
                title="Tasks"
                body="Task extraction and the approval workflow arrive in Phase 3, once email intelligence is in place."
              />
            }
          />
          <Route
            path="activity"
            element={
              <ComingSoon
                title="Activity"
                body="A history of AI suggestions and your decisions will appear here starting in Phase 3."
              />
            }
          />
          <Route
            path="settings"
            element={
              <ComingSoon
                title="Settings"
                body="Gmail connection and account settings arrive in Phase 4."
              />
            }
          />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
