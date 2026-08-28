import { useState } from 'react'
import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import { useEffect } from 'react'

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [notifications, setNotifications] = useState([])
  const [unreadCount, setUnreadCount] = useState(0)

  useEffect(() => {
    api.get('/notifications?per_page=5').then(res => {
      setNotifications(res.data.data.items || [])
      setUnreadCount(res.data.data.unread_count || 0)
    }).catch(() => {})
  }, [])

  const handleLogout = () => { logout(); navigate('/login') }
  const isAdmin = user?.role?.name === 'ADMIN'
  const isManager = user?.role?.name === 'DEPARTMENT_MANAGER'
  const isStaff = user?.role?.name === 'STAFF'

  const navItems = [
    { label: 'Dashboard', path: '/dashboard', icon: '📊' },
    { label: 'Create Request', path: '/create-request', icon: '➕' },
    { label: 'My Requests', path: '/my-requests', icon: '📋' },
  ]

  const adminItems = [
    { label: 'Users', path: '/admin/users', icon: '👥' },
    { label: 'Departments', path: '/admin/departments', icon: '🏢' },
    { label: 'Workflows', path: '/admin/workflows', icon: '⚙️' },
    { label: 'Approvals', path: '/admin/approvals', icon: '✅' },
    { label: 'Knowledge Base', path: '/admin/knowledge', icon: '📚' },
    { label: 'Audit Logs', path: '/admin/audit', icon: '📝' },
    { label: 'Analytics', path: '/admin/analytics', icon: '📈' },
  ]

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1>Campus<span>OS</span></h1>
        </div>
        <nav className="sidebar-nav">
          <div className="nav-section">
            <div className="nav-section-title">Main</div>
            {navItems.map(item => (
              <NavLink key={item.path} to={item.path}
                className={({isActive}) => `nav-item ${isActive ? 'active' : ''}`}>
                <span>{item.icon}</span> {item.label}
              </NavLink>
            ))}
          </div>
          {(isAdmin || isManager) && (
            <div className="nav-section">
              <div className="nav-section-title">Administration</div>
              {adminItems.map(item => (
                <NavLink key={item.path} to={item.path}
                  className={({isActive}) => `nav-item ${isActive ? 'active' : ''}`}>
                  <span>{item.icon}</span> {item.label}
                </NavLink>
              ))}
            </div>
          )}
          {isStaff && (
            <div className="nav-section">
              <div className="nav-section-title">Staff</div>
              <NavLink to="/my-requests" className={({isActive}) => `nav-item ${isActive ? 'active' : ''}`}>
                <span>📋</span> Assigned Tasks
              </NavLink>
            </div>
          )}
        </nav>
        <div className="sidebar-footer">
          <div className="nav-item" onClick={handleLogout} style={{cursor:'pointer'}}>
            <span>🚪</span> Logout
          </div>
        </div>
      </aside>
      <main className="main-content">
        <header className="topbar">
          <div className="topbar-left">
            <h2 className="topbar-title">CampusOS</h2>
          </div>
          <div className="topbar-right">
            <NavLink to="/notifications" className="topbar-btn">
              🔔
              {unreadCount > 0 && <span className="badge">{unreadCount}</span>}
            </NavLink>
            <NavLink to="/profile" className="topbar-btn" style={{display:'flex',alignItems:'center',gap:8}}>
              <span style={{width:32,height:32,borderRadius:'50%',background:'var(--secondary)',color:'white',display:'flex',alignItems:'center',justifyContent:'center',fontSize:14,fontWeight:600}}>
                {user?.name?.[0] || 'U'}
              </span>
              <span style={{fontSize:14,fontWeight:500}}>{user?.name}</span>
            </NavLink>
          </div>
        </header>
        <div className="page-content">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
