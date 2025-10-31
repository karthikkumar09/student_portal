import { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { courseService, enrollmentService } from '../../services/api';

const BrowseCourses = () => {
  const { user } = useAuth();
  const [courses, setCourses] = useState([]);
  const [enrolledCourseIds, setEnrolledCourseIds] = useState(new Set());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [enrolling, setEnrolling] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [coursesRes, enrollmentsRes] = await Promise.all([
        courseService.getAllCourses(0, 100),
        enrollmentService.getStudentEnrollments(user.id)
      ]);
      
      setCourses(coursesRes.data.courses);
      
      // Create a set of enrolled course IDs
      const enrolled = new Set(
        enrollmentsRes.data.enrollments
          .filter(e => e.status === 'enrolled' || e.status === 'completed')
          .map(e => e.course_id)
      );
      setEnrolledCourseIds(enrolled);
    } catch (err) {
      setError('Failed to load courses');
    } finally {
      setLoading(false);
    }
  };

  const handleEnroll = async (courseId) => {
    setEnrolling(courseId);
    try {
      await enrollmentService.enrollInCourse({
        student_id: user.id,
        course_id: courseId,
      });
      
      // Refresh data
      await fetchData();
      alert('Successfully enrolled in course!');
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to enroll in course');
    } finally {
      setEnrolling(null);
    }
  };

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
          <h1 className="text-3xl font-bold text-gray-900">Browse Courses</h1>
          <p className="text-gray-600 mt-2">Discover and enroll in available courses</p>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {courses.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {courses.map((course) => {
              const isEnrolled = enrolledCourseIds.has(course.id);
              const isFull = course.max_students && course.current_enrollments >= course.max_students;
              
              return (
                <div key={course.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                  <div className="mb-4">
                    <h3 className="text-xl font-bold text-gray-900 mb-2">{course.title}</h3>
                    {course.instructor && (
                      <p className="text-sm text-gray-600">Instructor: {course.instructor}</p>
                    )}
                  </div>

                  {course.description && (
                    <p className="text-gray-600 mb-4 line-clamp-3">{course.description}</p>
                  )}

                  <div className="space-y-2 mb-4 text-sm">
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600">Credits:</span>
                      <span className="font-semibold text-blue-600">{course.credits}</span>
                    </div>
                    {course.duration_weeks && (
                      <div className="flex items-center justify-between">
                        <span className="text-gray-600">Duration:</span>
                        <span className="font-semibold">{course.duration_weeks} weeks</span>
                      </div>
                    )}
                    {course.max_students && (
                      <div className="flex items-center justify-between">
                        <span className="text-gray-600">Enrollment:</span>
                        <span className={`font-semibold ${isFull ? 'text-red-600' : 'text-green-600'}`}>
                          {course.current_enrollments}/{course.max_students}
                        </span>
                      </div>
                    )}
                  </div>

                  {isEnrolled ? (
                    <div className="bg-green-100 text-green-800 text-center py-3 rounded-md font-semibold">
                      ✓ Enrolled
                    </div>
                  ) : isFull ? (
                    <div className="bg-red-100 text-red-800 text-center py-3 rounded-md font-semibold">
                      Course Full
                    </div>
                  ) : (
                    <button
                      onClick={() => handleEnroll(course.id)}
                      disabled={enrolling === course.id}
                      className="w-full bg-blue-600 text-white py-3 rounded-md hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
                    >
                      {enrolling === course.id ? 'Enrolling...' : 'Enroll Now'}
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <p className="text-gray-500 text-lg">No courses available at the moment</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default BrowseCourses;
