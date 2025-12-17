# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FIDE API is a Python web scraper that exposes FIDE (World Chess Federation) chess player data as a REST API. It scrapes data from ratings.fide.com and serves it via FastAPI.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn src.api:app --reload

# Run with Docker
docker compose up -d
```

The API documentation is available at `/docs` when the server is running.

## Architecture

### Layer Structure

```
src/
├── api.py                      # FastAPI app with 3 endpoints
└── scraper/
    ├── fide_scraper.py         # HTTP fetching layer (requests to FIDE)
    └── functions/              # HTML parsing layer (BeautifulSoup)
        ├── top_players.py      # Parses top players table
        ├── player_info.py      # Parses player profile page
        ├── player_history.py   # Parses rating history table
        └── utils.py            # Date conversion utilities
```

### Data Flow

1. **API Layer** (`src/api.py`): FastAPI endpoints receive requests
2. **Fetcher Layer** (`src/scraper/fide_scraper.py`): Makes HTTP requests to ratings.fide.com
3. **Parser Layer** (`src/scraper/functions/`): BeautifulSoup extracts data from HTML

### API Endpoints

- `GET /top_players/?limit=100&history=false` - Top rated players
- `GET /player_info/?fide_id=<id>&history=false` - Player profile
- `GET /player_history/?fide_id=<id>` - Rating history

### Key Implementation Details

- Uses `ORJSONResponse` for fast JSON serialization
- CORS is fully open (all origins allowed)
- The `history=true` parameter triggers additional HTTP requests per player
- Deployed to Vercel (see `vercel.json`)
