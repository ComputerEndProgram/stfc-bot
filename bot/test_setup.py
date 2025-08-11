#!/usr/bin/env python3
"""
Test script to verify STFC bot setup without connecting to Discord.
Run this to check if your configuration is correct.
"""

import os
import sys
from pathlib import Path

def test_environment():
    """Test environment setup."""
    print("🔧 Testing Environment Setup...")
    
    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found. Copy .env.example to .env and configure it.")
        return False
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ .env file loaded successfully")
    except ImportError:
        print("❌ python-dotenv not installed. Run: pip install -r requirements.txt")
        return False
    
    # Check required environment variables
    required_vars = ['DISCORD_TOKEN', 'BOT_PREFIX', 'BOT_TYPE']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value == 'your_bot_token_here':
            missing_vars.append(var)
        else:
            print(f"✅ {var}: {'*' * min(10, len(value))}...")
    
    if missing_vars:
        print(f"❌ Missing or invalid environment variables: {', '.join(missing_vars)}")
        return False
    
    return True

def test_imports():
    """Test if all required imports work."""
    print("\n📦 Testing Python Dependencies...")
    
    try:
        import discord
        print(f"✅ discord.py version: {discord.__version__}")
        
        from discord.ext import commands
        print("✅ discord.ext.commands imported")
        
        import sqlite3
        print("✅ sqlite3 available")
        
        from dotenv import load_dotenv
        print("✅ python-dotenv available")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def test_database():
    """Test database setup."""
    print("\n🗄️ Testing Database Setup...")
    
    try:
        from utils.data_database import createAllianceTables
        from utils.db import get_connection
        
        # Test database connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT sqlite_version();")
        version = cursor.fetchone()[0]
        print(f"✅ SQLite version: {version}")
        conn.close()
        
        # Test table creation
        createAllianceTables()
        print("✅ Database tables created successfully")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    return True

def test_cogs():
    """Test if cogs can be imported."""
    print("\n🧩 Testing Bot Cogs...")
    
    cogs = ['registration', 'setup', 'administration', 'help', 'resources', 'intel', 'war']
    failed_cogs = []
    
    for cog in cogs:
        try:
            __import__(f'cogs.{cog}')
            print(f"✅ cogs.{cog}")
        except Exception as e:
            print(f"❌ cogs.{cog}: {e}")
            failed_cogs.append(cog)
    
    return len(failed_cogs) == 0

def main():
    """Main test function."""
    print("🤖 STFC Discord Bot Setup Test")
    print("=" * 40)
    
    # Change to bot directory
    bot_dir = Path(__file__).parent
    os.chdir(bot_dir)
    
    tests = [
        test_environment,
        test_imports,
        test_database,
        test_cogs
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! Your bot setup is ready.")
        print("Run 'python startup.py' to start the bot.")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()