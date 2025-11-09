#!/bin/bash
# RackSum Django Server Startup Script
set -e  # Exit on error

echo "=== RackSum Django Server Setup & Startup ==="

# Step 1: Check and create virtual environment if needed
if [ ! -d "venv" ]; then
    echo "🔧 Virtual environment not found. Creating new virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Step 2: Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Step 3: Check if dependencies are installed
if [ ! -f "venv/.dependencies_installed" ]; then
    echo "📦 Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    # Create marker file to skip this step on future runs
    touch venv/.dependencies_installed
    echo "✓ Dependencies installed"
else
    echo "✓ Dependencies already installed"
fi

# Step 4: Navigate to backend directory
cd backend

# Step 5: Run migrations to create/update database
echo "🗄️  Running database migrations..."
python manage.py migrate --no-input
echo "✓ Database ready"

# Step 6: Create superuser if needed (optional, for convenience)
# Uncomment the following lines if you want to auto-create a superuser
# echo "👤 Checking for superuser..."
# python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" 2>/dev/null || true

# Step 7: Start Django server
echo ""
echo "🚀 Starting Django server on port 3000..."
echo "================================================"
echo "   Server will be available at: http://localhost:3000"
echo "   Press Ctrl+C to stop the server"
echo "================================================"
echo ""
python manage.py runserver 3000
