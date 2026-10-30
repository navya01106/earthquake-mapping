# Earthquake Live Map

A beginner-friendly Python desktop app that pulls the last 24 hours of earthquakes from the public USGS feed and plots them on a world map. Stronger quakes get bigger circles, and the map refreshes itself every minute.

<!-- Add a screenshot or GIF: upload it to the repo and use ![Screenshot](screenshot.png) -->

## Features
- Live data from the USGS earthquake feed (no API key needed)
- Circle size and colour scale with magnitude (yellow, orange, red)
- Hover over a circle to see magnitude, place, depth and time
- Auto-refresh every 60 seconds
- Standard library only, nothing to install

## How it works
1. **Fetch:** `urllib` downloads the GeoJSON feed and `json` parses it.
2. **Map:** longitude (-180 to 180) and latitude (90 to -90) are converted into screen pixels.
3. **Draw:** one circle per quake on a `tkinter` canvas, sized and coloured by magnitude.
4. **Poll:** `root.after()` re-runs the fetch on a timer to keep the map live.

## Run it
```
python earthquake_map.py
```
Requires Python 3 with tkinter. On Linux, install it with `sudo apt install python3-tk`.

## Ideas for next steps
- Switch the feed to `all_hour` or `all_week`
- Show only quakes of magnitude 2.5 or higher
- Colour circles by depth
- Add real coastlines with matplotlib and cartopy

## Data
Earthquake data from the [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/earthquakes/feed/).

## About this project
Built with AI-assisted coding tools while learning real-time APIs. I handled running, testing and extending it.
