"""Render the homepage's explanatory GIF from the public authentication fixture.

Requires Pillow and DejaVu Sans (Debian: fonts-dejavu-core). Run from any cwd.
The 4.8-second animation loops; its last frame is also the reduced-motion
poster. This is a visual explanation, not a Splunk capture or live telemetry.
"""
import csv
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/animation"
FONT = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
BG, TRACK, MINT, WHITE, AMBER = "#172b28", "#365a50", "#baf1d0", "#eff8f2", "#f1cf85"


def render(frame):
    im = Image.new("RGB", (960, 360), BG)
    d = ImageDraw.Draw(im)
    font = lambda size: ImageFont.truetype(str(FONT), size)
    t = frame / 10
    source_x, gate_x, destination_x = 65, 388, 800
    ys = [55, 93, 131, 169, 207]
    # Five failure lanes and an independent success lane converge at the rule.
    routes = [[(source_x, y), (195, y), (310, 146), (gate_x, 146)] for y in ys]
    routes.append([(source_x, 286), (240, 286), (335, 215), (gate_x, 215)])
    for i, points in enumerate(routes):
        color = MINT if i < 5 else AMBER
        d.line(points, fill=TRACK, width=3, joint="curve")
        d.ellipse((source_x-8, points[0][1]-8, source_x+8, points[0][1]+8), fill=color)
        progress = min(1, max(0, (t - i * .13) / 1.55))
        if progress:
            # Polyline interpolation keeps each packet attached to its lane.
            lengths = [((b[0]-a[0])**2+(b[1]-a[1])**2)**.5 for a, b in zip(points, points[1:])]
            distance = sum(lengths) * progress
            trace = [points[0]]
            for a, b, length in zip(points, points[1:], lengths):
                amount = min(1, distance / length)
                endpoint = (a[0]+(b[0]-a[0])*amount, a[1]+(b[1]-a[1])*amount)
                trace.append(endpoint)
                if distance <= length:
                    break
                distance -= length
            d.line(trace, fill=color, width=4, joint="curve")
            x, y = trace[-1]
            d.ellipse((x-12, y-12, x+12, y+12), outline=color, width=2)
            d.ellipse((x-5, y-5, x+5, y+5), fill=WHITE)
    active = t >= 2.2
    d.rounded_rectangle((388, 69, 630, 267), radius=18, fill="#213f36", outline=MINT if active else TRACK, width=3)
    d.text((509, 148), "600s", font=font(68), fill=WHITE, anchor="mm")
    d.text((509, 217), "5 FAIL + 1 OK", font=font(23), fill=MINT, anchor="mm")
    d.line([(630, 168), (710, 168), (756, 168)], fill=TRACK, width=3)
    progress = min(1, max(0, (t-2.45)/.75))
    if progress:
        x = 630 + 126*progress
        d.line([(630, 168), (x, 168)], fill=AMBER, width=4)
        d.ellipse((x-7, 161, x+7, 175), fill=AMBER)
    points = [(800, 124), (844, 168), (800, 212), (756, 168)]
    d.polygon(points, fill="#3b3b2a" if t >= 3.2 else BG)
    d.line(points+[points[0]], fill=AMBER if t >= 3.2 else TRACK, width=3)
    if t >= 3.2:
        d.text((800, 170), "?", font=font(42), fill=AMBER, anchor="mm")
    d.text((800, 257), "REVIEW", font=font(30), fill=AMBER, anchor="mm")
    d.text((source_x-12, 330), "SOURCE EVENTS", font=font(24), fill=MINT)
    return im


def main():
    with (ROOT / "projects/01-authentication-detection/validation_events.csv").open(newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["scenario"] == "ten_minute_boundary"]
    assert [r["event_type"] for r in rows] == ["login_failure"]*5+["login_success"]
    assert len({(r["username"], r["source_ip"]) for r in rows}) == 1
    assert (datetime.fromisoformat(rows[-1]["timestamp"])-datetime.fromisoformat(rows[0]["timestamp"])).total_seconds() == 600
    OUT.mkdir(exist_ok=True)
    frames = [render(i).quantize(colors=32) for i in range(48)]
    frames[0].save(OUT / "signal-to-case.gif", save_all=True, append_images=frames[1:], duration=100, loop=0, optimize=True, disposal=1)
    render(47).save(OUT / "signal-to-case-still.png", optimize=True)
    with Image.open(OUT / "signal-to-case.gif") as gif:
        assert gif.info.get("loop") == 0, "GIF must repeat continuously while displayed"
        duration = 0
        for i in range(gif.n_frames):
            gif.seek(i)
            duration += gif.info["duration"]
        assert duration == 4800
    assert (OUT / "signal-to-case.gif").stat().st_size < 250_000
    print("PASS: 4.8s looping GIF; five failures, one success, exact 600s boundary; under 250KB")


if __name__ == "__main__":
    main()
