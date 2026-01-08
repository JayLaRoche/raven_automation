import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Navigation } from './components/layout/Navigation'
import { Dashboard } from './components/layout/Dashboard'
import { ProjectDashboard } from './components/dashboard/ProjectDashboard'
import { SalesPresentation } from './components/sales/SalesPresentation'
import { ToastContainer } from './components/ui/Toast'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 flex flex-col">
        {/* Navigation bar with Dashboard and Drawing Generator tabs */}
        <Navigation />

        {/* Main content area */}
        <div className="flex-1">
          <Routes>
            {/* Dashboard - Home Page */}
            <Route path="/" element={<Dashboard />} />

            {/* Projects - Legacy projects list */}
            <Route path="/projects" element={<ProjectDashboard />} />

            {/* Drawing Generator - New drawing tool */}
            <Route path="/generator" element={<SalesPresentation />} />

            {/* Project Editor - Edit existing project */}
            <Route path="/project/:id" element={<SalesPresentation />} />

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>

        <ToastContainer />
      </div>
    </Router>
  )
}

export default App
