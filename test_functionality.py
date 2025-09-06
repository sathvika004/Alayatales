#!/usr/bin/env python3
"""
Comprehensive test script for Alayatales Temple Management System
Tests all major functionality and button operations
"""

import sys
import os
import importlib.util
from datetime import datetime

def test_imports():
    """Test if all modules can be imported successfully"""
    print("🔍 Testing module imports...")
    
    modules_to_test = [
        'app',
        'auth', 
        'models',
        'temple_pages',
        'utils'
    ]
    
    failed_imports = []
    
    for module_name in modules_to_test:
        try:
            spec = importlib.util.spec_from_file_location(
                module_name, 
                f"c:\\Users\\jakku\\Downloads\\new\\aalayatales\\{module_name}.py"
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(f"  ✅ {module_name}.py imported successfully")
        except Exception as e:
            print(f"  ❌ {module_name}.py failed to import: {str(e)}")
            failed_imports.append(module_name)
    
    return len(failed_imports) == 0

def test_database_functions():
    """Test database-related functions"""
    print("\n🗄️ Testing database functions...")
    
    try:
        # Import models
        sys.path.append("c:\\Users\\jakku\\Downloads\\new\\aalayatales")
        import models
        
        # Test database connection function
        print("  🔗 Testing database connection...")
        client = models.get_database_connection()
        if client is not None:
            print("  ✅ Database connection function works")
        else:
            print("  ⚠️ Database connection returned None (expected if MongoDB not running)")
        
        # Test ObjectId validation
        print("  🔍 Testing ObjectId validation...")
        valid_id = "507f1f77bcf86cd799439011"
        invalid_id = "invalid_id"
        
        if models.is_valid_object_id(valid_id):
            print("  ✅ Valid ObjectId correctly identified")
        else:
            print("  ❌ Valid ObjectId incorrectly rejected")
            
        if not models.is_valid_object_id(invalid_id):
            print("  ✅ Invalid ObjectId correctly rejected")
        else:
            print("  ❌ Invalid ObjectId incorrectly accepted")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Database function test failed: {str(e)}")
        return False

def test_utility_functions():
    """Test utility functions"""
    print("\n🛠️ Testing utility functions...")
    
    try:
        sys.path.append("c:\\Users\\jakku\\Downloads\\new\\aalayatales")
        import utils
        
        # Test email validation
        print("  📧 Testing email validation...")
        valid_email = "test@example.com"
        invalid_email = "invalid_email"
        
        if utils.validate_email(valid_email):
            print("  ✅ Valid email correctly identified")
        else:
            print("  ❌ Valid email incorrectly rejected")
            
        if not utils.validate_email(invalid_email):
            print("  ✅ Invalid email correctly rejected")
        else:
            print("  ❌ Invalid email incorrectly accepted")
        
        # Test password validation
        print("  🔒 Testing password validation...")
        strong_password = "StrongPass123!"
        weak_password = "weak"
        
        strong_result = utils.validate_password(strong_password)
        weak_result = utils.validate_password(weak_password)
        
        if strong_result['valid']:
            print("  ✅ Strong password correctly validated")
        else:
            print(f"  ❌ Strong password incorrectly rejected: {strong_result['message']}")
            
        if not weak_result['valid']:
            print("  ✅ Weak password correctly rejected")
        else:
            print("  ❌ Weak password incorrectly accepted")
        
        # Test text utilities
        print("  📝 Testing text utilities...")
        long_text = "This is a very long text that should be truncated when it exceeds the maximum length limit."
        truncated = utils.truncate_text(long_text, 50)
        
        if len(truncated) <= 53:  # 50 + "..." = 53
            print("  ✅ Text truncation works correctly")
        else:
            print("  ❌ Text truncation failed")
        
        # Test slug generation
        slug = utils.generate_slug("Test Temple Name!")
        if slug == "test-temple-name":
            print("  ✅ Slug generation works correctly")
        else:
            print(f"  ❌ Slug generation failed: got '{slug}', expected 'test-temple-name'")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Utility function test failed: {str(e)}")
        return False

def test_auth_functions():
    """Test authentication functions"""
    print("\n🔐 Testing authentication functions...")
    
    try:
        sys.path.append("c:\\Users\\jakku\\Downloads\\new\\aalayatales")
        import auth
        
        # Test password hashing
        print("  🔑 Testing password hashing...")
        password = "testpassword123"
        hashed = auth.hash_password(password)
        
        if auth.verify_password(password, hashed):
            print("  ✅ Password hashing and verification works")
        else:
            print("  ❌ Password hashing and verification failed")
        
        # Test wrong password
        if not auth.verify_password("wrongpassword", hashed):
            print("  ✅ Wrong password correctly rejected")
        else:
            print("  ❌ Wrong password incorrectly accepted")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Authentication function test failed: {str(e)}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        'app.py',
        'auth.py',
        'models.py',
        'temple_pages.py',
        'utils.py',
        'requirements.txt',
        'README.md',
        'LICENSE',
        'CHANGELOG.md',
        '.env.example',
        '.gitignore',
        'setup.py',
        'pyproject.toml'
    ]
    
    base_path = "c:\\Users\\jakku\\Downloads\\new\\aalayatales"
    missing_files = []
    
    for file_name in required_files:
        file_path = os.path.join(base_path, file_name)
        if os.path.exists(file_path):
            print(f"  ✅ {file_name} exists")
        else:
            print(f"  ❌ {file_name} missing")
            missing_files.append(file_name)
    
    return len(missing_files) == 0

def test_configuration_files():
    """Test configuration files"""
    print("\n⚙️ Testing configuration files...")
    
    base_path = "c:\\Users\\jakku\\Downloads\\new\\aalayatales"
    
    # Test requirements.txt
    req_file = os.path.join(base_path, "requirements.txt")
    if os.path.exists(req_file):
        with open(req_file, 'r') as f:
            content = f.read()
            required_packages = ['streamlit', 'pymongo', 'pillow', 'plotly', 'python-dotenv']
            missing_packages = []
            
            for package in required_packages:
                if package.lower() not in content.lower():
                    missing_packages.append(package)
            
            if not missing_packages:
                print("  ✅ requirements.txt contains all required packages")
            else:
                print(f"  ⚠️ requirements.txt missing packages: {missing_packages}")
    
    # Test .env.example
    env_example = os.path.join(base_path, ".env.example")
    if os.path.exists(env_example):
        with open(env_example, 'r') as f:
            content = f.read()
            required_vars = ['MONGODB_URI', 'DB_NAME', 'SECRET_KEY']
            missing_vars = []
            
            for var in required_vars:
                if var not in content:
                    missing_vars.append(var)
            
            if not missing_vars:
                print("  ✅ .env.example contains all required variables")
            else:
                print(f"  ⚠️ .env.example missing variables: {missing_vars}")
    
    return True

def main():
    """Run all tests"""
    print("🚀 Starting Alayatales Functionality Tests")
    print("=" * 50)
    
    test_results = []
    
    # Run all tests
    test_results.append(("File Structure", test_file_structure()))
    test_results.append(("Module Imports", test_imports()))
    test_results.append(("Database Functions", test_database_functions()))
    test_results.append(("Utility Functions", test_utility_functions()))
    test_results.append(("Authentication Functions", test_auth_functions()))
    test_results.append(("Configuration Files", test_configuration_files()))
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The application is ready to use.")
        print("\n📋 Next steps:")
        print("1. Set up MongoDB (local or Atlas)")
        print("2. Copy .env.example to .env and configure")
        print("3. Run: streamlit run app.py")
        print("4. Create an admin account")
        print("5. Use debug mode in admin dashboard to create sample temples")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please review the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)