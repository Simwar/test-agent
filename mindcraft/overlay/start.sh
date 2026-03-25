#!/bin/sh
# Builds SETTINGS_JSON from injected env vars and starts Mindcraft.
# Works identically in ast dev (local) and deployed on Astropods (prod).

MC_HOST="${MINECRAFT_HOST:-host.docker.internal}"
MC_PORT="${MINECRAFT_PORT:-30565}"
BOT_NAME="${BOT_NAME:-arena_bot}"
ARENA_URL="${ARENA_CONTROLLER_URL:-http://host.docker.internal:30300}"
DEFAULT_STRATEGY="Strategy:
1. Run to the nearest building (!goToCoordinates), loot the chest, craft weapons/armor.
2. Hunt all other bots with !attackPlayer(name). Check \$STATS for nearby players.
3. Stay near center (0,0) as the border shrinks.
4. If any action seems stuck, call !stop() immediately.
5. NEVER idle. NEVER use !stay."
export BOT_STRATEGY="${BOT_STRATEGY:-$DEFAULT_STRATEGY}"
echo "[arena] BOT_NAME=$BOT_NAME"
echo "[arena] BOT_STRATEGY=$BOT_STRATEGY"

# Inject name, strategy, and optional model override into the arena profile
node -e "
  const fs = require('fs');
  const f = './profiles/arena.json';
  const p = JSON.parse(fs.readFileSync(f, 'utf8'));
  p.name = process.env.BOT_NAME;
  p.conversing = p.conversing.replace('\$STRATEGY', process.env.BOT_STRATEGY);
  if (process.env.BOT_MODEL) p.model = process.env.BOT_MODEL;
  fs.writeFileSync(f, JSON.stringify(p));
"

# Register with the arena controller so we're treated as a fighter, not a spectator
node register.cjs

export PROFILES="[\"./profiles/arena.json\"]"
export SETTINGS_JSON=$(printf '{
  "auto_open_ui": false,
  "host": "%s",
  "port": %s,
  "minecraft_version": "1.21.6",
  "base_profile": "survival",
  "init_message": "Use !goal to begin immediately.",
  "max_commands": -1,
  "allow_insecure_coding": false,
  "chat_bot_messages": false,
  "narrate_behavior": false,
  "chat_ingame": false,
  "spawn_timeout": 60
}' "$MC_HOST" "$MC_PORT")

# Restart loop — if Mindcraft crashes or the bot disconnects fatally, restart within 1s
while true; do
  npm start
  echo "[arena] Mindcraft exited, restarting in 1s..."
  sleep 1
done
