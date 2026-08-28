import { useState, useEffect } from 'react'
import api from '../services/api'

export default function AdminKnowledge() {
  const [docs, setDocs] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [form, setForm] = useState({ title: '', content: '', category: 'General' })

  const fetchDocs = () => {
    api.get('/knowledge').then(res => setDocs(res.data.data.items || [])).catch(() => {}).finally(() => setLoading(false))
  }

  useEffect(() => { fetchDocs() }, [])

  const handleCreate = async (e) => {
    e.preventDefault()
    try {
      await api.post('/knowledge', form)
      setShowModal(false)
      setForm({ title: '', content: '', category: 'General' })
      fetchDocs()
    } catch (err) {
      alert(err.response?.data?.error?.message || 'Failed')
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Delete this document?')) return
    await api.delete(`/knowledge/${id}`)
    fetchDocs()
  }

  return (
    <div>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:24}}>
        <h1 style={{fontSize:24,fontWeight:700}}>Knowledge Base</h1>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>+ Add Document</button>
      </div>
      <div className="card">
        {loading ? <div className="loading-spinner" /> : docs.length > 0 ? (
          <div style={{display:'flex',flexDirection:'column',gap:12}}>
            {docs.map(d => (
              <div key={d.id} style={{padding:16,border:'1px solid var(--border)',borderRadius:8,display:'flex',justifyContent:'space-between',alignItems:'flex-start'}}>
                <div style={{flex:1}}>
                  <div style={{fontWeight:600,marginBottom:4}}>{d.title}</div>
                  <div style={{fontSize:13,color:'var(--text-secondary)',marginBottom:8}}>{d.content?.substring(0,150)}...</div>
                  <span className="badge badge-info">{d.category}</span>
                </div>
                <button className="btn btn-danger btn-sm" onClick={() => handleDelete(d.id)}>Delete</button>
              </div>
            ))}
          </div>
        ) : <div className="empty-state"><div className="empty-state-title">No documents</div></div>}
      </div>
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3 className="modal-title">Add Document</h3>
              <button onClick={() => setShowModal(false)} style={{background:'none',border:'none',fontSize:20}}>✕</button>
            </div>
            <form onSubmit={handleCreate}>
              <div className="form-group">
                <label className="form-label">Title</label>
                <input className="form-input" value={form.title} onChange={e => setForm({...form, title: e.target.value})} required />
              </div>
              <div className="form-group">
                <label className="form-label">Category</label>
                <select className="form-select" value={form.category} onChange={e => setForm({...form, category: e.target.value})}>
                  <option>General</option><option>Hostel Rules</option><option>Maintenance Procedures</option>
                  <option>IT Support</option><option>Scholarship Policies</option><option>Campus Policies</option>
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Content</label>
                <textarea className="form-textarea" value={form.content} onChange={e => setForm({...form, content: e.target.value})} required />
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
