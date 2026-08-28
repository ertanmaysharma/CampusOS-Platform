import { useState, useEffect } from 'react'
import api from '../services/api'

export default function AdminUsers() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [form, setForm] = useState({ name: '', email: '', password: '', role: 'STUDENT', department_id: '' })
  const [departments, setDepartments] = useState([])
  const [roles, setRoles] = useState([])

  const fetchUsers = () => {
    api.get('/users').then(res => setUsers(res.data.data.items || [])).catch(() => {}).finally(() => setLoading(false))
  }

  useEffect(() => {
    fetchUsers()
    api.get('/departments').then(res => setDepartments(res.data.data || [])).catch(() => {})
    api.get('/admin/roles').then(res => setRoles(res.data.data || [])).catch(() => {})
  }, [])

  const handleCreate = async (e) => {
    e.preventDefault()
    try {
      await api.post('/users', { ...form, department_id: form.department_id ? parseInt(form.department_id) : undefined })
      setShowModal(false)
      setForm({ name: '', email: '', password: '', role: 'STUDENT', department_id: '' })
      fetchUsers()
    } catch (err) {
      alert(err.response?.data?.error?.message || 'Failed to create user')
    }
  }

  return (
    <div>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:24}}>
        <h1 style={{fontSize:24,fontWeight:700}}>Users</h1>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>+ Add User</button>
      </div>
      <div className="card">
        {loading ? <div className="loading-spinner" /> : (
          <div className="table-wrapper">
            <table>
              <thead><tr><th>Name</th><th>Email</th><th>Role</th><th>Department</th><th>Status</th></tr></thead>
              <tbody>
                {users.map(u => (
                  <tr key={u.id}>
                    <td style={{fontWeight:500}}>{u.name}</td>
                    <td>{u.email}</td>
                    <td><span className="badge badge-purple">{u.role?.name}</span></td>
                    <td>{u.department?.name || '-'}</td>
                    <td><span className={`badge badge-${u.is_active ? 'success' : 'danger'}`}>{u.is_active ? 'Active' : 'Inactive'}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3 className="modal-title">Add User</h3>
              <button onClick={() => setShowModal(false)} style={{background:'none',border:'none',fontSize:20}}>✕</button>
            </div>
            <form onSubmit={handleCreate}>
              <div className="form-group">
                <label className="form-label">Name</label>
                <input className="form-input" value={form.name} onChange={e => setForm({...form, name: e.target.value})} required />
              </div>
              <div className="form-group">
                <label className="form-label">Email</label>
                <input type="email" className="form-input" value={form.email} onChange={e => setForm({...form, email: e.target.value})} required />
              </div>
              <div className="form-group">
                <label className="form-label">Password</label>
                <input type="password" className="form-input" value={form.password} onChange={e => setForm({...form, password: e.target.value})} required />
              </div>
              <div className="form-group">
                <label className="form-label">Role</label>
                <select className="form-select" value={form.role} onChange={e => setForm({...form, role: e.target.value})}>
                  {roles.map(r => <option key={r.id} value={r.name}>{r.name}</option>)}
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Department</label>
                <select className="form-select" value={form.department_id} onChange={e => setForm({...form, department_id: e.target.value})}>
                  <option value="">None</option>
                  {departments.map(d => <option key={d.id} value={d.id}>{d.name}</option>)}
                </select>
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
