import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Layout from './layouts/Layout'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import CreateRequest from './pages/CreateRequest'
import MyRequests from './pages/MyRequests'
import RequestDetail from './pages/RequestDetail'
import Notifications from './pages/Notifications'
import Profile from './pages/Profile'
import AdminUsers from './pages/AdminUsers'
import AdminWorkflows from './pages/AdminWorkflows'
import AdminApprovals from './pages/AdminApprovals'
import AdminAudit from './pages/AdminAudit'
import AdminKnowledge from './pages/AdminKnowledge'
import AdminAnalytics from './pages/AdminAnalytics'
import AdminDepartments from './pages/AdminDepartments'

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <div className="loading-spinner" />
  if (!user) return <Navigate to="/login" />
  return children
}

function AdminRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <div className="loading-spinner" />
  if (!user) return <Navigate to="/login" />
  if (!['ADMIN', 'DEPARTMENT_MANAGER'].includes(user.role?.name)) return <Navigate to="/dashboard" />
  return children
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
        <Route index element={<Navigate to="/dashboard" />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="create-request" element={<CreateRequest />} />
        <Route path="my-requests" element={<MyRequests />} />
        <Route path="requests/:id" element={<RequestDetail />} />
        <Route path="notifications" element={<Notifications />} />
        <Route path="profile" element={<Profile />} />
        <Route path="admin/users" element={<AdminRoute><AdminUsers /></AdminRoute>} />
        <Route path="admin/workflows" element={<AdminRoute><AdminWorkflows /></AdminRoute>} />
        <Route path="admin/approvals" element={<AdminRoute><AdminApprovals /></AdminRoute>} />
        <Route path="admin/audit" element={<AdminRoute><AdminAudit /></AdminRoute>} />
        <Route path="admin/knowledge" element={<AdminRoute><AdminKnowledge /></AdminRoute>} />
        <Route path="admin/analytics" element={<AdminRoute><AdminAnalytics /></AdminRoute>} />
        <Route path="admin/departments" element={<AdminRoute><AdminDepartments /></AdminRoute>} />
      </Route>
    </Routes>
  )
}
