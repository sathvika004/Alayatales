#!/usr/bin/env python3
"""Test MongoDB Atlas connection"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    """Test MongoDB Atlas connection"""
    mongodb_uri = os.getenv('MONGODB_URI')
    db_name = os.getenv('DB_NAME', 'alayatales')
    
    print("🔍 Testing MongoDB Atlas connection...")
    print(f"📡 Connecting to: {mongodb_uri[:50]}...")
    
    try:
        # Create client with a short timeout for testing
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        
        # Test the connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        
        # List databases
        print("\n📚 Available databases:")
        for db in client.list_database_names():
            print(f"   - {db}")
        
        # Use the specified database
        db = client[db_name]
        print(f"\n🗄️ Using database: {db_name}")
        
        # List collections
        collections = db.list_collection_names()
        if collections:
            print(f"📂 Collections in {db_name}:")
            for collection in collections:
                print(f"   - {collection}")
        else:
            print(f"📂 No collections found in {db_name} (database is empty)")
        
        # Close connection
        client.close()
        print("\n🎉 Connection test successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Verify the connection string in .env file")
        print("3. Ensure IP whitelist in MongoDB Atlas includes your current IP")
        print("4. Check username and password are correct")
        return False

if __name__ == "__main__":
    test_connection()
