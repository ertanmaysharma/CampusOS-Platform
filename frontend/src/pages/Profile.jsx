import { useAuth } from '../context/AuthContext'

export default function Profile() {
  const { user } = useAuth()
  return (
    <div style={{maxWidth:600,margin:'0 auto'}}>
      <h1 style={{fontSize:24,fontWeight:700,marginBottom:24}}>Profile</h1>
      <div className="card">
        <div style={{display:'flex',alignItems:'center',gap:20,marginBottom:24}}>
          <div style={{width:80,height:80,borderRadius:'50%',background:'var(--secondary)',color:'white',display:'flex',alignItems:'center',justifyContent:'center',fontSize:32,fontWeight:700}}>
            {user?.name?.[0] || 'U'}
          </div>
          <div>
            <h2 style={{fontSize:20,fontWeight:600}}>{user?.name}</h2>
            <p style={{color:'var(--text-secondary)',fontSize:14}}>{user?.email}</p>
          </div>
        </div>
        <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:20}}>
          <div><div style={{fontSize:12,color:'var(--text-secondary)',marginBottom:4}}>Role</div><span className="badge badge-info">{user?.role?.name}</span></div>
          <div><div style={{fontSize:12,color:'var(--text-secondary)',marginBottom:4}}>Department</div><span style={{fontSize:14}}>{user?.department?.name || 'N/A'}</span></div>
          <div><div style={{fontSize:12,color:'var(--text-secondary)',marginBottom:4}}>Status</div><span className={`badge badge-${user?.is_active ? 'success' : 'danger'}`}>{user?.is_active ? 'Active' : 'Inactive'}</span></div>
          <div><div style={{fontSize:12,color:'var(--text-secondary)',marginBottom:4}}>Joined</div><span style={{fontSize:14}}>{user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}</span></div>
        </div>
      </div>
    </div>
  )
}
