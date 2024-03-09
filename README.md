# RMFbot
**Discord Bot for Message Forwarding and Scheduling**

_Author: Mohamed Elfadil_

## Table of Contents
- [Description](#description)
- [Installing](#installing)
- [Usage](#usage)
	- [Remote execution](#remote-execution)
	- [Local execution](#local-execution)
    - [Commands](#commands)
- [Contributing](#contributing)
- [License](#license)


## Description

This bot listens to messages in specific channels and forwards them to other
channels based on role mentions. It also supports scheduling message
forwarding at specified times.


**The current features are:**

1. `Message forwarding` to mapped channels. Example of mapping:
Channels to listen to:
- :loudspeaker:︱announcement
- :dart:︱challenges-tasks
- :loudspeaker:︱scheduled-announcements
channel to role mapping:
- :loudspeaker:︱fitness-announcements: Fitness Group
- :loudspeaker:︱c-announcements: C Group
- :loudspeaker:︱python-announcements: Python Group
- :loudspeaker:︱javascript-announcements: JavaScript Group
- :loudspeaker:︱sql-announcements: SQL Group
log channel name:
- :card_box:︱log-scheduling

however you can change that if you  want by using the `!set_channel' command. use !help & !bot_help for more information on the formatting.

2. `Message scheduling`. Using `TIME:` in the beginning of a line initiates a scheduled message forwarding where all messages will be forwarded at the same time. Please note that the time format must be in GMT for synchronization. Although you can schedule from any channel, it might be best to use:
 - :loudspeaker:︱scheduled-announcements

and set it as a private channel. 

3. `Schedule Logging`. Any scheduled message will be logged in the logging channel. The info will be: Author, destination, time sent, time scheduled. eg:

```
Forwarded message
        From <sender's username>
        To: :loudspeaker:︱c-announcements
        At: 09-03-2024 15:17 (GMT)
        Set to arrive at: 15:18:00 (GMT)
```


## Installing

[Invite Link](https://discord.com/oauth2/authorize?client_id=1215734062799650927&permissions=2183991393344&scope=bot) 
to add the bot to your server. For full functionality its best to give it administrator role.

Clone the repository
```
git clone https://github.com/mo7amedElfadil/RMFbot.git
```

Add these lines to your `bashrc` or `zshrc`, otherwise just add them to the start of the bot function in the `exec_bot.sh` file. The discordTOKEN is recommended even for local execution/hosting but the others are only for remote execution:
```
export discordTOKEN="<Your discord API token>"
export SERVER3LB="<your server ip>"
export sshKEY="<path to ssh private-key on your local device>"
```
add these to the start of the bot function in the `exec_bot.sh` file:
```
USER="<the username of the machine hosting the bot>"
```

## Usage

### Remote execution
Usage:
```
./exec_bot.sh [r/run/k/kill/t/tail/l/log]
```
To remotely update the bot, use the `update_bot.sh` script
```
./update_bot.sh
```

### Local execution
```
./bot $discordTOKEN
or
./bot <discord API key>
```
Once the bot script is running either remotely or locally, check your discord server. The bot should appear as online.


### Commands
- `!set_channels`: Set the channels to listen to and the role mappings
				   for forwarding messages.
				   Note that the current list will be overwritten.
	1. List the channels to listen to, separated by commas.
	2. List the channel name and the role it will be mapped to
	   The format is channel_name:role_name, separated by commas.
- `!help`: Display the help message.
- `!bot_help`: Display the bot help message.
- `!set_log_channel`: set the log channel for the server.
- `!get_log_channel`: get the log channel for the server.
- `!get_channels`: get the channels and role mappings for the server.


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](LICENSE)
