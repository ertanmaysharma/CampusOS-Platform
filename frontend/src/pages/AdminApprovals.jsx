import { useState, useEffect } from 'react'
import api from '../services/api'

export default function AdminApprovals() {
  const [approvals, setApprovals] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchApprovals = () => {
    api.get('/approvals').then(res => setApprovals(res.data.data.items || [])).catch(() => {}).finally(() => setLoading(false))
  }

  useEffect(() => { fetchApprovals() }, [])

  const handleApprove = async (id) => {
    await api.post(`/approvals/${id}/approve`, { comment: 'Approved by administrator' })
    fetchApprovals()
  }

  const handleReject = async (id) => {
    await api.post(`/approvals/${id}/reject`, { comment: 'Rejected by administrator' })
    fetchApprovals()
  }

  return (
    <div>
      <h1 style={{fontSize:24,fontWeight:700,marginBottom:24}}>Pending Approvals</h1>
      {loading ? <div className="loading-spinner" /> : approvals.length > 0 ? (
        <div style={{display:'flex',flexDirection:'column',gap:16}}>
          {approvals.map(a => (
            <div key={a.id} className="card">
              <div style={{display:'flex',justifyContent:'space-between',alignItems:'flex-start'}}>
                <div>
                  <div style={{fontSize:12,color:'var(--text-secondary)',marginBottom:4}}>Approval #{a.id}</div>
                  <div style={{fontSize:14,fontWeight:500,marginBottom:8}}>{a.reason}</div>
                  <div style={{display:'flex',gap:12}}>
                    <span className={`badge badge-${a.risk_level === 'HIGH' || a.risk_level === 'CRITICAL' ? 'danger' : 'warning'}`}>Risk: {a.risk_level}</span>
                    <span className="badge badge-info">Workflow: {a.workflow_id}</span>
                  </div>
                </div>
                <div style={{display:'flex',gap:8}}>
                  <button className="btn btn-success btn-sm" onClick={() => handleApprove(a.id)}>Approve</button>
                  <button className="btn btn-danger btn-sm" onClick={() => handleReject(a.id)}>Reject</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card">
          <div className="empty-state">
            <div className="empty-state-title">No pending approvals</div>
            <div className="empty-state-text">All caught up!</div>
          </div>
        </div>
      )}
    </div>
  )
}
