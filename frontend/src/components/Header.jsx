import { Link } from 'react-router-dom'

export default function Header() {
  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Raven Custom Glass
            </h1>
            <p className="text-sm text-gray-600 mt-1">
              Shop Drawing Generator
            </p>
          </div>
          <nav className="flex space-x-4">
            <Link
              to="/"
              className="px-4 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100"
            >
              Generator
            </Link>
            <Link
              to="/projects"
              className="px-4 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100"
            >
              Projects
            </Link>
          </nav>
        </div>
      </div>
    </header>
  )
}
