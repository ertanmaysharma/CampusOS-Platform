import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await login(email, password)
      navigate('/dashboard')
    } catch (err) {
      if (err.response) {
        setError(err.response?.data?.error?.message || 'Invalid credentials')
      } else {
        setError('Unable to connect to server. Please try again later.')
      }
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
          <p style={{fontSize:18,opacity:0.8}}>An Autonomous AI Workforce for Smarter Campus Operations</p>
          <div style={{marginTop:40,padding:20,borderRadius:12,background:'rgba(255,255,255,0.1)',textAlign:'left'}}>
            <p style={{fontSize:14,opacity:0.9}}>💡 "The water cooler near Block B has not worked for 3 days."</p>
            <p style={{fontSize:13,opacity:0.7,marginTop:8}}>CampusOS automatically classifies, routes, and resolves campus requests.</p>
          </div>
        </div>
      </div>
      <div className="auth-right">
        <div className="auth-form">
          <h2 className="auth-title">Welcome back</h2>
          <p className="auth-subtitle">Sign in to your CampusOS account</p>
          {error && <div style={{background:'var(--danger-bg)',color:'var(--danger)',padding:'12px 16px',borderRadius:8,marginBottom:20,fontSize:14}}>{error}</div>}
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">Email address</label>
              <input type="email" className="form-input" value={email} onChange={e => setEmail(e.target.value)} placeholder="you@campus.edu" required />
            </div>
            <div className="form-group">
              <label className="form-label">Password</label>
              <div style={{position:'relative'}}>
                <input type={showPassword ? 'text' : 'password'} className="form-input" value={password} onChange={e => setPassword(e.target.value)} placeholder="Enter your password" required style={{paddingRight:44}} />
                <button type="button" onClick={() => setShowPassword(!showPassword)} style={{position:'absolute',right:12,top:'50%',transform:'translateY(-50%)',background:'none',border:'none',color:'var(--text-secondary)',fontSize:18}}>
                  {showPassword ? '🙈' : '👁️'}
                </button>
              </div>
            </div>
            <button type="submit" className="btn btn-primary" disabled={loading} style={{width:'100%',justifyContent:'center',padding:'12px 20px',fontSize:15}}>
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>
          <p style={{textAlign:'center',marginTop:24,fontSize:14,color:'var(--text-secondary)'}}>
            Don't have an account? <Link to="/register" className="auth-link">Create one</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
