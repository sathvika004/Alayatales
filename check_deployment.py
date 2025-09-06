"""
Streamlit Deployment Checker
This script checks for common deployment issues before deploying to Streamlit Cloud
"""

import os
import sys
import json
from pathlib import Path
import importlib.util

def check_file_exists(filename, required=True):
    """Check if a file exists"""
    exists = Path(filename).exists()
    status = "✅" if exists else ("❌" if required else "⚠️")
    print(f"{status} {filename}: {'Found' if exists else 'Missing'}")
    return exists

def check_requirements():
    """Check requirements.txt for common issues"""
    print("\n📦 Checking requirements.txt...")
    
    if not check_file_exists("requirements.txt"):
        return False
    
    issues = []
    with open("requirements.txt", "r") as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            # Check for local file references
            if "file://" in line or "./" in line or "/" in line and not "==" in line:
                issues.append(f"  ❌ Local file reference found: {line}")
            
            # Check for git references
            if "git+" in line:
                issues.append(f"  ⚠️ Git reference found (may not work on Streamlit Cloud): {line}")
    
    if issues:
        print("  Issues found:")
        for issue in issues:
            print(issue)
        return False
    else:
        print("  ✅ No issues found in requirements.txt")
        return True

def check_imports():
    """Check if all imports in Python files can be resolved"""
    print("\n🐍 Checking Python imports...")
    
    python_files = ["app.py", "models.py", "auth.py", "temple_pages.py"]
    import_issues = []
    
    for file in python_files:
        if Path(file).exists():
            with open(file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if line.startswith("import ") or line.startswith("from "):
                    # Extract module name
                    if line.startswith("import "):
                        module = line.split()[1].split(".")[0]
                    else:
                        module = line.split()[1].split(".")[0]
                    
                    # Skip relative imports and built-in modules
                    if module in ["streamlit", "pymongo", "PIL", "pandas", "plotly", 
                                  "dotenv", "os", "sys", "datetime", "typing", "base64",
                                  "io", "hashlib", "secrets", "bson", "models", "auth", 
                                  "temple_pages"]:
                        continue
                    
                    # Check if module can be imported
                    spec = importlib.util.find_spec(module)
                    if spec is None:
                        import_issues.append(f"  ⚠️ {file}:{i} - Cannot find module: {module}")
    
    if import_issues:
        print("  Import issues found:")
        for issue in import_issues:
            print(issue)
        return False
    else:
        print("  ✅ All imports look good")
        return True

def check_secrets():
    """Check for secrets configuration"""
    print("\n🔐 Checking secrets configuration...")
    
    secrets_needed = []
    env_exists = check_file_exists(".env", required=False)
    
    # Check for MongoDB URI usage
    with open("models.py", "r", encoding="utf-8") as f:
        content = f.read()
        if "MONGODB_URI" in content:
            secrets_needed.append("MONGODB_URI")
        if "DB_NAME" in content:
            secrets_needed.append("DB_NAME")
    
    if secrets_needed:
        print(f"  ℹ️ Your app uses these environment variables: {', '.join(secrets_needed)}")
        print("  📝 For Streamlit Cloud deployment:")
        print("     1. Go to your app settings on Streamlit Cloud")
        print("     2. Add these as secrets in TOML format:")
        print("     ```")
        print("     MONGODB_URI = \"your-mongodb-connection-string\"")
        print("     DB_NAME = \"alayatales\"")
        print("     ```")
    
    # Create .streamlit/secrets.toml template if it doesn't exist
    secrets_dir = Path(".streamlit")
    secrets_file = secrets_dir / "secrets.toml"
    
    if not secrets_file.exists():
        print("\n  Creating .streamlit/secrets.toml template...")
        secrets_dir.mkdir(exist_ok=True)
        
        with open(secrets_file, "w") as f:
            f.write("""# Streamlit Secrets Configuration
# This file is for local development only
# On Streamlit Cloud, add these secrets in the app settings

# MongoDB Configuration
MONGODB_URI = "mongodb://localhost:27017/"
DB_NAME = "alayatales"

# Optional: MongoDB Atlas connection
# MONGODB_URI = "mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority"
""")
        print("  ✅ Created .streamlit/secrets.toml template")
    
    return True

def check_streamlit_config():
    """Check Streamlit configuration"""
    print("\n⚙️ Checking Streamlit configuration...")
    
    config_exists = check_file_exists(".streamlit/config.toml", required=False)
    
    if config_exists:
        print("  ✅ Streamlit config found")
    else:
        print("  ℹ️ No config.toml found (using defaults)")
    
    return True

def check_mongodb_fallback():
    """Check if app has proper MongoDB connection fallback"""
    print("\n🔄 Checking MongoDB connection fallback...")
    
    with open("models.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    has_fallback = "serverSelectionTimeoutMS" in content
    has_error_handling = "except" in content and "MongoDB" in content
    
    if has_fallback and has_error_handling:
        print("  ✅ MongoDB connection has timeout and error handling")
    else:
        print("  ⚠️ Consider adding timeout and better error handling for MongoDB connection")
    
    return True

def check_file_uploads():
    """Check file upload configuration"""
    print("\n📤 Checking file upload configuration...")
    
    with open("temple_pages.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    if "file_uploader" in content:
        print("  ✅ File uploads are used")
        print("  ℹ️ Note: Streamlit Cloud has a default 200MB limit for file uploads")
        
        # Check if images are stored as base64
        if "base64" in content:
            print("  ✅ Images are converted to base64 (good for MongoDB storage)")
        else:
            print("  ⚠️ Consider converting images to base64 for database storage")
    
    return True

def create_deployment_files():
    """Create necessary deployment files if missing"""
    print("\n📝 Creating/updating deployment files...")
    
    # Create a simple Procfile if it doesn't exist
    if not Path("Procfile").exists():
        with open("Procfile", "w") as f:
            f.write("web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0\n")
        print("  ✅ Created Procfile")
    
    # Create runtime.txt if it doesn't exist
    if not Path("runtime.txt").exists():
        with open("runtime.txt", "w") as f:
            f.write("python-3.9.18\n")
        print("  ✅ Created runtime.txt")
    
    # Create .gitignore if it doesn't exist
    if not Path(".gitignore").exists():
        with open(".gitignore", "w") as f:
            f.write("""# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# Environment
.env
.env.local
.streamlit/secrets.toml

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Database
*.db
*.sqlite
*.sqlite3

# Uploaded files
uploads/
temp/
""")
        print("  ✅ Created .gitignore")
    
    return True

def check_dependencies_compatibility():
    """Check if dependencies are compatible with Streamlit Cloud"""
    print("\n🔍 Checking dependency compatibility...")
    
    with open("requirements.txt", "r") as f:
        requirements = f.read()
    
    issues = []
    
    # Check Python version compatibility
    if "numpy==1.24.3" in requirements:
        print("  ✅ NumPy version is compatible")
    
    if "pandas==2.1.3" in requirements:
        print("  ✅ Pandas version is compatible")
    
    if "streamlit==1.28.2" in requirements:
        print("  ✅ Streamlit version specified")
    
    # Check for pymongo with srv support
    if "pymongo" in requirements:
        if "pymongo[srv]" in requirements or "dnspython" in requirements:
            print("  ✅ MongoDB Atlas support is included (dnspython)")
        else:
            print("  ⚠️ For MongoDB Atlas, ensure dnspython is in requirements.txt")
    
    return True

def main():
    """Main deployment checker"""
    print("=" * 60)
    print("🛕 Alayatales - Streamlit Deployment Checker")
    print("=" * 60)
    
    all_good = True
    
    # Run all checks
    all_good &= check_requirements()
    all_good &= check_imports()
    all_good &= check_secrets()
    all_good &= check_streamlit_config()
    all_good &= check_mongodb_fallback()
    all_good &= check_file_uploads()
    all_good &= check_dependencies_compatibility()
    all_good &= create_deployment_files()
    
    print("\n" + "=" * 60)
    if all_good:
        print("✅ Your app is ready for Streamlit deployment!")
        print("\n📋 Deployment Checklist:")
        print("1. Push your code to GitHub")
        print("2. Connect your GitHub repo to Streamlit Cloud")
        print("3. Add secrets (MONGODB_URI, DB_NAME) in Streamlit Cloud settings")
        print("4. Deploy and monitor the logs")
        print("\n💡 Tips:")
        print("- Use MongoDB Atlas for cloud database (free tier available)")
        print("- Monitor your app's resource usage in Streamlit Cloud")
        print("- Check logs if any issues occur during deployment")
    else:
        print("⚠️ Some issues were found. Please review the output above.")
        print("Fix the issues and run this checker again.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
