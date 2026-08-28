import { useState, useEffect } from 'react'
import api from '../services/api'

export default function AdminAudit() {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)
  const [actionFilter, setActionFilter] = useState('')

  useEffect(() => {
    setLoading(true)
    const params = { per_page: 50 }
    if (actionFilter) params.action = actionFilter
    api.get('/audit-logs', { params }).then(res => setLogs(res.data.data.items || [])).catch(() => {}).finally(() => setLoading(false))
  }, [actionFilter])

  return (
    <div>
      <h1 style={{fontSize:24,fontWeight:700,marginBottom:24}}>Audit Logs</h1>
      <div className="card">
        <div style={{marginBottom:16}}>
          <select className="form-select" style={{width:200}} value={actionFilter} onChange={e => setActionFilter(e.target.value)}>
            <option value="">All Actions</option>
            <option value="REQUEST_CREATED">Request Created</option>
            <option value="REQUEST_UPDATED">Request Updated</option>
            <option value="WORKFLOW_COMPLETED">Workflow Completed</option>
            <option value="APPROVAL_APPROVED">Approval Approved</option>
            <option value="APPROVAL_REJECTED">Approval Rejected</option>
            <option value="USER_CREATED">User Created</option>
          </select>
        </div>
        {loading ? <div className="loading-spinner" /> : logs.length > 0 ? (
          <div className="table-wrapper">
            <table>
              <thead><tr><th>Timestamp</th><th>Action</th><th>Actor</th><th>Request</th><th>Details</th></tr></thead>
              <tbody>
                {logs.map(l => (
                  <tr key={l.id}>
                    <td style={{fontSize:13}}>{new Date(l.created_at).toLocaleString()}</td>
                    <td><span className="badge badge-info">{l.action}</span></td>
                    <td>{l.user?.name || l.actor_type}</td>
                    <td>{l.request_id ? `REQ-${l.request_id}` : '-'}</td>
                    <td style={{fontSize:12,maxWidth:200,overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>{l.metadata ? JSON.stringify(l.metadata) : '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : <div className="empty-state"><div className="empty-state-title">No audit logs</div></div>}
      </div>
    </div>
  )
}
