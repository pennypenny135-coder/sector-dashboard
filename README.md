# 🇺🇸 US Sector ETF Dashboard

A dark-themed, real-time US Sector ETF dashboard built with Plotly.js — no backend required.

## 📊 Sectors Covered
| ETF | Sector |
|-----|--------|
| XLE | Energy |
| XLF | Financials |
| XLP | Consumer Staples |
| XLC | Communication Services |
| XLV | Health Care |
| XLRE | Real Estate |
| XLI | Industrials |
| XLY | Consumer Discretionary |
| XLK | Technology |
| XLU | Utilities |
| XLB | Materials |

## ✨ Features
- 📈 Price line + **10MA** (gold dashed) + **20MA** (red dotted)
- 📊 Volume bars on a secondary axis
- ⏱ Switch between **3-month** or **6-month** view
- 🔄 Manual Refresh button + **auto-refresh every 5 minutes**
- 🌑 Dark theme matching the reference dashboard style
- 🚀 Pure HTML/JS — zero server needed

## 🚀 Deployment

### Option 1 — GitHub Pages (Free)
1. Go to repo **Settings → Pages**
2. Source: `Deploy from a branch` → `main` / `/ (root)`
3. Save — your URL: `https://<username>.github.io/sector-dashboard/`

### Option 2 — Vercel (Free)
1. Import this repo at [vercel.com/new](https://vercel.com/new)
2. Framework: **Other** (static)
3. Deploy — done!

## 📦 Stack
- [Plotly.js](https://plotly.com/javascript/) — charts
- [Yahoo Finance API](https://finance.yahoo.com) (via allorigins CORS proxy) — data
- Pure HTML + Vanilla JS — no npm / no build step
