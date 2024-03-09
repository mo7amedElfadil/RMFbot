#!/usr/bin/env bash
if [ -z "$1" ]; then
  echo "No argument supplied"
  exit 1
fi
if [ "$1" = "r" ]; then
	echo "starting bot"
	ssh -i "$path_to_ssh_key" "$USER@$IP" "pkill bot"
	COMMAND="bot $discordTOKEN"
elif [ "$1" = "k" ]; then
	echo "killing bot"
	COMMAND="pkill bot"
else
	echo "Invalid argument"
	exit 1
fi
IP=$SERVER3LB
USER=ubuntu
path_to_ssh_key=~/.ssh/id_rsa

ssh -i "$path_to_ssh_key" "$USER@$IP" "$COMMAND"

