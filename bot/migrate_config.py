#!/usr/bin/env python3
"""
Migration script to convert old config file to new .env format.
"""

import os
from pathlib import Path

def migrate_config():
    """Migrate from old config file to .env file."""
    print("🔄 STFC Bot Configuration Migration")
    print("=" * 40)
    
    config_file = Path('config')
    env_file = Path('.env')
    
    # Check if old config exists
    if not config_file.exists():
        print("❌ No old 'config' file found.")
        print("Create a .env file manually using .env.example as template.")
        return False
    
    # Check if .env already exists
    if env_file.exists():
        print("⚠️  .env file already exists.")
        response = input("Overwrite existing .env file? (y/N): ")
        if response.lower() != 'y':
            print("Migration cancelled.")
            return False
    
    try:
        # Read old config
        with open(config_file, 'r') as f:
            lines = f.readlines()
        
        # Parse old config format
        config = {}
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split()
                if len(parts) >= 3:
                    bot_type = parts[0]
                    setting = parts[1]
                    value = parts[2]
                    
                    if bot_type not in config:
                        config[bot_type] = {}
                    config[bot_type][setting] = value
        
        # Create .env content
        env_content = "# Discord Bot Configuration\n"
        env_content += "# Migrated from old config file\n\n"
        
        # Handle DATA bot configuration
        if 'DATA' in config:
            if 'token' in config['DATA']:
                env_content += f"DISCORD_TOKEN={config['DATA']['token']}\n"
            if 'prefix' in config['DATA']:
                env_content += f"BOT_PREFIX={config['DATA']['prefix']}\n"
        
        # Handle test bot configuration
        if 'DATAtestsim' in config:
            if 'token' in config['DATAtestsim']:
                env_content += f"TEST_DISCORD_TOKEN={config['DATAtestsim']['token']}\n"
            if 'prefix' in config['DATAtestsim']:
                env_content += f"TEST_BOT_PREFIX={config['DATAtestsim']['prefix']}\n"
        
        # Add default values
        env_content += "\n# Default settings\n"
        env_content += "BOT_TYPE=DATA\n"
        env_content += "DATABASE_PATH=./utils/stfc_bot.db\n"
        env_content += "LOG_LEVEL=INFO\n"
        env_content += "DISCORD_INTENTS_MESSAGE_CONTENT=true\n"
        env_content += "DISCORD_INTENTS_GUILDS=true\n"
        env_content += "DISCORD_INTENTS_MEMBERS=true\n"
        
        # Write .env file
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print("✅ Migration completed successfully!")
        print(f"✅ Created .env file with {len(config)} bot configurations")
        
        # Show what was migrated
        for bot_type, settings in config.items():
            print(f"  - {bot_type}: {list(settings.keys())}")
        
        print("\n📝 Next steps:")
        print("1. Review the .env file and ensure tokens are correct")
        print("2. Run 'python test_setup.py' to verify setup")
        print("3. Run 'python startup.py' to start the bot")
        
        # Backup old config
        backup_file = Path('config.backup')
        config_file.rename(backup_file)
        print(f"📁 Old config file backed up as {backup_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def main():
    """Main migration function."""
    # Change to bot directory
    bot_dir = Path(__file__).parent
    os.chdir(bot_dir)
    
    success = migrate_config()
    if not success:
        print("\n💡 Manual setup:")
        print("1. Copy .env.example to .env")
        print("2. Edit .env with your bot token and settings")
        print("3. Run 'python test_setup.py' to verify")

if __name__ == "__main__":
    main()