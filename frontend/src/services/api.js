import axios from 'axios';
import { config } from '../config';

const STUDENT_SERVICE_URL = config.STUDENT_SERVICE_URL;
const COURSE_SERVICE_URL = config.COURSE_SERVICE_URL;
const ENROLLMENT_SERVICE_URL = config.ENROLLMENT_SERVICE_URL;

// Create axios instances for each service
const studentAPI = axios.create({
  baseURL: STUDENT_SERVICE_URL,
});

const courseAPI = axios.create({
  baseURL: COURSE_SERVICE_URL,
});

const enrollmentAPI = axios.create({
  baseURL: ENROLLMENT_SERVICE_URL,
});

// Add token to requests if available
const addAuthToken = (config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
};

studentAPI.interceptors.request.use(addAuthToken);
courseAPI.interceptors.request.use(addAuthToken);
enrollmentAPI.interceptors.request.use(addAuthToken);

// Student Service APIs
export const studentService = {
  register: (data) => studentAPI.post('/students/register', data),
  login: (data) => studentAPI.post('/students/login', data),
  getProfile: () => studentAPI.get('/students/me'),
  updateProfile: (data) => studentAPI.put('/students/me', data),
  getStudentById: (id) => studentAPI.get(`/students/${id}`),
};

// Admin Service APIs
export const adminService = {
  login: (data) => studentAPI.post('/admin/login', data),
  getProfile: () => studentAPI.get('/admin/me'),
  getAllStudents: (skip = 0, limit = 100) => 
    studentAPI.get('/admin/students', { params: { skip, limit } }),
  getStudentDetails: (id) => studentAPI.get(`/admin/students/${id}`),
};

// Course Service APIs
export const courseService = {
  getAllCourses: (skip = 0, limit = 100) => 
    courseAPI.get('/courses', { params: { skip, limit } }),
  getCourse: (id) => courseAPI.get(`/courses/${id}`),
  createCourse: (data) => courseAPI.post('/courses', data),
  updateCourse: (id, data) => courseAPI.put(`/courses/${id}`, data),
  deleteCourse: (id) => courseAPI.delete(`/courses/${id}`),
};

// Enrollment Service APIs
export const enrollmentService = {
  enrollInCourse: (data) => enrollmentAPI.post('/enrollments', data),
  dropCourse: (data) => enrollmentAPI.post('/enrollments/drop', data),
  getStudentEnrollments: (studentId) => 
    enrollmentAPI.get(`/enrollments/student/${studentId}`),
  getCourseEnrollments: (courseId) => 
    enrollmentAPI.get(`/enrollments/course/${courseId}`),
  updateProgress: (enrollmentId, progress) => 
    enrollmentAPI.put(`/enrollments/${enrollmentId}/progress`, { progress }),
  markComplete: (data) => enrollmentAPI.post('/enrollments/complete', data),
  getEnrollmentCounts: () => enrollmentAPI.get('/enrollments/counts'),
  getStats: () => enrollmentAPI.get('/enrollments/stats'),
  getAllEnrollments: (skip = 0, limit = 100) => 
    enrollmentAPI.get('/enrollments', { params: { skip, limit } }),
};

export default {
  studentService,
  adminService,
  courseService,
  enrollmentService,
};
