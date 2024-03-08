import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.typing = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

channel_name_to_role_map = {
    'task-help': 'task-help',  # Replace with actual channel name and role name
    'session-planning': 'session-planning',  # Replace with actual channel name and role name
    # Add more channels and corresponding roles as needed
}

@bot.event
async def on_message(message):
    # Check if the message is in the 'general' channel
    if message.channel.name == 'general':
        # Check if the message contains roles
        mentioned_roles = [role.name for role in message.role_mentions]

        # Iterate through channel-role map
        for channel_name, role in channel_name_to_role_map.items():
            # Check if the mentioned roles include the specified role
            if role in mentioned_roles:
                # Find the destination channel by name
                destination_channel = discord.utils.get(message.guild.channels, name=channel_name)

                # Forward the message to the destination channel
                if destination_channel:
                    forwarded_message = f'Forwarded from {message.author.name}: {message.content}'
                    await destination_channel.send(forwarded_message)

    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

def run_bot():
    bot.run('MTIxNTczNDA2Mjc5OTY1MDkyNw.GDqS6Z.zWejHPOW7PmQKUVxPFYgZGYJDKRcBy4aC-qOEU')
