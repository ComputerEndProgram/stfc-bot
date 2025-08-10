# STFC Discord Bot - Setup Instructions

## Overview
This is a Star Trek Fleet Command (STFC) Discord bot that provides alliance management, intel tracking, resource management, and war coordination features. The bot has been updated to work with Discord.py v2.x.

## Features
- **Alliance Registration & Management**: Register members, allies, and ambassadors
- **Intel Tracking**: Track allies, NAP agreements, KOS lists, wars, and ROE violations
- **Resource Management**: Interactive resource tracking system with STFC emojis
- **Administration**: Server setup, member management, and moderation tools
- **War Coordination**: Kill tracking and war points management
- **Help System**: Comprehensive command documentation

## Prerequisites
- Python 3.8 or higher
- Discord bot token
- Server admin permissions

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure the bot**:
   - Edit `bot/config` file
   - Replace `YOUR_DISCORD_BOT_TOKEN_HERE` with your actual Discord bot token
   - Replace `YOUR_DISCORD_USER_ID_HERE` with your Discord user ID (for admin commands)

3. **Run the bot**:
   ```bash
   cd bot
   python startup.py
   ```

## Configuration File Format
The `bot/config` file should contain:
```
# STFC Bot Configuration File - Replace placeholder values
DATA token YOUR_DISCORD_BOT_TOKEN_HERE
DATA prefix .
OWNER id YOUR_DISCORD_USER_ID_HERE
# DEV BOT CONFIG (optional)
DATAtestsim token YOUR_DEV_BOT_TOKEN_HERE
DATAtestsim prefix .
```

## Bot Setup in Discord

1. **Create a Discord Application**:
   - Go to https://discord.com/developers/applications
   - Create a new application
   - Go to the "Bot" section and create a bot
   - Copy the bot token to your config file

2. **Set Bot Permissions**:
   The bot needs the following permissions:
   - Read Messages
   - Send Messages
   - Manage Messages
   - Manage Roles
   - Manage Channels
   - Use External Emojis
   - Add Reactions
   - View Channel History

3. **Invite the Bot**:
   Use the OAuth2 URL generator in your Discord application to create an invite link with the required permissions.

## First Time Setup

1. **Run the setup command**:
   ```
   .setup YOUR_ALLIANCE_ID
   ```

2. **Configure your alliance settings** using the various setup commands available in `.help setup`

3. **Register members** using `.register` or admin registration commands

## Commands Overview

- `.help` - Show general help
- `.help admin` - Admin commands
- `.help setup` - Setup commands  
- `.help intel` - Intel commands
- `.help register` - Registration commands
- `.help resources` - Resource commands
- `.info` - Bot information

## Database
The bot uses SQLite for data storage. The database file (`stfc_bot.db`) will be created automatically in the bot directory.

## Custom Emojis
The bot includes STFC-themed emoji images in the `img/` directory. For best experience, upload these as custom emojis to your Discord server.

## Troubleshooting

- **Bot won't start**: Check that your token is correct in the config file
- **Cogs won't load**: Ensure all Python dependencies are installed
- **Commands not working**: Verify the bot has the required permissions
- **Database errors**: Delete `stfc_bot.db` to reset the database

## Support
For support or questions about this bot, refer to the help commands or check the GitHub repository.