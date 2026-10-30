"""
Earthquake Live Map
-------------------
Pulls the last 24 hours of earthquakes from the free USGS feed (no API key
needed) and draws them on a world map. Stronger quakes get bigger circles.
The map refreshes itself every minute.

Only uses Python's standard library, so there is nothing to pip install.
Run it with:  python earthquake_map.py
"""

import json
import tkinter as tk
import urllib.request
from datetime import datetime

# ---------- Settings you can play with ----------
URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
WIDTH, HEIGHT = 1000, 500      # map is 2:1 because longitude spans 360, latitude 180
REFRESH_SECONDS = 60           # how often we ask the API for fresh data
SIZE_PER_MAGNITUDE = 2.5       # bigger number = bigger circles


# ---------- Step 1: get the data (fetch) ----------
def fetch_quakes():
    """Download the earthquake feed and return a list of quakes."""
    with urllib.request.urlopen(URL, timeout=10) as response:
        data = json.load(response)      # turn the JSON text into Python dicts/lists
    return data["features"]


# ---------- Step 2: lat/lon -> screen pixels (mapping) ----------
def to_screen(lon, lat):
    """
    Longitude runs from -180 (left) to +180 (right).
    Latitude runs from +90 (top) to -90 (bottom).
    We squeeze those ranges into our window's pixel size.
    """
    x = (lon + 180) / 360 * WIDTH
    y = (90 - lat) / 180 * HEIGHT       # flipped: screen y grows downward!
    return x, y


def color_for(magnitude):
    """Pick a color based on how strong the quake is."""
    if magnitude < 3:
        return "#ffd43b"    # yellow: small
    if magnitude < 5:
        return "#ff922b"    # orange: medium
    return "#e03131"        # red: strong


# ---------- Step 3: draw everything ----------
def draw_grid():
    """Draw latitude/longitude lines so the map has some structure."""
    for lon in range(-180, 181, 30):
        x, _ = to_screen(lon, 0)
        canvas.create_line(x, 0, x, HEIGHT, fill="#1e3a5f")
    for lat in range(-90, 91, 30):
        _, y = to_screen(0, lat)
        # the equator (lat 0) gets a brighter line
        canvas.create_line(0, y, WIDTH, y, fill="#3b6ea5" if lat == 0 else "#1e3a5f")


def draw_quakes(quakes):
    """Draw one circle per earthquake."""
    # Sort so the biggest are drawn first and small ones end up on top.
    quakes = [q for q in quakes if q["properties"]["mag"] is not None]
    quakes.sort(key=lambda q: q["properties"]["mag"], reverse=True)

    for quake in quakes:
        props = quake["properties"]
        lon, lat, depth = quake["geometry"]["coordinates"]
        mag = props["mag"]

        x, y = to_screen(lon, lat)
        radius = max(2, mag * SIZE_PER_MAGNITUDE)    # never smaller than 2px

        circle = canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill=color_for(mag), outline="white",
        )

        # Text to show when the mouse hovers over this circle
        when = datetime.fromtimestamp(props["time"] / 1000).strftime("%H:%M")
        text = f"M {mag:.1f}  |  {props['place']}  |  depth {depth:.0f} km  |  {when}"
        canvas.tag_bind(circle, "<Enter>", lambda event, t=text: info.set(t))
        canvas.tag_bind(circle, "<Leave>", lambda event: info.set("Hover over a circle"))

    return quakes


# ---------- Step 4: polling (refresh on a timer) ----------
def refresh():
    """Fetch new data, redraw the map, then schedule ourselves to run again."""
    try:
        quakes = fetch_quakes()
        canvas.delete("all")            # wipe the old drawing
        draw_grid()
        shown = draw_quakes(quakes)
        now = datetime.now().strftime("%H:%M:%S")
        status.set(f"{len(shown)} earthquakes in the last 24h  |  updated {now}")
    except Exception as error:          # no internet, API down, etc.
        status.set(f"Could not fetch data: {error}")

    # Run refresh() again after REFRESH_SECONDS (the "polling" part).
    root.after(REFRESH_SECONDS * 1000, refresh)


# ---------- Build the window ----------
root = tk.Tk()
root.title("Earthquake Live Map")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#0b1d33", highlightthickness=0)
canvas.pack()

status = tk.StringVar(value="Loading...")
info = tk.StringVar(value="Hover over a circle")
tk.Label(root, textvariable=status, anchor="w").pack(fill="x", padx=8)
tk.Label(root, textvariable=info, anchor="w", font=("Arial", 11, "bold")).pack(fill="x", padx=8, pady=(0, 6))

refresh()           # first fetch right away
root.mainloop()     # keep the window open
