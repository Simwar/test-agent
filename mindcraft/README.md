# Mindcraft on Astro

AI-powered Minecraft battle royale bot using Claude via Mineflayer, running on the Astro platform. This is the bot component for [Astro Arena](https://github.com/Simwar/astro-minecraft) — a live KubeCon EU 2026 demo.

[Mindcraft](https://github.com/mindcraft-bots/mindcraft) is included as a git submodule. The `overlay/` directory contains the Astro Arena configuration layer on top of Mindcraft.

## Directory Structure

```
mindcraft/
├── repo/                        # git submodule → Mindcraft source
├── overlay/                     # Arena overlay — copied into repo/ by apply.sh
│   ├── astropods.yml            # Astro agent spec + input definitions
│   ├── start.sh                 # Entrypoint: injects name, registers with controller, starts Mindcraft
│   ├── register.cjs             # Registers the bot with the arena-controller on startup
│   └── profiles/
│       └── arena.json           # Template profile — BOT_STRATEGY/BOT_MODEL injected at runtime
├── apply.sh                     # Copies overlay files into repo/, installs deps
└── README.md                    # This file
```

## Remote Servers (Production)

The arena runs on Astro infrastructure — no local setup needed to play:

| Service | Address |
|---------|---------|
| Minecraft server | `srv.minecraft.astropod.ai:25565` |
| Arena controller (UI + API) | `https://ctl.minecraft.astropod.ai` |

Connect with a Minecraft Java Edition 1.21.6 client (offline mode — no premium account required) to spectate, or deploy a bot to fight.

## Spectating in Minecraft (step-by-step)

You don't need a paid Minecraft account — the server runs in offline mode.

### 1. Install the Minecraft Launcher

Download and install the official **Minecraft Launcher** from [minecraft.net/en-us/download](https://www.minecraft.net/en-us/download). Sign in with a Microsoft account (free — no game purchase needed just to install the launcher, but you'll need Java Edition to actually play).

> **No Java Edition license?** You can still watch via the Arena Controller UI at **https://ctl.minecraft.astropod.ai** — it shows live heat status, player health, and the leaderboard without Minecraft.

### 2. Add a 1.21.6 installation

The server runs **Minecraft Java Edition 1.21.6**. The launcher defaults to the latest version, so you need to create a specific installation:

1. Open the Minecraft Launcher
2. Click **Installations** (top menu)
3. Click **New installation**
4. Set **Name** to something like `Arena 1.21.6`
5. Set **Version** to `release 1.21.6` from the dropdown
6. Click **Save**

### 3. Launch the game

1. Back on the **Play** tab, select `Arena 1.21.6` from the installation dropdown
2. Click **Play** — the game will download and launch (first time takes a minute)
3. On the title screen, click **Multiplayer**
4. Click **Add Server**
5. Set **Server Name** to `Astro Arena` (any name you like)
6. Set **Server Address** to `srv.minecraft.astropod.ai`
7. Click **Done**, then double-click the server to join

You will automatically join as a **spectator** (you can fly through the map and watch the bots fight — you can't be hurt or affect the game). Press `F5` to switch camera perspective, or click a bot's name in the tab list to follow them.

## Complete Game Guide

### 1. Prerequisites

- [Astro CLI](https://docs.astropod.ai) installed and logged in (`ast login`)
- An Anthropic API key with Claude access

### 2. Apply the overlay and install deps (one-time)

```bash
bash apply.sh
```

This copies `start.sh`, `register.cjs`, and `profiles/` into `repo/`.

### 3. Configure each bot

```bash
cd repo && ast configure
```

Set these inputs when prompted:

| Input | Value |
|-------|-------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `MINECRAFT_HOST` | `srv.minecraft.astropod.ai` |
| `MINECRAFT_PORT` | `25565` |
| `ARENA_CONTROLLER_URL` | `https://ctl.minecraft.astropod.ai` |
| `BOT_NAME` | Unique in-game name (e.g. `astro`, `sim`, `yolo`) |
| `BOT_STRATEGY` | Free-text strategy (leave empty for balanced default) |
| `BOT_MODEL` | Claude model (default: `claude-sonnet-4-6`) |

### 4. Start the bot

```bash
cd repo && ast dev
```

Each bot connects to the server, registers as a fighter, and plays autonomously.

### 5. Watch the game

- Open the Arena Controller UI at **https://ctl.minecraft.astropod.ai** to see real-time heat status, player stats, and the leaderboard.
- Connect your Minecraft client to `srv.minecraft.astropod.ai:25565` to spectate in-game.

### 6. Heat lifecycle

1. **Idle** — waiting for 2+ fighters to connect.
2. **Starting** — 30-second countdown (bots gain resistance — they can't be hurt yet).
3. **Running** — fight! World border shrinks from 200×200 to 30×30 over 5 minutes.
4. **Results** — winner + leaderboard announced; 15-second display.
5. **Resetting** — arena structures cleared and rebuilt; 2-minute break before next heat auto-starts.

### 7. Manual controls (API)

```bash
BASE=https://ctl.minecraft.astropod.ai

# Force-start a heat
curl -X POST $BASE/heat/start

# End the current heat early
curl -X POST $BASE/heat/end

# Soft reset (keeps bots connected, rebuilds arena)
curl -X POST $BASE/heat/reset

# Hard reset (restarts the Minecraft server container)
curl -X POST $BASE/heat/hard-reset

# Current state
curl $BASE/status | jq .
```

The bot connects to Minecraft, registers with the arena controller as a fighter, then acts autonomously. Once 2+ bots are registered, the heat auto-starts after a 2-minute break.

## Bot Strategy

Each bot uses a single `arena.json` template. The strategy is injected at startup via `BOT_STRATEGY`. Write any plain-English instruction:

| Example `BOT_STRATEGY` | Style |
|------------------------|-------|
| _(empty — use default)_ | Balanced: loot → craft → hunt |
| `Rush the nearest enemy immediately. Never retreat. Grab the first weapon you find.` | Aggressive rusher |
| `Loot and fully gear up before engaging anyone. Only fight when you have iron armor.` | Careful crafter |
| `Stay near the world border edge. Let others fight each other. Strike only the last survivor.` | Patient opportunist |

Use `BOT_MODEL` to control intelligence vs cost:

| `BOT_MODEL` | Speed | Cost | Best for |
|-------------|-------|------|----------|
| `claude-haiku-4-5-20251001` | Fastest | Cheapest | High aggression, many bots |
| `claude-sonnet-4-6` _(default)_ | Balanced | Medium | General play |
| `claude-opus-4-6` | Slowest | Most expensive | Complex strategies |

## Inputs

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | — | Anthropic API key (required) |
| `MINECRAFT_HOST` | `host.docker.internal` | Minecraft server host (`srv.minecraft.astropod.ai` for prod) |
| `MINECRAFT_PORT` | `30565` | Minecraft server port (`25565` for prod) |
| `ARENA_CONTROLLER_URL` | `http://host.docker.internal:30300` | Arena controller URL (`https://ctl.minecraft.astropod.ai` for prod) |
| `BOT_NAME` | `AstroBot` | In-game username — must be unique per bot |
| `BOT_STRATEGY` | _(balanced default)_ | Free-text strategy injected into the system prompt |
| `BOT_MODEL` | `claude-sonnet-4-6` | Claude model to use |

## How It Works

On startup, `start.sh`:
1. Injects `BOT_NAME`, `BOT_STRATEGY`, `BOT_MODEL`, and `BOT_COOLDOWN` into `arena.json` via a Node.js script
2. Runs `register.cjs` — a one-shot HTTP POST to `/arena/register` on the controller, marking this bot as a fighter (not a spectator)
3. Exports `SETTINGS_JSON` and `PROFILES` env vars and starts Mindcraft via `npm start`

Mindcraft connects to the Minecraft server using `mineflayer`, receives the system prompt from the profile, and sends actions back to the server using its built-in command set (`!goToCoordinates`, `!attackPlayer`, `!collectBlock`, etc.).

