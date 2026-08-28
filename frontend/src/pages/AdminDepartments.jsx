import { useState, useEffect } from 'react'
import api from '../services/api'

export default function AdminDepartments() {
  const [depts, setDepts] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [form, setForm] = useState({ name: '', description: '' })

  const fetchDepts = () => {
    api.get('/departments').then(res => setDepts(res.data.data || [])).catch(() => {}).finally(() => setLoading(false))
  }

  useEffect(() => { fetchDepts() }, [])

  const handleCreate = async (e) => {
    e.preventDefault()
    try {
      await api.post('/departments', form)
      setShowModal(false)
      setForm({ name: '', description: '' })
      fetchDepts()
    } catch (err) {
      alert(err.response?.data?.error?.message || 'Failed')
    }
  }

  return (
    <div>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:24}}>
        <h1 style={{fontSize:24,fontWeight:700}}>Departments</h1>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>+ Add Department</button>
      </div>
      <div className="card">
        {loading ? <div className="loading-spinner" /> : depts.length > 0 ? (
          <div className="table-wrapper">
            <table>
              <thead><tr><th>Name</th><th>Description</th><th>Users</th><th>Status</th></tr></thead>
              <tbody>
                {depts.map(d => (
                  <tr key={d.id}>
                    <td style={{fontWeight:500}}>{d.name}</td>
                    <td>{d.description || '-'}</td>
                    <td>{d.user_count || 0}</td>
                    <td><span className={`badge badge-${d.is_active ? 'success' : 'danger'}`}>{d.is_active ? 'Active' : 'Inactive'}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : <div className="empty-state"><div className="empty-state-title">No departments</div></div>}
      </div>
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3 className="modal-title">Add Department</h3>
              <button onClick={() => setShowModal(false)} style={{background:'none',border:'none',fontSize:20}}>✕</button>
            </div>
            <form onSubmit={handleCreate}>
              <div className="form-group">
                <label className="form-label">Name</label>
                <input className="form-input" value={form.name} onChange={e => setForm({...form, name: e.target.value})} required />
              </div>
              <div className="form-group">
                <label className="form-label">Description</label>
                <textarea className="form-textarea" value={form.description} onChange={e => setForm({...form, description: e.target.value})} style={{minHeight:80}} />
              </div>
              <div style={{display:'flex',gap:8,justifyContent:'flex-end'}}>
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary">Create</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
