#!/bin/bash
# Bot health check and restart script
BOT_DIR="/Users/macintosheesh/Documents/Kimi/Workspaces/Покер клуб/blackwood-poker-bot"
LOG_FILE="$BOT_DIR/bot.log"

# Check if bot is running
if ! pgrep -f "bot.main" > /dev/null; then
    echo "$(date): Bot not running, restarting..." >> "$LOG_FILE"
    cd "$BOT_DIR"
    nohup python3 -m bot.main >> "$LOG_FILE" 2>&1 &
    echo "$(date): Bot restarted with PID $!" >> "$LOG_FILE"
else
    echo "$(date): Bot is alive" >> "$LOG_FILE"
fi
