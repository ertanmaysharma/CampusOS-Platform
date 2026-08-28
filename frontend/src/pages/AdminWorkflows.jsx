import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import api from '../services/api'

export default function AdminWorkflows() {
  const [workflows, setWorkflows] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/workflows').then(res => setWorkflows(res.data.data.items || [])).catch(() => {}).finally(() => setLoading(false))
  }, [])

  return (
    <div>
      <h1 style={{fontSize:24,fontWeight:700,marginBottom:24}}>Workflows</h1>
      <div className="card">
        {loading ? <div className="loading-spinner" /> : workflows.length > 0 ? (
          <div className="table-wrapper">
            <table>
              <thead><tr><th>ID</th><th>Request</th><th>State</th><th>Agent</th><th>Status</th><th>Created</th></tr></thead>
              <tbody>
                {workflows.map(w => (
                  <tr key={w.id}>
                    <td>WF-{w.id}</td>
                    <td><Link to={`/requests/${w.request_id}`}>REQ-{w.request_id}</Link></td>
                    <td><span className="badge badge-info">{w.state?.replace(/_/g, ' ')}</span></td>
                    <td>{w.current_agent || '-'}</td>
                    <td><span className={`badge badge-${w.status === 'COMPLETED' ? 'success' : w.status === 'FAILED' ? 'danger' : 'warning'}`}>{w.status}</span></td>
                    <td style={{fontSize:13,color:'var(--text-secondary)'}}>{new Date(w.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : <div className="empty-state"><div className="empty-state-title">No workflows</div></div>}
      </div>
    </div>
  )
}
