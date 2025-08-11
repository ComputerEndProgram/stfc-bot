# STFC Discord Bot - Modernized & Fixed!

A Star Trek Fleet Command (STFC) Discord bot for alliance management, updated for Discord.py 2.x with modern configuration and database handling.

## ✅ Fixed Issues

- **Discord.py 2.x Compatibility**: Fixed `add_reaction()` calls and updated all API usage
- **Database Initialization**: Proper database schema creation with error handling
- **Guild Context Issues**: Fixed NoneType errors in message handlers
- **Modern Configuration**: Switched from plain text config to secure .env file system
- **Proper Error Handling**: Added comprehensive error handling throughout

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Copy the example environment file and configure it:
```bash
cp .env.example .env
```

Edit `.env` with your bot credentials:
```env
DISCORD_TOKEN=your_bot_token_here
BOT_PREFIX=$
BOT_TYPE=DATA
```

### 3. Run the Bot
```bash
cd bot
python startup.py
```

## 🔧 Configuration

### Environment Variables (.env file)

| Variable | Default | Description |
|----------|---------|-------------|
| `DISCORD_TOKEN` | - | Your Discord bot token (required) |
| `BOT_PREFIX` | `$` | Command prefix |
| `BOT_TYPE` | `DATA` | Bot type (DATA or DATAtestsim) |
| `TEST_DISCORD_TOKEN` | - | Test bot token (optional) |
| `TEST_BOT_PREFIX` | `$` | Test bot prefix (optional) |
| `DATABASE_PATH` | `./utils/stfc_bot.db` | Database file path |

### Legacy Config Migration

If you have an old `config` file, create a `.env` file with:
```env
DISCORD_TOKEN=your_token_from_line_2_of_config
BOT_PREFIX=your_prefix_from_line_3_of_config
```

## 📊 Database

The bot uses SQLite with automatic schema creation including:
- **Server Settings**: Alliance configuration per Discord server
- **Alliance Management**: Multi-alliance support with hierarchies
- **Role Permissions**: Granular Discord role-based permissions
- **War Tracking**: Kill counts and war point management
- **Intelligence**: Alliance relationships and player tracking
- **Resources**: STFC resource location database
- **ROE Management**: Rules of engagement violation tracking

Database is automatically initialized on first startup.

## 🎮 Bot Features

### Core Cogs
- **Registration**: User registration and role management
- **Setup**: Server configuration and alliance setup
- **Administration**: Server management commands
- **Help**: Interactive help system
- **Resources**: STFC resource location tracking
- **Intel**: Alliance intelligence and diplomacy
- **War**: War point tracking and kill counts

### Key Commands
- `$help` - Show available commands
- `$setup` - Configure server settings
- `$register` - Register users with alliance roles
- `$resources <query>` - Search resource locations
- `$intel` - View alliance intelligence
- `$war` - War statistics and leaderboards

## 🔐 Security

- Bot tokens are stored in `.env` files (not committed to git)
- Database files are excluded from version control
- Proper input validation and error handling
- Guild context validation to prevent DM errors

## 🛠️ Development

### File Structure
```
bot/
├── startup.py          # Main bot entry point
├── .env                # Environment configuration (create this)
├── cogs/               # Bot command modules
│   ├── registration.py
│   ├── setup.py
│   ├── administration.py
│   ├── help.py
│   ├── resources.py
│   ├── intel.py
│   └── war.py
└── utils/              # Utility modules
    ├── db.py           # Database operations
    ├── data_database.py# Database schema
    ├── functions.py    # Helper functions
    └── constants.py    # Bot constants
```

### Requirements
- Python 3.8+
- discord.py 2.5.2+
- python-dotenv 1.0.0+

## 📝 Migration from Old Version

### Automatic Migration
If you have an old `config` file, use the migration script:
```bash
cd bot
python migrate_config.py
```

### Manual Migration
1. **Backup your old config**: Save any important settings
2. **Create .env file**: Use `.env.example` as template
3. **Set your token**: Add your Discord bot token to `.env`
4. **Test setup**: Run `python test_setup.py` to verify
5. **Run the new bot**: Database will be automatically created
6. **Reconfigure servers**: Use `$setup` to configure each server

### Verify Setup
Before running the bot, test your configuration:
```bash
cd bot
python test_setup.py
```

This will check:
- ✅ Environment variables are properly configured
- ✅ All Python dependencies are installed
- ✅ Database can be created and accessed
- ✅ All bot cogs can be imported

## 🆘 Troubleshooting

### Common Issues

**"Improper token has been passed"**
- Check your `.env` file has correct `DISCORD_TOKEN`
- Ensure token has no extra spaces or quotes

**"Database query error: no such table"**
- Delete any old database files
- Restart bot to auto-create new schema

**"AttributeError: 'NoneType' object has no attribute 'id'"**
- Fixed in this version - update to latest code

**Permission errors**
- Ensure bot has necessary Discord permissions
- Check role hierarchy in Discord server settings
