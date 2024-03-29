"""
Discord Bot for Message Forwarding and Scheduling

This bot listens to messages in specific channels and forwards them to other
channels based on role mentions. It also supports scheduling message
forwarding at specified times.

Commands:
    - !set_channels: Set the channels to listen to and the role mappings
    for forwarding messages.
    - !help: Display the help message.

Author: Mohamed Elfadil
"""
import logging
from os.path import exists, join
from os import makedirs, getenv
import discord
from discord.ext import commands
import datetime
import asyncio
import pytz

# get username
user = getenv('USER') or getenv('LOGNAME')
# logging
log_directory = f'/home/{user}/RMFBot/bot_log'
log_file_name = 'bot_log.txt'
if not exists(log_directory):
    makedirs(log_directory)
log_file_path = join(log_directory, log_file_name)
# intents
intents = discord.Intents.default()
intents.typing = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
"""
Channels to listen to:
- 📢︱announcement
- 🎯︱challenges-tasks
- 📢︱scheduled-announcements
channel to role mapping:
- 📢︱fitness-announcements: Fitness Group
- 📢︱c-announcements: C Group
- 📢︱python-announcements: Python Group
- 📢︱javascript-announcements: JavaScript Group
- 📢︱sql-announcements: SQL Group
log channel name:
- 🗃︱log-scheduling
"""
channel_to_listen = ['📢︱announcement', '🎯︱challenges-tasks',
                     '📢︱scheduled-announcements']
channel_name_to_role_map = {
    '📢︱fitness-announcements': 'Fitness Group',
    '📢︱c-announcements': 'C Group',
    '📢︱python-announcements': 'Python Group',
    '📢︱javascript-announcements': 'JavaScript Group',
    '📢︱sql-announcements': 'SQL Group',
}
log_channel_name = '🗃︱log-scheduling'


def log_and_print(message):
    print(message)
    logging.info(message)


@bot.command(name='bot_help', help='Display the help message')
async def custom_help(ctx):
    """
    Display the help message.
    """
    help_message = """
    **Welcome to the  bot!**
    **Commands:**
    - `!set_channels`: Set the channels to listen to and the role mappings
                       for forwarding messages.
                       Note that the current list will be overwritten.
        1. List the channels to listen to, separated by commas.
        2. List the channel name and the role it will be mapped to
           The format is channel_name:role_name, separated by commas.
    - `!help`: Display the help message.
    """
    await ctx.send(help_message)


@bot.command(name='set_channels', help='Set channels and role mappings')
async def set_channels(ctx):
    """
    Set the channels to listen to and the role mappings
    for forwarding messages.
    """
    if ctx.author.guild_permissions.administrator:
        await ctx.send("Please provide the channels to listen"
                       + " to (separated by commas):")
        try:
            channels_input = await bot.wait_for('message', timeout=60.0,
                                                check=lambda m: m.author ==
                                                ctx.author and
                                                m.channel == ctx.channel)
            channel_to_listen.clear()
            channel_to_listen.extend([channel.strip() for channel in
                                      channels_input.content.split(',')])

            await ctx.send("Please provide the channel name to role mappings"
                           + " (in the format channel_name:role_name,"
                           + " separated by commas):")
            mappings_input = await bot.wait_for('message', timeout=60.0,
                                                check=lambda m: m.author ==
                                                ctx.author and
                                                m.channel == ctx.channel)
            channel_name_to_role_map.clear()
            for mapping in mappings_input.content.split(','):
                channel_name, role_name = map(str.strip, mapping.split(':'))
                channel_name_to_role_map[channel_name] = role_name

            await ctx.send("Channels and role mappings updated successfully.")
        except asyncio.TimeoutError:
            await ctx.send("Timeout. Please run the command again.")
    else:
        await ctx.send("You do not have the necessary permissions"
                       + " to run this command.")


@bot.event
async def on_message(message):
    """
    Listen to messages in the channels to listen to and
    forward them to the respective channels based on the role mentions.
    """
    if ((message.channel.name in channel_to_listen)
            and (message.author != bot.user)
            and (message.content != '')):
        mentioned_roles = [role.name for role in message.role_mentions]
        forwarding_tasks = []

        for channel_name, role in channel_name_to_role_map.items():
            log_and_print(f'Checking for role {role} in mentioned roles')
            if role in mentioned_roles:
                destination_channel = discord.utils.get(message.guild.channels,
                                                        name=channel_name)
                log_channel = discord.utils.get(message.guild.channels,
                                                name=log_channel_name)
                time_line = next((line.strip() for line in
                                  message.content.split('\n')
                                  if line.strip().startswith("TIME:")), None)

                if time_line:
                    time_str = time_line.strip().split("TIME:",
                                                       1)[1].split()[0].strip()
                    try:
                        scheduled_time_gmt = datetime.datetime.strptime(
                                                time_str, "%H:%M").time()
                        current_time_gmt = datetime.datetime.utcnow().time()
                        time_difference = datetime.datetime.combine(
                            datetime.date.today(),
                            scheduled_time_gmt) - datetime.datetime.combine(
                                datetime.date.today(),
                                current_time_gmt)
                        message_content_copy = message.content.replace(
                                                time_line, '')
                        # Schedule the forwarding task
                        log_and_print(f'Scheduling forwarding to ' +
                                      f'{destination_channel.name} ' +
                                      f'at {scheduled_time_gmt}')

                        forwarding_tasks.append(
                                    schedule_forwarding(
                                        destination_channel, log_channel,
                                        scheduled_time_gmt, message,
                                        message_content_copy,
                                        time_difference.seconds))
                    except ValueError:
                        m = f"Invalid time format in the TIME line: {time_str}"
                        print(m)
                        logging.exception(m)
                else:
                    # If time_line is not found, forward immediately
                    m = "TIME line not found. Forwarding immediately."
                    log_and_print(m)
                    await destination_channel.send(message.content)

        # Wait for all forwarding tasks to complete
        await asyncio.gather(*forwarding_tasks)

    await bot.process_commands(message)


async def schedule_forwarding(destination_channel, log_channel,
                              scheduled_time, message, message_content_copy,
                              delay):
    """
    Schedule the forwarding of the message to the destination channel
    at the scheduled time.
    """
    forwarded_message = f'{message_content_copy}'
    gmt = pytz.timezone('GMT')
    current_time_gmt = datetime.datetime.now(gmt)
    log_message = f'''Forwarded message
        From `{message.author.name}`
        To: `{destination_channel.name}`
        At: `{current_time_gmt.strftime("%d-%m-%Y %H:%M (GMT)")}`
        Set to arrive at: `{scheduled_time} (GMT)`'''
    await log_channel.send(log_message)
    logging.info(log_message)
    await asyncio.sleep(delay)
    await destination_channel.send(forwarded_message)


@bot.event
async def on_ready():
    """
    Print the bot's name when it is ready.
    """
    log_and_print(f'Logged in as {bot.user.name}')


def run_bot(token):
    """
    Run the bot with the given token.
    """
    bot.run(token)
