import os
import sys
import discord
from discord.ext import commands
import traceback
import platform
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database initialization
from utils.data_database import createAllianceTables

# Set up intents for discord.py v2
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# COGS
initial_extensions = [
    'cogs.registration',
    'cogs.setup',
    'cogs.administration',
    'cogs.help',
    'cogs.resources',
    'cogs.intel',
    'cogs.war'
]

def get_bot_config():
    """Get bot configuration from environment variables."""
    bot_type = os.getenv('BOT_TYPE', 'DATA')
    
    if bot_type == 'DATAtestsim':
        token = os.getenv('TEST_DISCORD_TOKEN')
        prefix = os.getenv('TEST_BOT_PREFIX', '$')
    else:
        token = os.getenv('DISCORD_TOKEN')
        prefix = os.getenv('BOT_PREFIX', '$')
    
    if not token:
        print(f"ERROR: No token found for bot type '{bot_type}'")
        if bot_type == 'DATAtestsim':
            print("Set TEST_DISCORD_TOKEN in your .env file")
        else:
            print("Set DISCORD_TOKEN in your .env file")
        sys.exit(1)
    
    return token, prefix, bot_type

class StfcBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.remove_command('help')  # Remove default help command before loading cogs
    
    async def setup_hook(self):
        """Setup hook to load extensions and initialize database."""
        # Initialize database tables
        try:
            createAllianceTables()
            print("Database tables initialized successfully.")
        except Exception as e:
            print(f"Error initializing database: {e}")
            traceback.print_exc()
        
        # Load extensions
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
                print(f'{extension} loaded')
            except Exception as e:
                print(f'Failed to load extension {extension}')
                traceback.print_exc()

    async def on_ready(self):
        """Event triggered when bot is ready."""
        print('\n\n\nLogged in as {} (ID: {}) | Connected to {} servers'
            .format(self.user, self.user.id, len(self.guilds))
        )
        print('-------'*18)
        print('Discord.py Version: {} | Python Version: {}'.format(discord.__version__, platform.python_version()))
        print('-------'*18)
        print('Use this link to invite {}:'.format(self.user.name))
        print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(self.user.id))
        print('-------'*18)
        print('Support Discord Server: https://discord.gg/FNNNgqb')
        print('-------'*18)
        print('Successfully logged in and booted...! Use prefix: "'+self.command_prefix+'".\n\n')

def main():
    """Main function to start the bot."""
    # Parse command line arguments
    bot_type_arg = None
    if len(sys.argv) > 2:
        print('**ERROR: Too many arguments. program takes at most one.\nexiting... ... ...')
        sys.exit()
    elif len(sys.argv) == 2:
        bot_type_arg = sys.argv[1]
        os.environ['BOT_TYPE'] = bot_type_arg
    
    # Get configuration
    token, prefix, bot_type = get_bot_config()
    
    # Create and run bot
    bot = StfcBot(command_prefix=prefix, intents=intents)
    
    try:
        bot.run(token, reconnect=True)
    except discord.LoginFailure:
        print("ERROR: Invalid token provided. Please check your .env file.")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()