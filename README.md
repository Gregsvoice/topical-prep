# Topical Prep — Music & Showbiz Radio News Desk

## What's new
- Radio-readable, source-attributed **10-second headline reads** with one-click copy.
- A **30-second buzz** combining three sourced headlines, with source links.
- UK/USA and category filters, mobile layout and fullscreen studio mode.
- Scheduled 08:00 and 12:00 **Europe/London** updates, including BST/GMT.
- Automatic website polling every five minutes for the new edition.

**Editorial safeguard:** These are headline-based scripts, not independently verified article summaries. They intentionally do not add details not contained in headlines. Read the original articles before broadcasting. The buzz is approximately 30 seconds depending on headline length and presenter pace. Sources may be unavailable or indexed late.

## Publish to GitHub Pages
1. Create a GitHub repository (e.g. `topical-prep`). Upload `index.html`, `update.py`, `news.json`, and `.github/workflows/update.yml` preserving the folders.
2. In GitHub **Settings → Pages**, set **Deploy from a branch**, `main`, `/ (root)`.
3. In **Actions**, enable workflows if prompted; run **Refresh Topical Prep** manually once. Ensure Actions has read/write repository permission if commits fail.
4. Visit `https://YOUR-USERNAME.github.io/topical-prep/` on your laptop, phone and studio computer. Use Studio mode for the studio screen.

**Important:** This ZIP does not deploy anything automatically. GitHub Actions runs on a best-effort schedule and can be delayed. The hourly workflow checks the UK local clock and only updates during the 08:00 and 12:00 hours; if GitHub skips that window the edition may be missed. To guarantee precise publication times, use a dedicated always-on scheduler instead. GitHub Pages is public. No API key is needed; headlines come from Google News RSS queries for Capital FM, BBC Entertainment, Official Charts, KIIS FM, Billboard, Variety and People. Some results may redirect through Google News.

## Local test
Run `python update.py` with internet access, then `python -m http.server 8000`, and open `http://localhost:8000`.
