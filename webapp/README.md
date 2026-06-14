# WebApp Documentation

## Overview

Telegram Mini App (WebApp) for Blackwood Poker Club. Built with vanilla HTML/CSS/JS — no frameworks needed. Opens inside Telegram's built-in browser when user clicks the button in the bot.

## Tech Stack

- **HTML5** — Semantic markup
- **CSS3** — Custom properties, flexbox, grid, animations
- **Vanilla JavaScript** — No frameworks, fetch API
- **Telegram WebApp JS** — `https://telegram.org/js/telegram-web-app.js`

## Pages

### 1. Home (Dashboard)

Shows the next upcoming tournament with:
- Tournament title and date/time
- Format tag (Texas Hold'em Classic)
- Seats bar (occupied / total)
- Registration button (or "SOLD OUT" if full)
- News section below

### 2. Tournaments

List of all tournaments:
- Past and upcoming
- Status badges (open / SOLD OUT / closed)
- Registration button per tournament
- Registration count display

### 3. Leaderboard

Ranked player list with:
- Position (1st, 2nd, 3rd highlighted with gold/silver/bronze)
- Player nickname
- Stats: games played, wins, finals
- Total points

### 4. Profile

Player personal page (requires Telegram login):
- Avatar placeholder + nickname
- Statistics: games, points, wins, finals
- Tournament history (last 10)

## Design System

### Color Palette (Blackwood Theme)

```css
--bg-deep: #0a0e1a;       /* Main background */
--bg-card: #141824;       /* Card backgrounds */
--gold: #c9a227;          /* Primary accent */
--gold-light: #e5c158;    /* Lighter gold */
--gold-dark: #a08020;     /* Darker gold */
--text: #e0e0e0;          /* Primary text */
--text-muted: #8a8f9e;    /* Secondary text */
--border: #2a3040;        /* Card borders */
--success: #2d8a4e;       /* Open status */
--danger: #8a2d2d;        /* Sold out status */
```

### Typography

- Primary font: Georgia / Times New Roman (serif) — premium casino feel
- Navigation: uppercase, letter-spacing 2px
- Gold text: #c9a227 with subtle shadow

### Visual Elements

- **Cards:** Rounded 12-16px, dark background, gold border accents
- **Buttons:** Gold gradient, uppercase, letter-spacing 1px
- **Seats bar:** Gold gradient fill showing occupancy
- **Podium:** Gold (1st), Silver (2nd), Bronze (3rd) circles
- **Status badges:** Color-coded pills with borders

## API Integration

The web app connects to the FastAPI backend:

```javascript
const API_URL = 'https://your-api-url.com';  // Set to your Render URL
```

All data is fetched via REST API endpoints (see `api/README.md` for full endpoint list).

## Telegram Integration

The app detects Telegram environment and extracts user data:

```javascript
let tg = window.Telegram?.WebApp;
if (tg) {
    tg.expand();  // Expand to full screen
    tg.ready();   // Signal ready state
    currentUser = tg.initDataUnsafe?.user;  // Get Telegram user data
}
```

**Note:** `initDataUnsafe` is only available when the app is opened from Telegram. If opened directly in a browser, the user will see a "Guest" profile and won't be able to register.

## Files

- `webapp/index.html` — Main HTML structure with all pages as sections
- `webapp/styles.css` — All styling (dark theme, gold accents, responsive)
- `webapp/app.js` — JavaScript logic: navigation, API calls, rendering
- `docs/*` — Copy of webapp files for GitHub Pages deployment

## Mobile-First

The app is designed for mobile (max-width: 480px). It works perfectly inside Telegram's in-app browser on iOS and Android.

```css
.app {
    max-width: 480px;
    margin: 0 auto;
}
```

## Deployment

The webapp is served via GitHub Pages from the `docs/` folder:

1. Push code to GitHub
2. Go to repo Settings → Pages
3. Source: Deploy from a branch → `main` → `/docs`
4. URL: `https://zazabag.github.io/poker/`

## Future Features

- Achievement gallery page with badge collection
- Admin panel for tournament management
- Live tournament tracker (who is still in, who busted)
- Season selector (monthly/quarterly leaderboards)
- Player search and comparison
- Tournament history with detailed results
- Share profile to Telegram stories
- Dark/light theme toggle
- Language switcher (EN/RU)
