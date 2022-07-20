# Script for backup your files

## Dependends
- OS: Linux
- dd
- zstd

## Periodic backup
- terminal: crontab -e. Add to end file: 1 1 1 * * /your_path_to_script/run.sh

## Properties
- Create file pass_server.py near run.sh and add variables:

-- sudo_password = "" // your root pass

-- telegram_bot_id = "" // your telegram bot id

-- telegram_chat_id = "" // yout chat id

- Add to run.sh path to your backup-script.py file

Script for create full backup with support images, arhives and compressions.
