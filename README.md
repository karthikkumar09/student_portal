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

-   [Docker](https://docs.docker.com/get-docker/): A containerization platform.
-   [Docker Compose](https://docs.docker.com/compose/install/): A tool for defining and running multi-container Docker applications.

## Getting Started

Follow these steps to get the project up and running on your local machine.

### 1. Clone the Repository

First, you need to clone the project's repository to your local machine. You can do this by running the following command in your terminal:

```bash
git clone https://github.com/your-username/student-portal.git
```

This will create a new directory named `student-portal` with all the project files.

### 2. Navigate to the Project Directory

Next, navigate to the newly created project directory:

```bash
cd student-portal
```

All subsequent commands should be run from this directory.

### 3. Run the Application

To start the application, run the following command:

```bash
docker-compose up
```

This command will:
-   Build the Docker images for each service (frontend, student-service, etc.). This might take a few minutes the first time you run it.
-   Start all the services in the correct order.
-   Display the logs from all the services in your terminal.

To run the application in the background (detached mode), you can use the `-d` flag:

```bash
docker-compose up -d
```

### 4. Access the Application

Once all the services are running, you can access the application in your web browser:

-   **Frontend:** [http://localhost](http://localhost)

The backend services are also accessible at the following addresses:

-   **Student Service:** [http://localhost:8001](http://localhost:8001)
-   **Course Service:** [http://localhost:8000](http://localhost:8000)
-   **Enrollment Service:** [http://localhost:8002](http://localhost:8002)

### 5. Login Credentials

#### Admin Login

A default admin user is created automatically when the `student-service` starts up for the first time. You can use the following credentials to log in as an administrator:

-   **Email:** `admin@example.com`
-   **Password:** `admin123`

**Important:** For production environments, it is highly recommended to change these default credentials immediately after the first login.

#### Student Login

There are no default student accounts. You will need to register a new student account through the application's frontend.

### 6. Stopping the Application

To stop the application and remove the containers, run the following command:

```bash
docker-compose down
```

This will stop and remove the containers, but it will not delete the data in the database, as it is stored in a Docker volume.

## Troubleshooting

-   **Port conflicts:** If you have another application running on port 80, 8000, 8001, 8002, or 27017, you will need to stop it before running this project. You can also change the ports in the `docker-compose.yml` file.

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
