import { useState, useEffect } from 'react'
import api from '../services/api'

export default function Notifications() {
  const [notifications, setNotifications] = useState([])
  const [loading, setLoading] = useState(true)
  const [unreadCount, setUnreadCount] = useState(0)

  const fetchNotifications = () => {
    api.get('/notifications').then(res => {
      setNotifications(res.data.data.items || [])
      setUnreadCount(res.data.data.unread_count || 0)
    }).catch(() => {}).finally(() => setLoading(false))
  }

  useEffect(() => { fetchNotifications() }, [])

  const markRead = async (id) => {
    await api.patch(`/notifications/${id}/read`)
    fetchNotifications()
  }

  const markAllRead = async () => {
    await api.patch('/notifications/read-all')
    fetchNotifications()
  }

  if (loading) return <div className="loading-spinner" />

  return (
    <div style={{maxWidth:800,margin:'0 auto'}}>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:24}}>
        <div>
          <h1 style={{fontSize:24,fontWeight:700}}>Notifications</h1>
          <p style={{color:'var(--text-secondary)',fontSize:14}}>{unreadCount} unread</p>
        </div>
        {unreadCount > 0 && <button className="btn btn-secondary btn-sm" onClick={markAllRead}>Mark all as read</button>}
      </div>
      <div className="card">
        {notifications.length > 0 ? (
          <div style={{display:'flex',flexDirection:'column'}}>
            {notifications.map(n => (
              <div key={n.id} style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'14px 16px',borderBottom:'1px solid var(--border-light)',background:n.is_read?'transparent':'var(--info-bg)',borderRadius:8,marginBottom:4}}>
                <div>
                  <div style={{fontWeight:n.is_read?400:600,fontSize:14}}>{n.title}</div>
                  <div style={{fontSize:13,color:'var(--text-secondary)',marginTop:2}}>{n.message}</div>
                  <div style={{fontSize:12,color:'var(--text-light)',marginTop:4}}>{new Date(n.created_at).toLocaleString()}</div>
                </div>
                {!n.is_read && <button className="btn btn-secondary btn-sm" onClick={() => markRead(n.id)}>Mark read</button>}
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state-title">No notifications</div>
            <div className="empty-state-text">You're all caught up!</div>
          </div>
        )}
      </div>
    </div>
  )
}
