import { useState, useEffect } from 'react';
import { adminService, enrollmentService } from '../../services/api';

const ManageStudents = () => {
  const [students, setStudents] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [studentEnrollments, setStudentEnrollments] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      const response = await adminService.getAllStudents(0, 100);
      setStudents(response.data.students);
    } catch (err) {
      setError('Failed to load students');
    } finally {
      setLoading(false);
    }
  };

  const fetchStudentDetails = async (studentId) => {
    try {
      const response = await enrollmentService.getStudentEnrollments(studentId);
      setStudentEnrollments(response.data);
      setSelectedStudent(students.find(s => s.id === studentId));
    } catch (err) {
      alert('Failed to load student details');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl">Loading students...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Manage Students</h1>
          <p className="text-gray-600 mt-2">View and manage student accounts</p>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Students List */}
          <div className="bg-white rounded-lg shadow-md">
            <div className="p-6 border-b">
              <h2 className="text-xl font-bold text-gray-900">All Students ({students.length})</h2>
            </div>
            {students.length > 0 ? (
              <div className="divide-y divide-gray-200 max-h-[600px] overflow-y-auto">
                {students.map((student) => (
                  <div
                    key={student.id}
                    onClick={() => fetchStudentDetails(student.id)}
                    className={`p-4 cursor-pointer hover:bg-gray-50 ${
                      selectedStudent?.id === student.id ? 'bg-blue-50' : ''
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium text-gray-900">{student.name}</p>
                        <p className="text-sm text-gray-600">{student.email}</p>
                      </div>
                      <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-12 text-center">
                <p className="text-gray-500">No students found</p>
              </div>
            )}
          </div>

          {/* Student Details */}
          <div className="bg-white rounded-lg shadow-md">
            <div className="p-6 border-b">
              <h2 className="text-xl font-bold text-gray-900">Student Details</h2>
            </div>
            {selectedStudent && studentEnrollments ? (
              <div className="p-6">
                <div className="mb-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-2">{selectedStudent.name}</h3>
                  <p className="text-gray-600">{selectedStudent.email}</p>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-3 gap-4 mb-6">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <p className="text-blue-600 text-2xl font-bold">{studentEnrollments.total_enrolled}</p>
                    <p className="text-blue-800 text-sm">Enrolled</p>
                  </div>
                  <div className="bg-green-50 p-4 rounded-lg">
                    <p className="text-green-600 text-2xl font-bold">{studentEnrollments.total_completed}</p>
                    <p className="text-green-800 text-sm">Completed</p>
                  </div>
                  <div className="bg-purple-50 p-4 rounded-lg">
                    <p className="text-purple-600 text-2xl font-bold">{studentEnrollments.total_credits_completed}</p>
                    <p className="text-purple-800 text-sm">Credits</p>
                  </div>
                </div>

                {/* Enrollments */}
                <div>
                  <h4 className="font-bold text-gray-900 mb-3">Enrollments</h4>
                  {studentEnrollments.enrollments.length > 0 ? (
                    <div className="space-y-3 max-h-96 overflow-y-auto">
                      {studentEnrollments.enrollments.map((enrollment) => (
                        <div key={enrollment.id} className="border border-gray-200 rounded-lg p-4">
                          <div className="flex items-center justify-between mb-2">
                            <p className="font-medium text-gray-900">{enrollment.course_title}</p>
                            <span className={`px-2 py-1 text-xs rounded-full ${
                              enrollment.status === 'completed' ? 'bg-green-100 text-green-800' :
                              enrollment.status === 'enrolled' ? 'bg-blue-100 text-blue-800' :
                              'bg-red-100 text-red-800'
                            }`}>
                              {enrollment.status}
                            </span>
                          </div>
                          <div className="text-sm text-gray-600 space-y-1">
                            <p>Credits: {enrollment.course_credits}</p>
                            <p>Progress: {enrollment.progress}%</p>
                            <p>Enrolled: {new Date(enrollment.enrollment_date).toLocaleDateString()}</p>
                            {enrollment.completion_date && (
                              <p>Completed: {new Date(enrollment.completion_date).toLocaleDateString()}</p>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-500 text-center py-4">No enrollments</p>
                  )}
                </div>
              </div>
            ) : (
              <div className="p-12 text-center">
                <p className="text-gray-500">Select a student to view details</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ManageStudents;
