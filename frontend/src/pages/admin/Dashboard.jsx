import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { adminService, courseService, enrollmentService } from '../../services/api';

const AdminDashboard = () => {
  const [stats, setStats] = useState({
    totalStudents: 0,
    totalCourses: 0,
    totalEnrollments: 0,
    activeEnrollments: 0,
    completedEnrollments: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [recentCourses, setRecentCourses] = useState([]);
  const [recentStudents, setRecentStudents] = useState([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [studentsRes, coursesRes, enrollmentStatsRes] = await Promise.all([
        adminService.getAllStudents(0, 10),
        courseService.getAllCourses(0, 10),
        enrollmentService.getStats(),
      ]);

      setStats({
        totalStudents: studentsRes.data.total,
        totalCourses: coursesRes.data.total,
        totalEnrollments: enrollmentStatsRes.data.total,
        activeEnrollments: enrollmentStatsRes.data.enrolled,
        completedEnrollments: enrollmentStatsRes.data.completed,
      });

      setRecentCourses(coursesRes.data.courses.slice(0, 5));
      setRecentStudents(studentsRes.data.students.slice(0, 5));
    } catch (err) {
      setError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="text-gray-600 mt-2">System overview and management</p>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {/* Stats Cards */}
        <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Total Students</p>
                <p className="text-3xl font-bold text-blue-600">{stats.totalStudents}</p>
              </div>
              <div className="bg-blue-100 p-3 rounded-full">
                <span className="text-2xl">👥</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Total Courses</p>
                <p className="text-3xl font-bold text-purple-600">{stats.totalCourses}</p>
              </div>
              <div className="bg-purple-100 p-3 rounded-full">
                <span className="text-2xl">📚</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Total Enrollments</p>
                <p className="text-3xl font-bold text-orange-600">{stats.totalEnrollments}</p>
              </div>
              <div className="bg-orange-100 p-3 rounded-full">
                <span className="text-2xl">📋</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Active</p>
                <p className="text-3xl font-bold text-green-600">{stats.activeEnrollments}</p>
              </div>
              <div className="bg-green-100 p-3 rounded-full">
                <span className="text-2xl">✅</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Completed</p>
                <p className="text-3xl font-bold text-teal-600">{stats.completedEnrollments}</p>
              </div>
              <div className="bg-teal-100 p-3 rounded-full">
                <span className="text-2xl">🎓</span>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <Link 
            to="/admin/courses"
            className="bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow"
          >
            <h3 className="text-xl font-bold mb-2">Manage Courses</h3>
            <p className="text-purple-100">Create, edit, and delete courses</p>
          </Link>

          <Link 
            to="/admin/students"
            className="bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow"
          >
            <h3 className="text-xl font-bold mb-2">Manage Students</h3>
            <p className="text-blue-100">View and manage student accounts</p>
          </Link>

          <Link 
            to="/admin/enrollments"
            className="bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow"
          >
            <h3 className="text-xl font-bold mb-2">Enrollments</h3>
            <p className="text-green-100">Track and manage enrollments</p>
          </Link>
        </div>

        {/* Recent Data */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Recent Courses */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-gray-900">Recent Courses</h2>
              <Link to="/admin/courses" className="text-blue-600 hover:underline text-sm">
                View All
              </Link>
            </div>
            {recentCourses.length > 0 ? (
              <div className="space-y-3">
                {recentCourses.map((course) => (
                  <div key={course.id} className="flex items-center justify-between py-2 border-b last:border-0">
                    <div>
                      <p className="font-medium text-gray-900">{course.title}</p>
                      <p className="text-sm text-gray-600">{course.credits} credits</p>
                    </div>
                    <span className="text-sm text-gray-500">
                      {course.current_enrollments} enrolled
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">No courses yet</p>
            )}
          </div>

          {/* Recent Students */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-gray-900">Recent Students</h2>
              <Link to="/admin/students" className="text-blue-600 hover:underline text-sm">
                View All
              </Link>
            </div>
            {recentStudents.length > 0 ? (
              <div className="space-y-3">
                {recentStudents.map((student) => (
                  <div key={student.id} className="flex items-center justify-between py-2 border-b last:border-0">
                    <div>
                      <p className="font-medium text-gray-900">{student.name}</p>
                      <p className="text-sm text-gray-600">{student.email}</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">No students yet</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
