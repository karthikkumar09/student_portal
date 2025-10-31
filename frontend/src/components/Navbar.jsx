import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navbar = () => {
  const { user, logout, isAuthenticated, isAdmin, isStudent } = useAuth();

  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="text-xl font-bold">
              Student Portal
            </Link>
            
            {isAuthenticated && (
              <div className="ml-10 flex space-x-4">
                {isStudent && (
                  <>
                    <Link 
                      to="/student/dashboard" 
                      className="hover:bg-blue-700 px-3 py-2 rounded-md"
                    >
                      Dashboard
                    </Link>
                    <Link 
                      to="/student/my-courses" 
                      className="hover:bg-blue-700 px-3 py-2 rounded-md"
                    >
                      My Courses
                    </Link>
                    <Link 
                      to="/student/browse-courses" 
                      className="hover:bg-blue-700 px-3 py-2 rounded-md"
                    >
                      Browse Courses
                    </Link>
                  </>
                )}
                
                {isAdmin && (
                  <>
                    <Link 
                      to="/admin/dashboard" 
                      className="hover:bg-blue-700 px-3 py-2 rounded-md"
                    >
                      Dashboard
                    </Link>
                    <Link 
                      to="/admin/courses" 
                      className="hover:bg-blue-700 px-3 py-2 rounded-md"
                    >
                      Manage Courses
                    </Link>
                    <Link 
                      to="/admin/students" 
                      className="hover:bg-blue-700 px-3 py-2 rounded-md"
                    >
                      Manage Students
                    </Link>
                  </>
                )}
              </div>
            )}
          </div>
          
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <span className="text-sm">
                  Welcome, <strong>{user?.name}</strong>
                </span>
                <button
                  onClick={logout}
                  className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded-md"
                >
                  Logout
                </button>
              </>
            ) : (
              <div className="space-x-2">
                <Link 
                  to="/login" 
                  className="bg-white text-blue-600 hover:bg-gray-100 px-4 py-2 rounded-md"
                >
                  Student Login
                </Link>
                <Link 
                  to="/admin-login" 
                  className="bg-yellow-500 hover:bg-yellow-600 px-4 py-2 rounded-md text-white"
                >
                  Admin Login
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
