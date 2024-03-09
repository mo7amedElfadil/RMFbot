#!/usr/bin/env bash
# This script is used to update the discord bot

FILE=bot
IP="$SERVER3LB"
USER="ubuntu"
path_to_ssh_key="$sshKEY"
scp -o StrictHostKeyChecking=no -i "$path_to_ssh_key" "$FILE" "$USER@$IP":/bin/

