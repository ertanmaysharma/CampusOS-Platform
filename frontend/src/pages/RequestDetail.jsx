import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'

const WORKFLOW_STEPS = ['INTAKE', 'CLASSIFICATION', 'PRIORITY', 'RESEARCH', 'ROUTING', 'ANALYSIS', 'VERIFICATION', 'ACTION', 'COMMUNICATION', 'COMPLETED']

export default function RequestDetail() {
  const { id } = useParams()
  const { user } = useAuth()
  const navigate = useNavigate()
  const [request, setRequest] = useState(null)
  const [loading, setLoading] = useState(true)
  const [processing, setProcessing] = useState(false)
  const [feedback, setFeedback] = useState({ rating: 5, comment: '' })

  useEffect(() => {
    api.get(`/requests/${id}`).then(res => setRequest(res.data.data)).catch(() => navigate('/my-requests')).finally(() => setLoading(false))
  }, [id])

  const handleProcess = async () => {
    setProcessing(true)
    try {
      const res = await api.post(`/requests/${id}/process`)
      const updated = await api.get(`/requests/${id}`)
      setRequest(updated.data.data)
    } catch (err) {
      console.error(err)
    }
    setProcessing(false)
  }

  const handleFeedback = async () => {
    try {
      await api.post('/feedback', { request_id: parseInt(id), rating: feedback.rating, comment: feedback.comment })
      setFeedback({ rating: 5, comment: '' })
    } catch (err) {
      console.error(err)
    }
  }

  if (loading) return <div className="loading-spinner" />
  if (!request) return <div className="empty-state"><div className="empty-state-title">Request not found</div></div>

  const workflow = request.workflow
  const currentStep = workflow?.state || 'INTAKE'
  const stepIndex = WORKFLOW_STEPS.indexOf(currentStep)

  return (
    <div style={{maxWidth:900,margin:'0 auto'}}>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'flex-start',marginBottom:24}}>
        <div>
          <h1 style={{fontSize:24,fontWeight:700}}>{request.request_number}</h1>
          <p style={{color:'var(--text-secondary)',fontSize:14}}>{request.title}</p>
        </div>
        <div style={{display:'flex',gap:8}}>
          {(request.status === 'NEW' || request.status === 'FAILED') && (
            <button className="btn btn-primary" onClick={handleProcess} disabled={processing}>
              {processing ? 'Processing...' : 'Process with AI'}
            </button>
          )}
          <button className="btn btn-secondary" onClick={() => navigate(-1)}>Back</button>
        </div>
      </div>

      <div style={{display:'grid',gridTemplateColumns:'2fr 1fr',gap:24}}>
        <div>
          <div className="card" style={{marginBottom:24}}>
            <h3 className="card-title" style={{marginBottom:16}}>Request Details</h3>
            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:16}}>
              <div><div style={{fontSize:12,color:'var(--text-secondary)',marginBottom:4}}>Status</div><StatusBadge status={request.status} /></div>
              <div><div style={{fontSize:12,color:'var(--text-secondary)',marginBottom:4}}>Priority</div><span className={`badge badge-${request.priority === 'HIGH' || request.priority === 'CRITICAL' ? 'danger' : request.priority === 'LOW' ? 'neutral' : 'warning'}`}>{request.priority}</span></div>
              <div><div style={{fontSize:12,color:'var(--text-secondary)',marginBottom:4}}>Category</div><span className="badge badge-info">{request.category}</span></div>
              <div><div style={{fontSize:12,color:'var(--text-secondary)',marginBottom:4}}>Department</div><span style={{fontSize:14}}>{request.department?.name || 'Unassigned'}</span></div>
              <div><div style={{fontSize:12,color:'var(--text-secondary)',marginBottom:4}}>Created</div><span style={{fontSize:14}}>{new Date(request.created_at).toLocaleString()}</span></div>
              <div><div style={{fontSize:12,color:'var(--text-secondary)',marginBottom:4}}>Assigned To</div><span style={{fontSize:14}}>{request.assignee?.name || 'Unassigned'}</span></div>
            </div>
            <div style={{marginTop:20,paddingTop:20,borderTop:'1px solid var(--border)'}}>
              <div style={{fontSize:12,color:'var(--text-secondary)',marginBottom:8}}>Description</div>
              <p style={{fontSize:14,lineHeight:1.6}}>{request.description}</p>
            </div>
          </div>

          <div className="card" style={{marginBottom:24}}>
            <h3 className="card-title" style={{marginBottom:16}}>Feedback</h3>
            <div style={{display:'flex',gap:4,marginBottom:12}}>
              {[1,2,3,4,5].map(star => (
                <button key={star} onClick={() => setFeedback({...feedback, rating: star})}
                  style={{background:'none',border:'none',fontSize:24,color:star <= feedback.rating ? '#f59e0b' : '#d1d5db'}}>
                  ★
                </button>
              ))}
            </div>
            <textarea className="form-textarea" value={feedback.comment} onChange={e => setFeedback({...feedback, comment: e.target.value})} placeholder="Share your experience..." style={{minHeight:80}} />
            <button className="btn btn-primary btn-sm" style={{marginTop:12}} onClick={handleFeedback}>Submit Feedback</button>
          </div>
        </div>

        <div>
          <div className="card" style={{marginBottom:24}}>
            <h3 className="card-title" style={{marginBottom:16}}>Workflow Progress</h3>
            <div className="timeline">
              {WORKFLOW_STEPS.map((step, idx) => {
                let dotClass = 'pending'
                if (idx < stepIndex || (idx === stepIndex && currentStep === 'COMPLETED')) dotClass = 'completed'
                else if (idx === stepIndex) dotClass = 'active'
                return (
                  <div key={step} className="timeline-item">
                    <div className={`timeline-dot ${dotClass}`}>{dotClass === 'completed' ? '✓' : dotClass === 'active' ? '●' : '○'}</div>
                    <div className="timeline-content">
                      <div className="timeline-title" style={{fontSize:13}}>{step.replace(/_/g, ' ')}</div>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          {request.workflow?.requires_human_approval && (
            <div className="card">
              <h3 className="card-title" style={{marginBottom:8}}>Approval Status</h3>
              <span className={`badge badge-${request.workflow.approval_status === 'APPROVED' ? 'success' : request.workflow.approval_status === 'REJECTED' ? 'danger' : 'warning'}`}>
                {request.workflow.approval_status || 'PENDING'}
              </span>
            </div>
          )}
        </div>
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
