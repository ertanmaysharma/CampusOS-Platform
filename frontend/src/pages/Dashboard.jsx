import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'

export default function Dashboard() {
  const { user } = useAuth()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const role = user?.role?.name
    const endpoint = role === 'ADMIN' ? '/dashboard/admin' :
      role === 'DEPARTMENT_MANAGER' ? '/dashboard/manager' :
      role === 'STAFF' ? '/dashboard/staff' : '/dashboard/student'
    api.get(endpoint).then(res => setData(res.data.data)).catch(() => {}).finally(() => setLoading(false))
  }, [user])

  if (loading) return <div className="loading-spinner" />
  if (!data) return <div className="empty-state"><div className="empty-state-title">Unable to load dashboard</div></div>

  const isAdmin = user?.role?.name === 'ADMIN'

  return (
    <div>
      <div style={{marginBottom:32}}>
        <h1 style={{fontSize:24,fontWeight:700}}>
          Good {new Date().getHours() < 12 ? 'morning' : new Date().getHours() < 17 ? 'afternoon' : 'evening'}, {user?.name?.split(' ')[0]}
        </h1>
        <p style={{color:'var(--text-secondary)',fontSize:14}}>Here's what's happening on campus today</p>
      </div>

      {isAdmin ? (
        <AdminDashboard data={data} />
      ) : (
        <StudentDashboard data={data} user={user} />
      )}
    </div>
  )
}

function StudentDashboard({ data, user }) {
  const stats = data.stats || {}
  return (
    <>
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon blue">📋</div>
          <div><div className="stat-value">{stats.total || 0}</div><div className="stat-label">Total Requests</div></div>
        </div>
        <div className="stat-card">
          <div className="stat-icon amber">⏳</div>
          <div><div className="stat-value">{stats.open || 0}</div><div className="stat-label">Open Requests</div></div>
        </div>
        <div className="stat-card">
          <div className="stat-icon green">✅</div>
          <div><div className="stat-value">{stats.resolved || 0}</div><div className="stat-label">Resolved</div></div>
        </div>
        <div className="stat-card">
          <div className="stat-icon red">🔔</div>
          <div><div className="stat-value">{data.unread_notifications || 0}</div><div className="stat-label">Unread Notifications</div></div>
        </div>
      </div>
      <div className="card" style={{marginBottom:24}}>
        <div className="card-header">
          <h3 className="card-title">Recent Requests</h3>
          <Link to="/create-request" className="btn btn-primary btn-sm">+ New Request</Link>
        </div>
        {data.recent_requests?.length > 0 ? (
          <div className="table-wrapper">
            <table>
              <thead><tr><th>ID</th><th>Title</th><th>Category</th><th>Priority</th><th>Status</th></tr></thead>
              <tbody>
                {data.recent_requests.map(r => (
                  <tr key={r.id}>
                    <td><Link to={`/requests/${r.id}`}>{r.request_number}</Link></td>
                    <td>{r.title}</td>
                    <td><span className="badge badge-info">{r.category}</span></td>
                    <td><span className={`badge badge-${r.priority === 'HIGH' || r.priority === 'CRITICAL' ? 'danger' : r.priority === 'LOW' ? 'neutral' : 'warning'}`}>{r.priority}</span></td>
                    <td><StatusBadge status={r.status} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state-title">No requests yet</div>
            <div className="empty-state-text">Create your first request to get started</div>
            <Link to="/create-request" className="btn btn-primary">Create Request</Link>
          </div>
        )}
      </div>
    </>
  )
}

function AdminDashboard({ data }) {
  const chartData = Object.entries(data.category_distribution || {}).map(([name, value]) => ({ name, value }))
  const priorityData = Object.entries(data.priority_distribution || {}).map(([name, value]) => ({ name, value }))

  return (
    <>
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon blue">📋</div>
          <div><div className="stat-value">{data.total_requests || 0}</div><div className="stat-label">Total Requests</div></div>
        </div>
        <div className="stat-card">
          <div className="stat-icon amber">⏳</div>
          <div><div className="stat-value">{data.open_requests || 0}</div><div className="stat-label">Open Requests</div></div>
        </div>
        <div className="stat-card">
          <div className="stat-icon red">✅</div>
          <div><div className="stat-value">{data.pending_approvals || 0}</div><div className="stat-label">Pending Approvals</div></div>
        </div>
        <div className="stat-card">
          <div className="stat-icon green">🎉</div>
          <div><div className="stat-value">{data.resolved_today || 0}</div><div className="stat-label">Resolved Today</div></div>
        </div>
      </div>
      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:20,marginBottom:24}}>
        <div className="card">
          <h3 className="card-title" style={{marginBottom:16}}>Requests by Category</h3>
          {chartData.length > 0 ? (
            <div style={{display:'flex',flexDirection:'column',gap:8}}>
              {chartData.map(d => (
                <div key={d.name} style={{display:'flex',alignItems:'center',gap:12}}>
                  <span style={{width:120,fontSize:13,color:'var(--text-secondary)'}}>{d.name}</span>
                  <div style={{flex:1,height:20,background:'var(--bg)',borderRadius:4,overflow:'hidden'}}>
                    <div style={{height:'100%',width:`${Math.min((d.value / Math.max(...chartData.map(c=>c.value),1)) * 100, 100)}%`,background:'var(--secondary)',borderRadius:4,transition:'width 0.5s'}} />
                  </div>
                  <span style={{width:30,textAlign:'right',fontSize:13,fontWeight:600}}>{d.value}</span>
                </div>
              ))}
            </div>
          ) : <div className="empty-state"><div className="empty-state-text">No data yet</div></div>}
        </div>
        <div className="card">
          <h3 className="card-title" style={{marginBottom:16}}>Priority Distribution</h3>
          {priorityData.length > 0 ? (
            <div style={{display:'flex',flexDirection:'column',gap:8}}>
              {priorityData.map(d => (
                <div key={d.name} style={{display:'flex',alignItems:'center',gap:12}}>
                  <span style={{width:100,fontSize:13,color:'var(--text-secondary)'}}>{d.name}</span>
                  <div style={{flex:1,height:20,background:'var(--bg)',borderRadius:4,overflow:'hidden'}}>
                    <div style={{height:'100%',width:`${Math.min((d.value / Math.max(...priorityData.map(c=>c.value),1)) * 100, 100)}%`,background: d.name === 'HIGH' || d.name === 'CRITICAL' ? 'var(--danger)' : d.name === 'LOW' ? 'var(--success)' : 'var(--warning)',borderRadius:4,transition:'width 0.5s'}} />
                  </div>
                  <span style={{width:30,textAlign:'right',fontSize:13,fontWeight:600}}>{d.value}</span>
                </div>
              ))}
            </div>
          ) : <div className="empty-state"><div className="empty-state-text">No data yet</div></div>}
        </div>
      </div>
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Recent Requests</h3>
        </div>
        {data.recent_requests?.length > 0 ? (
          <div className="table-wrapper">
            <table>
              <thead><tr><th>ID</th><th>Title</th><th>Category</th><th>Priority</th><th>Status</th></tr></thead>
              <tbody>
                {data.recent_requests.map(r => (
                  <tr key={r.id}>
                    <td><Link to={`/requests/${r.id}`}>{r.request_number}</Link></td>
                    <td>{r.title}</td>
                    <td><span className="badge badge-info">{r.category}</span></td>
                    <td><span className={`badge badge-${r.priority === 'HIGH' ? 'danger' : r.priority === 'LOW' ? 'neutral' : 'warning'}`}>{r.priority}</span></td>
                    <td><StatusBadge status={r.status} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state-title">No requests yet</div>
            <div className="empty-state-text">Requests will appear here once created</div>
          </div>
        )}
      </div>
    </>
  )
}

function StatusBadge({ status }) {
  const map = {
    NEW: 'info', CLASSIFYING: 'info', ANALYZING: 'info', ROUTING: 'info',
    WAITING_FOR_APPROVAL: 'warning', APPROVED: 'success', IN_PROGRESS: 'info',
    COMPLETED: 'success', REJECTED: 'danger', FAILED: 'danger', CANCELLED: 'neutral',
  }
  return <span className={`badge badge-${map[status] || 'neutral'}`}>{status?.replace(/_/g, ' ')}</span>
}
