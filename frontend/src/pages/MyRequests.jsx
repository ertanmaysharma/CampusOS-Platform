import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import api from '../services/api'

export default function MyRequests() {
  const [requests, setRequests] = useState([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({ status: '', category: '' })
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)

  useEffect(() => {
    setLoading(true)
    const params = { page, per_page: 15 }
    if (filters.status) params.status = filters.status
    if (filters.category) params.category = filters.category
    api.get('/requests', { params }).then(res => {
      setRequests(res.data.data.items || [])
      setTotal(res.data.data.total || 0)
    }).catch(() => {}).finally(() => setLoading(false))
  }, [filters, page])

  return (
    <div>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:24}}>
        <div>
          <h1 style={{fontSize:24,fontWeight:700}}>My Requests</h1>
          <p style={{color:'var(--text-secondary)',fontSize:14}}>{total} total requests</p>
        </div>
        <Link to="/create-request" className="btn btn-primary">+ New Request</Link>
      </div>
      <div className="card">
        <div style={{display:'flex',gap:12,marginBottom:16}}>
          <select className="form-select" style={{width:160}} value={filters.status} onChange={e => {setFilters({...filters, status: e.target.value}); setPage(1)}}>
            <option value="">All Status</option>
            <option value="NEW">New</option>
            <option value="IN_PROGRESS">In Progress</option>
            <option value="WAITING_FOR_APPROVAL">Pending Approval</option>
            <option value="COMPLETED">Completed</option>
            <option value="REJECTED">Rejected</option>
          </select>
          <select className="form-select" style={{width:160}} value={filters.category} onChange={e => {setFilters({...filters, category: e.target.value}); setPage(1)}}>
            <option value="">All Categories</option>
            <option value="Maintenance">Maintenance</option>
            <option value="Facilities">Facilities</option>
            <option value="Hostel">Hostel</option>
            <option value="IT Support">IT Support</option>
            <option value="Finance">Finance</option>
            <option value="Administration">Administration</option>
          </select>
        </div>
        {loading ? <div className="loading-spinner" /> : requests.length > 0 ? (
          <div className="table-wrapper">
            <table>
              <thead><tr><th>ID</th><th>Title</th><th>Category</th><th>Priority</th><th>Status</th><th>Created</th></tr></thead>
              <tbody>
                {requests.map(r => (
                  <tr key={r.id}>
                    <td><Link to={`/requests/${r.id}`} style={{fontWeight:500}}>{r.request_number}</Link></td>
                    <td>{r.title}</td>
                    <td><span className="badge badge-info">{r.category}</span></td>
                    <td><span className={`badge badge-${r.priority === 'HIGH' || r.priority === 'CRITICAL' ? 'danger' : r.priority === 'LOW' ? 'neutral' : 'warning'}`}>{r.priority}</span></td>
                    <td><StatusBadge status={r.status} /></td>
                    <td style={{fontSize:13,color:'var(--text-secondary)'}}>{new Date(r.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state-title">No requests found</div>
            <div className="empty-state-text">Try adjusting your filters or create a new request</div>
            <Link to="/create-request" className="btn btn-primary">Create Request</Link>
          </div>
        )}
        {total > 15 && (
          <div style={{display:'flex',justifyContent:'center',gap:8,marginTop:16}}>
            <button className="btn btn-secondary btn-sm" disabled={page===1} onClick={() => setPage(p=>p-1)}>Previous</button>
            <span style={{padding:'6px 12px',fontSize:14}}>Page {page}</span>
            <button className="btn btn-secondary btn-sm" disabled={requests.length < 15} onClick={() => setPage(p=>p+1)}>Next</button>
          </div>
        )}
      </div>
    </div>
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
