import { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { enrollmentService } from '../../services/api';

const MyCourses = () => {
  const { user } = useAuth();
  const [enrollments, setEnrollments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('all');
  const [dropModal, setDropModal] = useState(null);
  const [dropReason, setDropReason] = useState('');
  const [dropping, setDropping] = useState(false);

  useEffect(() => {
    fetchEnrollments();
  }, []);

  const fetchEnrollments = async () => {
    try {
      const response = await enrollmentService.getStudentEnrollments(user.id);
      setEnrollments(response.data.enrollments || []);
    } catch (err) {
      setError('Failed to load courses');
    } finally {
      setLoading(false);
    }
  };

  const handleDropCourse = async () => {
    if (!dropReason || dropReason.length < 10) {
      alert('Please provide a reason (at least 10 characters)');
      return;
    }

    setDropping(true);
    try {
      await enrollmentService.dropCourse({
        student_id: user.id,
        course_id: dropModal.course_id,
        drop_reason: dropReason,
      });
      
      // Refresh enrollments
      await fetchEnrollments();
      setDropModal(null);
      setDropReason('');
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to drop course');
    } finally {
      setDropping(false);
    }
  };

  const filteredEnrollments = enrollments.filter(e => {
    if (filter === 'all') return true;
    return e.status === filter;
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl">Loading courses...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Courses</h1>
          <p className="text-gray-600 mt-2">Manage your enrolled courses</p>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {/* Filter Tabs */}
        <div className="bg-white rounded-lg shadow-md p-4 mb-6">
          <div className="flex space-x-2">
            <button
              onClick={() => setFilter('all')}
              className={`px-4 py-2 rounded-md ${
                filter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              All ({enrollments.length})
            </button>
            <button
              onClick={() => setFilter('enrolled')}
              className={`px-4 py-2 rounded-md ${
                filter === 'enrolled' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Enrolled ({enrollments.filter(e => e.status === 'enrolled').length})
            </button>
            <button
              onClick={() => setFilter('completed')}
              className={`px-4 py-2 rounded-md ${
                filter === 'completed' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Completed ({enrollments.filter(e => e.status === 'completed').length})
            </button>
            <button
              onClick={() => setFilter('dropped')}
              className={`px-4 py-2 rounded-md ${
                filter === 'dropped' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Dropped ({enrollments.filter(e => e.status === 'dropped').length})
            </button>
          </div>
        </div>

        {/* Courses Grid */}
        {filteredEnrollments.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredEnrollments.map((enrollment) => (
              <div key={enrollment.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                <div className="mb-4">
                  <h3 className="text-xl font-bold text-gray-900 mb-2">{enrollment.course_title}</h3>
                  <div className="flex items-center justify-between text-sm text-gray-600">
                    <span>{enrollment.course_credits} Credits</span>
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      enrollment.status === 'completed' ? 'bg-green-100 text-green-800' :
                      enrollment.status === 'enrolled' ? 'bg-blue-100 text-blue-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {enrollment.status}
                    </span>
                  </div>
                </div>

                {enrollment.status === 'enrolled' && (
                  <div className="mb-4">
                    <div className="flex items-center justify-between text-sm mb-1">
                      <span className="text-gray-600">Progress</span>
                      <span className="font-semibold text-blue-600">{enrollment.progress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full transition-all" 
                        style={{ width: `${enrollment.progress}%` }}
                      ></div>
                    </div>
                  </div>
                )}

                <div className="text-sm text-gray-600 mb-4">
                  <p>Enrolled: {new Date(enrollment.enrollment_date).toLocaleDateString()}</p>
                  {enrollment.completion_date && (
                    <p>Completed: {new Date(enrollment.completion_date).toLocaleDateString()}</p>
                  )}
                  {enrollment.drop_date && (
                    <p>Dropped: {new Date(enrollment.drop_date).toLocaleDateString()}</p>
                  )}
                </div>

                {enrollment.status === 'enrolled' && (
                  <button
                    onClick={() => setDropModal(enrollment)}
                    className="w-full bg-red-500 text-white py-2 rounded-md hover:bg-red-600 transition-colors"
                  >
                    Drop Course
                  </button>
                )}

                {enrollment.status === 'dropped' && enrollment.drop_reason && (
                  <div className="text-sm text-gray-600 bg-gray-50 p-3 rounded">
                    <p className="font-semibold mb-1">Drop Reason:</p>
                    <p>{enrollment.drop_reason}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <p className="text-gray-500 text-lg">No courses found</p>
          </div>
        )}
      </div>

      {/* Drop Course Modal */}
      {dropModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Drop Course</h3>
            <p className="text-gray-600 mb-4">
              Are you sure you want to drop <strong>{dropModal.course_title}</strong>?
            </p>
            <textarea
              value={dropReason}
              onChange={(e) => setDropReason(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 mb-4"
              rows="4"
              placeholder="Please provide a reason for dropping this course (minimum 10 characters)"
              required
              minLength={10}
            />
            <div className="flex space-x-3">
              <button
                onClick={() => {
                  setDropModal(null);
                  setDropReason('');
                }}
                disabled={dropping}
                className="flex-1 bg-gray-300 text-gray-700 py-2 rounded-md hover:bg-gray-400 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleDropCourse}
                disabled={dropping}
                className="flex-1 bg-red-500 text-white py-2 rounded-md hover:bg-red-600 transition-colors disabled:bg-gray-400"
              >
                {dropping ? 'Dropping...' : 'Confirm Drop'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MyCourses;
