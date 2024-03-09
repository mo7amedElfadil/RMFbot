import discord
from discord.ext import commands
import datetime
import asyncio
import pytz

intents = discord.Intents.default()
intents.typing = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

channel_name_to_role_map = {
    'task-help': 'task-help',
    'session-planning': 'session-planning',
}

@bot.event
async def on_message(message):
    if message.channel.name == 'general':
        mentioned_roles = [role.name for role in message.role_mentions]
        forwarding_tasks = []

        for channel_name, role in channel_name_to_role_map.items():
            print(f'Checking for role {role} in mentioned roles')
            if role in mentioned_roles:
                destination_channel = discord.utils.get(message.guild.channels, name=channel_name)
                log_channel = discord.utils.get(message.guild.channels, name="logging")
                time_line = next((line.strip() for line in message.content.split('\n') if line.startswith("TIME:")), None)

                if time_line:
                    time_str = time_line.strip().split("TIME:", 1)[1].split()[0].strip()
                    try:
                        scheduled_time_gmt = datetime.datetime.strptime(time_str, "%H:%M").time()
                        current_time_gmt = datetime.datetime.utcnow().time()
                        time_difference = datetime.datetime.combine(
                            datetime.date.today(),
                            scheduled_time_gmt) - datetime.datetime.combine(
                                datetime.date.today(),
                                current_time_gmt)
                        message_content_copy = message.content.replace(time_line, '')
                        # Schedule the forwarding task
                        print(f'Scheduling forwarding to {destination_channel.name} at {scheduled_time_gmt}')

                        forwarding_tasks.append(schedule_forwarding(destination_channel, log_channel,
                                                                    scheduled_time_gmt, message, message_content_copy,
                                                                    time_difference.seconds))
                    except ValueError:
                        print("Invalid time format in the TIME line.")

        # Wait for all forwarding tasks to complete
        await asyncio.gather(*forwarding_tasks)

    await bot.process_commands(message)

async def schedule_forwarding(destination_channel, log_channel, scheduled_time, message, message_content_copy, delay):
    await asyncio.sleep(delay)
    forwarded_message = f'{message_content_copy}'
    gmt = pytz.timezone('GMT')
    current_time_gmt = datetime.datetime.now(gmt)
    await destination_channel.send(forwarded_message)
    await log_channel.send(f'Forwarded message\nFrom `{message.author.name}`\nTo: `{destination_channel.name}`\nAt: `{current_time_gmt.strftime("%d-%m-%Y %H:%M")}`\nSet to arrive at: `{scheduled_time}`')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

def run_bot(token):
    bot.run(token)
