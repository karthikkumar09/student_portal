# Student Portal

This is a full-stack student portal application that allows students to register, log in, and enroll in courses. Admins can manage students and courses.

## Features

-   **Student Authentication:** Students can register and log in to the portal.
-   **Course Management:** Admins can create, read, update, and delete courses.
-   **Enrollment System:** Students can enroll in and drop courses.
-   **Progress Tracking:** Admins can track and update student progress in courses.
-   **Admin Dashboard:** Admins have a separate dashboard to manage students and courses.
-   **Microservices Architecture:** The backend is built with a microservices architecture, with separate services for students, courses, and enrollments.

## Technologies Used

-   **Frontend:** React, Vite, Tailwind CSS
-   **Backend:** FastAPI (Python), MongoDB
-   **Containerization:** Docker, Docker Compose

## Prerequisites

Before you begin, ensure you have the following installed on your system:

-   [Docker](https://docs.docker.com/get-docker/)
-   [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

To get the project up and running, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/student-portal.git
    cd student-portal
    ```

2.  **Run the application:**

    ```bash
    docker-compose up
    ```

    This command will build the Docker images for each service and start the application. The frontend will be available at `http://localhost`.

## Services

The application is composed of the following services:

-   **`student-service`:** Manages student authentication and profiles.
-   **`course-service`:** Manages course information.
-   **`enrollment-service`:** Manages student enrollments in courses.
-   **`frontend`:** The React-based user interface.
-   **`mongodb`:** The database for the application.

## API Endpoints

### Student Service (`/students`)

-   `POST /students/register`: Register a new student.
-   `POST /students/login`: Log in a student.
-   `GET /students/me`: Get the profile of the currently logged-in student.
-   `PUT /students/me`: Update the profile of the currently logged-in student.
-   `GET /students/{student_id}`: Get a student by ID (for internal service communication).
-   `DELETE /students/{student_id}`: Delete a student (admin only).

### Admin Service (`/admin`)

-   `POST /admin/login`: Log in an admin.
-   `GET /admin/me`: Get the profile of the currently logged-in admin.
-   `GET /admin/students`: Get all students (admin only).
-   `GET /admin/students/{student_id}`: Get a student by ID (admin only).

### Course Service (`/courses`)

-   `POST /courses`: Create a new course (admin only).
-   `GET /courses`: Get all courses.
-   `GET /courses/{course_id}`: Get a specific course.
-   `PUT /courses/{course_id}`: Update a course (admin only).
-   `DELETE /courses/{course_id}`: Delete a course (admin only).

### Enrollment Service (`/enrollments`)

-   `POST /enrollments`: Enroll a student in a course.
-   `POST /enrollments/drop`: Drop a course.
-   `PUT /enrollments/{enrollment_id}/progress`: Update course progress (admin only).
-   `POST /enrollments/complete`: Mark a course as completed (admin only).
-   `GET /enrollments/student/{student_id}`: Get all enrollments for a student.
-   `GET /enrollments/course/{course_id}`: Get all enrollments for a course (admin only).
-   `GET /enrollments/course/{course_id}/count`: Get the enrollment count for a course.
-   `GET /enrollments/counts`: Get enrollment counts for all courses.
-   `GET /enrollments/stats`: Get overall enrollment statistics (admin only).
-   `GET /enrollments`: Get all enrollments (admin only).

## Project Structure

```
student-portal/
├── backend/
│   ├── course-service/
│   ├── enrollment-service/
│   └── student-service/
├── frontend/
├── docker-compose.yml
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request.
