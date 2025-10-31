#!/bin/bash

# Start script for Student Portal
# This script starts all services in separate terminal windows

echo "=================================="
echo "   Student Portal Startup"
echo "=================================="
echo ""

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "⚠️  MongoDB is not running. Please start MongoDB first:"
    echo "   Ubuntu/Debian: sudo systemctl start mongodb"
    echo "   macOS: brew services start mongodb-community"
    exit 1
fi

echo "✅ MongoDB is running"
echo ""

# Function to start a service in a new terminal
start_service() {
    SERVICE_NAME=$1
    PORT=$2
    DIR=$3
    
    echo "Starting $SERVICE_NAME on port $PORT..."
    
    # Different commands for different operating systems
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        osascript -e "tell application \"Terminal\" to do script \"cd $(pwd)/$DIR && source venv/bin/activate && uvicorn main:app --port $PORT --reload\""
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v gnome-terminal &> /dev/null; then
            gnome-terminal -- bash -c "cd $(pwd)/$DIR && source venv/bin/activate && uvicorn main:app --port $PORT --reload; exec bash"
        elif command -v xterm &> /dev/null; then
            xterm -e "cd $(pwd)/$DIR && source venv/bin/activate && uvicorn main:app --port $PORT --reload" &
        else
            echo "⚠️  Please manually run: cd $DIR && source venv/bin/activate && uvicorn main:app --port $PORT --reload"
        fi
    else
        echo "⚠️  Unsupported OS. Please manually start services."
        echo "   cd $DIR && source venv/bin/activate && uvicorn main:app --port $PORT --reload"
    fi
}

# Start backend services
start_service "Student Service" 8001 "backend/student-service"
sleep 2

start_service "Course Service" 8000 "backend/course-service"
sleep 2

start_service "Enrollment Service" 8002 "backend/enrollment-service"
sleep 2

# Start frontend
echo "Starting Frontend on port 5173..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    osascript -e "tell application \"Terminal\" to do script \"cd $(pwd)/frontend && npm run dev\""
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash -c "cd $(pwd)/frontend && npm run dev; exec bash"
    elif command -v xterm &> /dev/null; then
        xterm -e "cd $(pwd)/frontend && npm run dev" &
    else
        echo "⚠️  Please manually run: cd frontend && npm run dev"
    fi
fi

echo ""
echo "=================================="
echo "✅ All services starting..."
echo "=================================="
echo ""
echo "Access the application at:"
echo "  Frontend: http://localhost:5173"
echo ""
echo "API Documentation:"
echo "  Student Service: http://localhost:8001/docs"
echo "  Course Service: http://localhost:8000/docs"
echo "  Enrollment Service: http://localhost:8002/docs"
echo ""
echo "Default Admin Login:"
echo "  Email: admin@example.com"
echo "  Password: admin123"
echo ""
echo "Press Ctrl+C in each terminal to stop the services"
echo "=================================="
