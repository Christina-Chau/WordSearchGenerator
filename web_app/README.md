# Word Search — Multiplayer Web App

A real-time multiplayer word search game built with Flask and Socket.IO. Up to 10 players join the same game, race to find words on a shared board, and earn points based on word length (**letters × 10**).
This part of the project was coded using Claude code.

---

## Features

- **Real-time multiplayer** — all players see the board update live as words are found
- **Up to 10 players** with unique colour coding
- **Three word sources** — built-in word bank, custom word list, or AI-generated words via OpenRouter
- **Flexible board sizes** — Easy (10×10), Medium (20×20), Hard (30×30), or any custom size from 5×5 to 50×50
- **Host controls** — the first player to join configures and starts the game; host role passes automatically if they leave
- **Accessible grid** — high-contrast light cells on a dark background; shared letters between words remain selectable

---

## Project Structure

```
web_app/
├── app.py              # Flask + Socket.IO server, game state, word validation
├── game_engine.py      # Placeholder (logic lives in wordsearch_generator/src/Game.py)
├── templates/
│   └── index.html      # Single-page frontend — join, lobby, game, game-over screens
├── requirements.txt    # Python dependencies
├── Procfile            # Start command for Railway / Render deployment
├── run.sh              # Convenience script for local development
└── README.md
```

The server imports `Game` and `WordBank` directly from `../wordsearch_generator/src/` — no code is duplicated.

---

## Prerequisites

- Python 3.10+
- The parent project's `.env` file at `WordSearchGenerator/.env` (only needed for AI word generation)

```
# WordSearchGenerator/.env
OPENROUTER_API_KEY=your_key_here
```

---

## Running Locally

```bash
cd WordSearchGenerator/web_app

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py
```

Or use the convenience script which does both steps:

```bash
bash run.sh
```

Open `http://localhost:5001` in your browser. Open multiple tabs to simulate multiple players.

---

## How to Play

1. **Enter your name** and click **Join Game**
2. The **first player to join is the host** — they choose board size and word source, then click **Start Game**
3. Other players see the lobby and wait for the host to start
4. On the game board, **click a starting letter**, then **click the ending letter** — the app draws a straight line between them and submits automatically
   - Valid directions: horizontal, vertical, and all four diagonals (forward or backward)
   - Words can share letters with already-found words — those cells remain clickable
5. **Points = number of letters × 10** — shown live on the scoreboard
6. Game ends when all words are found; the host can start a new round

### Word Sources

| Mode | Description |
|------|-------------|
| **Word Bank** | Pick from built-in categories (seasons, movies, animals, etc.) |
| **Custom List** | Paste your own words separated by commas or newlines (max 30, each ≤ board size) |
| **AI Generate** | Enter any topic — the server calls the OpenRouter API to generate thematic words |

---

## Sharing with Others

### Option A — Cloudflare Tunnel (quick, no account needed)

Run your server locally and expose it via a public URL:

```bash
# Terminal 1
python app.py

# Terminal 2
brew install cloudflared
cloudflared tunnel --url http://localhost:5001
```

Cloudflare prints a `https://random-name.trycloudflare.com` URL. Share it and anyone can join — link is active as long as your terminal is open.

### Option B — Railway (permanent hosted URL)

1. Push the full `WordSearchGenerator` repo to GitHub
2. Go to [railway.app](https://railway.app) → **New Project → Deploy from GitHub**
3. Set the **root directory** to `web_app`
4. Add environment variables in the Railway dashboard:
   ```
   OPENROUTER_API_KEY = your_key_here
   FLASK_ENV          = production
   ```
5. Railway detects the `Procfile` and deploys automatically

> **Note:** The `Procfile` runs `python app.py` directly using eventlet's built-in server (single process). This is required — game state is stored in memory, so multiple processes would each have isolated state and players would end up in separate games.