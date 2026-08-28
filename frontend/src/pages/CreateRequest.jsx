import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

const CATEGORIES = ['Hostel', 'Maintenance', 'Facilities', 'Academics', 'Finance', 'Administration', 'IT Support', 'Lost and Found', 'Student Grievance', 'Other']

export default function CreateRequest() {
  const [form, setForm] = useState({ title: '', description: '', category: 'Maintenance', priority: 'MEDIUM' })
  const [loading, setLoading] = useState(false)
  const [processing, setProcessing] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const res = await api.post('/requests', form)
      const requestId = res.data.data.id
      // Process through AI
      setProcessing(true)
      try {
        const procRes = await api.post(`/requests/${requestId}/process`)
        setResult(procRes.data.data)
      } catch {
        // Processing may fail but request was created
      }
      setProcessing(false)
      setLoading(false)
      navigate(`/requests/${requestId}`)
    } catch (err) {
      setError(err.response?.data?.error?.message || 'Failed to create request')
      setLoading(false)
    }
  }

  return (
    <div style={{maxWidth:700,margin:'0 auto'}}>
      <h1 style={{fontSize:24,fontWeight:700,marginBottom:8}}>Create Request</h1>
      <p style={{color:'var(--text-secondary)',fontSize:14,marginBottom:32}}>Submit a new campus request. Our AI workforce will process it automatically.</p>

      {error && <div style={{background:'var(--danger-bg)',color:'var(--danger)',padding:'12px 16px',borderRadius:8,marginBottom:20,fontSize:14}}>{error}</div>}

      <div className="card">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Request Title</label>
            <input type="text" name="title" className="form-input" value={form.title} onChange={handleChange} placeholder="Brief description of your request" required maxLength={200} />
          </div>
          <div className="form-group">
            <label className="form-label">Description</label>
            <textarea name="description" className="form-textarea" value={form.description} onChange={handleChange} placeholder="Provide details about your request..." required />
          </div>
          <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:16}}>
            <div className="form-group">
              <label className="form-label">Category</label>
              <select name="category" className="form-select" value={form.category} onChange={handleChange}>
                {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Priority</label>
              <select name="priority" className="form-select" value={form.priority} onChange={handleChange}>
                <option value="LOW">Low</option>
                <option value="MEDIUM">Medium</option>
                <option value="HIGH">High</option>
                <option value="CRITICAL">Critical</option>
              </select>
            </div>
          </div>
          <div style={{display:'flex',gap:12,justifyContent:'flex-end'}}>
            <button type="button" className="btn btn-secondary" onClick={() => navigate(-1)}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={loading || processing}>
              {processing ? 'Processing with AI...' : loading ? 'Creating...' : 'Submit Request'}
            </button>
          </div>
        </form>
      </div>

      {(loading || processing) && (
        <div className="card" style={{marginTop:20,textAlign:'center',padding:32}}>
          <div className="loading-spinner" />
          <p style={{color:'var(--text-secondary)',marginTop:12}}>
            {processing ? 'AI is processing your request...' : 'Creating your request...'}
          </p>
        </div>
      )}
    </div>
  )
}
