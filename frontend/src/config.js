export const config = {
  STUDENT_SERVICE_URL: import.meta.env.VITE_STUDENT_SERVICE_URL || 'http://localhost:8001',
  COURSE_SERVICE_URL: import.meta.env.VITE_COURSE_SERVICE_URL || 'http://localhost:8000',
  ENROLLMENT_SERVICE_URL: import.meta.env.VITE_ENROLLMENT_SERVICE_URL || 'http://localhost:8002',
};
