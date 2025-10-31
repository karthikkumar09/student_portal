import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Home = () => {
  const { isAuthenticated, isAdmin, isStudent } = useAuth();

  if (isAuthenticated) {
    if (isAdmin) {
      window.location.href = '/admin/dashboard';
    } else if (isStudent) {
      window.location.href = '/student/dashboard';
    }
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-blue-900 mb-4">
            Welcome to Student Portal
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Manage your courses, track your progress, and achieve your goals
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-xl p-8 hover:shadow-2xl transition-shadow">
            <h2 className="text-2xl font-bold text-blue-600 mb-4">Students</h2>
            <p className="text-gray-600 mb-6">
              Browse courses, enroll, track your progress, and manage your academic journey
            </p>
            <div className="space-y-3">
              <Link
                to="/login"
                className="block w-full bg-blue-600 text-white text-center py-3 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Student Login
              </Link>
              <Link
                to="/register"
                className="block w-full bg-green-600 text-white text-center py-3 rounded-lg hover:bg-green-700 transition-colors"
              >
                Register Now
              </Link>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-xl p-8 hover:shadow-2xl transition-shadow">
            <h2 className="text-2xl font-bold text-yellow-600 mb-4">Administrators</h2>
            <p className="text-gray-600 mb-6">
              Manage courses, students, enrollments, and monitor system performance
            </p>
            <Link
              to="/admin-login"
              className="block w-full bg-yellow-500 text-white text-center py-3 rounded-lg hover:bg-yellow-600 transition-colors"
            >
              Admin Login
            </Link>
          </div>
        </div>

        <div className="mt-16 text-center">
          <h3 className="text-2xl font-semibold text-gray-800 mb-8">Features</h3>
          <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-4xl mb-4">📚</div>
              <h4 className="font-semibold text-lg mb-2">Course Management</h4>
              <p className="text-gray-600">Browse and enroll in diverse courses</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-4xl mb-4">📊</div>
              <h4 className="font-semibold text-lg mb-2">Progress Tracking</h4>
              <p className="text-gray-600">Monitor your academic progress</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-4xl mb-4">🎓</div>
              <h4 className="font-semibold text-lg mb-2">Achievement Goals</h4>
              <p className="text-gray-600">Complete courses and earn credits</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
