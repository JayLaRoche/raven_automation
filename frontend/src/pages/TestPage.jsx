import React from 'react'

export default function TestPage() {
  return (
    <div style={{ padding: '40px', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ color: '#333' }}>✅ React is Working!</h1>
      <p style={{ color: '#666', fontSize: '16px' }}>
        If you can see this page, React and the app are loading correctly.
      </p>
      <div style={{ marginTop: '20px', padding: '20px', backgroundColor: '#f0f0f0', borderRadius: '8px' }}>
        <h2>Debug Info:</h2>
        <p>Frontend: http://localhost:3000 ✅</p>
        <p>Backend: http://localhost:8000</p>
        <p>React loaded at: {new Date().toLocaleTimeString()}</p>
      </div>
    </div>
  )
}
