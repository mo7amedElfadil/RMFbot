#!/usr/bin/env bash
function bot()
{
	if [ -z "$1" ]; then
		echo "Usage: ./exec_bot.sh [r/run/k/kill/t/tail/l/log]"
		exit 1
	fi
	IP=$SERVER3LB
	USER=ubuntu
	# r or run
	# k or kill
	if [ "$1" = "r" ] || [ "$1" = "run" ]; then
		echo "starting bot"
		ssh -i "$sshKEY" "$USER@$IP" "pkill bot"
		COMMAND="bot $discordTOKEN"
	elif [ "$1" = "k" ] || [ "$1" = "kill" ]; then
		echo "killing bot"
		COMMAND="pkill bot"
	elif [ "$1" = 't' ] || [ "$1" = 'tail' ]; then
		echo "reading tail of bot log"
		COMMAND="tail -f /home/$USER/RMFBot/bot_log/bot_log.txt"
	elif [ "$1" = 'l' ] || [ "$1" = 'log' ]; then
		echo "reading bot log file"
		COMMAND="less /home/$USER/RMFBot/bot_log/bot_log.txt"
	else
		echo "Invalid argument"
		exit 1
	fi


	ssh -i "$sshKEY" "$USER@$IP" "$COMMAND"
}

bot "$1"

