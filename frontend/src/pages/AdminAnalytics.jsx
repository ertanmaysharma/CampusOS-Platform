import { useState, useEffect } from 'react'
import api from '../services/api'

export default function AdminAnalytics() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/dashboard/admin').then(res => setData(res.data.data)).catch(() => {}).finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="loading-spinner" />
  if (!data) return <div className="empty-state"><div className="empty-state-title">No analytics data</div></div>

  const categories = Object.entries(data.category_distribution || {}).map(([name, value]) => ({ name, value }))
  const priorities = Object.entries(data.priority_distribution || {}).map(([name, value]) => ({ name, value }))
  const statuses = Object.entries(data.status_distribution || {}).map(([name, value]) => ({ name, value }))
  const departments = Object.entries(data.department_workload || {}).map(([name, value]) => ({ name, value }))

  return (
    <div>
      <h1 style={{fontSize:24,fontWeight:700,marginBottom:24}}>Analytics</h1>
      <div className="stats-grid" style={{marginBottom:32}}>
        <div className="stat-card"><div className="stat-icon blue">📋</div><div><div className="stat-value">{data.total_requests || 0}</div><div className="stat-label">Total Requests</div></div></div>
        <div className="stat-card"><div className="stat-icon amber">⏳</div><div><div className="stat-value">{data.open_requests || 0}</div><div className="stat-label">Open</div></div></div>
        <div className="stat-card"><div className="stat-icon red">⚠️</div><div><div className="stat-value">{data.failed_workflows || 0}</div><div className="stat-label">Failed Workflows</div></div></div>
        <div className="stat-card"><div className="stat-icon green">⏱️</div><div><div className="stat-value">{data.average_resolution_hours || '-'}</div><div className="stat-label">Avg Resolution (hrs)</div></div></div>
      </div>
      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:24,marginBottom:24}}>
        <div className="card">
          <h3 className="card-title" style={{marginBottom:16}}>By Category</h3>
          {categories.map(c => (
            <div key={c.name} style={{display:'flex',alignItems:'center',gap:12,marginBottom:8}}>
              <span style={{width:100,fontSize:13}}>{c.name}</span>
              <div style={{flex:1,height:20,background:'var(--bg)',borderRadius:4,overflow:'hidden'}}>
                <div style={{height:'100%',width:`${Math.min((c.value/Math.max(...categories.map(x=>x.value),1))*100,100)}%`,background:'var(--secondary)',borderRadius:4}} />
              </div>
              <span style={{width:30,textAlign:'right',fontSize:13,fontWeight:600}}>{c.value}</span>
            </div>
          ))}
        </div>
        <div className="card">
          <h3 className="card-title" style={{marginBottom:16}}>By Department</h3>
          {departments.map(d => (
            <div key={d.name} style={{display:'flex',alignItems:'center',gap:12,marginBottom:8}}>
              <span style={{width:100,fontSize:13}}>{d.name}</span>
              <div style={{flex:1,height:20,background:'var(--bg)',borderRadius:4,overflow:'hidden'}}>
                <div style={{height:'100%',width:`${Math.min((d.value/Math.max(...departments.map(x=>x.value),1))*100,100)}%`,background:'var(--accent)',borderRadius:4}} />
              </div>
              <span style={{width:30,textAlign:'right',fontSize:13,fontWeight:600}}>{d.value}</span>
            </div>
          ))}
        </div>
      </div>
      <div className="card">
        <h3 className="card-title" style={{marginBottom:16}}>Status Distribution</h3>
        <div style={{display:'flex',gap:16,flexWrap:'wrap'}}>
          {statuses.map(s => (
            <div key={s.name} style={{textAlign:'center',padding:'16px 24px',border:'1px solid var(--border)',borderRadius:8}}>
              <div style={{fontSize:24,fontWeight:700}}>{s.value}</div>
              <div style={{fontSize:12,color:'var(--text-secondary)',marginTop:4}}>{s.name.replace(/_/g,' ')}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
