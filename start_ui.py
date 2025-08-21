#!/usr/bin/env python3
"""
ParGaMD UI Startup Script
Checks dependencies and starts the web interface
"""

import sys
import subprocess
import importlib.util
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependency(module_name, package_name=None):
    """Check if a Python module is available"""
    if package_name is None:
        package_name = module_name
    
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"❌ Missing dependency: {package_name}")
        return False
    print(f"✅ {package_name} is available")
    return True

def install_dependencies():
    """Install missing dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_dependencies():
    """Check all required dependencies"""
    print("🔍 Checking dependencies...")
    
    required_deps = [
        ("flask", "Flask"),
        ("flask_socketio", "Flask-SocketIO"),
        ("paramiko", "Paramiko"),
        ("jinja2", "Jinja2"),
        ("werkzeug", "Werkzeug")
    ]
    
    missing_deps = []
    for module_name, package_name in required_deps:
        if not check_dependency(module_name, package_name):
            missing_deps.append(package_name)
    
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        response = input("Would you like to install them now? (y/n): ")
        if response.lower() in ['y', 'yes']:
            return install_dependencies()
        else:
            print("Please install the missing dependencies manually:")
            print("pip install -r requirements.txt")
            return False
    
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', 'templates', 'static/js']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def main():
    """Main startup function"""
    print("🚀 ParGaMD UI Startup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Check if UI files exist
    required_files = ['ui_app.py', 'templates/index.html', 'static/js/main.js']
    missing_files = []
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing required files: {', '.join(missing_files)}")
        print("Please ensure all UI files are present in the current directory")
        sys.exit(1)
    
    print("\n✅ All checks passed!")
    print("\n🌐 Starting ParGaMD UI...")
    print("📱 Open your browser and navigate to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the UI
    try:
        from ui_app import app, socketio
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 ParGaMD UI stopped")
    except Exception as e:
        print(f"\n❌ Failed to start UI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
