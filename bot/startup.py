import discord
from discord.ext import commands
import sys, traceback, platform

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


# determine which bot to load up
botType = ''
# error checking
if len(sys.argv) > 2:
    print('**ERROR: Too many arguments. program takes at most one.\nexiting... ... ...')
    sys.exit()
    
# handle argument
if len(sys.argv) > 1:
    botType = sys.argv[1]
else:
    botType = 'DATA'


# Load configs
configFile = open('config')
configs = configFile.readlines()
config = {
    'DATA': {
        'token': (configs[1].split()[2]).split('\n')[0],  # DATA token YOUR_TOKEN -> [2] gets the token
        'prefix': (configs[2].split()[2]).split('\n')[0],  # DATA prefix . -> [2] gets the prefix
    },
    'DATAtestsim': {
        'token': (configs[5].split()[2]).split('\n')[0],  # DATAtestsim token YOUR_TOKEN -> [2] gets the token
        'prefix': (configs[6].split()[2]).split('\n')[0],  # DATAtestsim prefix . -> [2] gets the prefix
    },
}

bot = commands.Bot(command_prefix=config[botType]['prefix'], intents=intents)
bot.remove_command('help')  # Remove default help command before loading cogs

async def setup_hook():
    """Setup hook to load extensions."""
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print('{} loaded'.format(extension))
        except Exception as e:
            print('issue with',extension)
            traceback.print_exc()

bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    print('\n\n\nLogged in as {} (ID: {}) | Connected to {} servers'
        .format(bot.user, bot.user.id, len(bot.guilds))
    )
    print('-------'*18)
    print('Discord.py Version: {} | Python Version: {}'.format(discord.__version__, platform.python_version()))
    print('-------'*18)
    print('Use this link to invite {}:'.format(bot.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
    print('-------'*18)
    print('Support Discord Server: https://discord.gg/FNNNgqb')
    print('-------'*18)
    print('Successfully logged in and booted...! Use prefix: "'+config[botType]['prefix']+'".\n\n')

# Start your engines~~
bot.run(config[botType]['token'], bot=True, reconnect=True)

@bot.event
# special for ACE server
async def on_message(message):
    print(message.channel.name.lower())
    if message.channel.name.lower() == 'hit-list':
        channel = message.channel
        await channel.send('We see it all good!')
