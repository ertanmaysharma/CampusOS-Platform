import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Register() {
  const [form, setForm] = useState({ name: '', email: '', password: '', confirm_password: '', role: 'STUDENT' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { register } = useAuth()
  const navigate = useNavigate()

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    if (form.password !== form.confirm_password) { setError('Passwords do not match'); return }
    setLoading(true)
    try {
      await register(form)
      navigate('/login')
    } catch (err) {
      setError(err.response?.data?.error?.message || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-left">
        <div style={{textAlign:'center',maxWidth:400}}>
          <div style={{fontSize:48,marginBottom:16}}>🎓</div>
          <h1 style={{fontSize:36,fontWeight:700,marginBottom:12}}>CampusOS</h1>
          <p style={{fontSize:18,opacity:0.8}}>Join the smart campus operations platform</p>
        </div>
      </div>
      <div className="auth-right">
        <div className="auth-form">
          <h2 className="auth-title">Create Account</h2>
          <p className="auth-subtitle">Get started with CampusOS</p>
          {error && <div style={{background:'var(--danger-bg)',color:'var(--danger)',padding:'12px 16px',borderRadius:8,marginBottom:20,fontSize:14}}>{error}</div>}
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">Full Name</label>
              <input type="text" name="name" className="form-input" value={form.name} onChange={handleChange} placeholder="Your full name" required />
            </div>
            <div className="form-group">
              <label className="form-label">Email</label>
              <input type="email" name="email" className="form-input" value={form.email} onChange={handleChange} placeholder="you@campus.edu" required />
            </div>
            <div className="form-group">
              <label className="form-label">Role</label>
              <select name="role" className="form-select" value={form.role} onChange={handleChange}>
                <option value="STUDENT">Student</option>
                <option value="FACULTY">Faculty</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Password</label>
              <input type="password" name="password" className="form-input" value={form.password} onChange={handleChange} placeholder="Min 8 characters" required />
            </div>
            <div className="form-group">
              <label className="form-label">Confirm Password</label>
              <input type="password" name="confirm_password" className="form-input" value={form.confirm_password} onChange={handleChange} placeholder="Repeat password" required />
            </div>
            <button type="submit" className="btn btn-primary" disabled={loading} style={{width:'100%',justifyContent:'center',padding:'12px 20px',fontSize:15}}>
              {loading ? 'Creating account...' : 'Create Account'}
            </button>
          </form>
          <p style={{textAlign:'center',marginTop:24,fontSize:14,color:'var(--text-secondary)'}}>
            Already have an account? <Link to="/login" className="auth-link">Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
