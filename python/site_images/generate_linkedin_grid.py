"""LinkedIn banner: an activity grid drawn from real per-day counts.

Each column is a week, Sunday at the top, newest week on the right. Shades run from the
site's background to its teal in four steps, by quartile of the active days.

    python generate_linkedin_grid.py            # 28 weeks, large tiles (7 rows fill 396px)
    python generate_linkedin_grid.py --dense    # 112 weeks in two bands, older year on top
    python generate_linkedin_grid.py --calendar arndvs            # refresh from the GitHub contribution calendar
    python generate_linkedin_grid.py --commits arndvs/arndvs ...  # refresh from commits in the named repos
    python generate_linkedin_grid.py --growth   # illustration, not data: few tiles on the left, more and more to the right

Rules: rules/site-images.md, "LinkedIn banner".
"""

import argparse
import json
import subprocess
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw

import style

DATA = style.HERE / "data" / "activity-days.json"
OUT = style.DEFAULT_OUT / "linkedin" / "banner-activity-grid.png"
TZ = ZoneInfo("America/Los_Angeles")
W, H = 1584, 396
SCALE, SS = 2, 3  # written at 2x; drawn at 6x and reduced so the corners stay clean
EMPTY = (16, 20, 19)
AUTHORS = ("Aaron Davis", "arndvs")


def gh(*args):
    return subprocess.run(["gh", "api", *args], capture_output=True, text=True, check=True).stdout


def from_calendar(login, today):
    """The contribution calendar GitHub shows on the profile, two years of it."""
    q = ("query($l:String!,$f:DateTime!,$t:DateTime!){user(login:$l){contributionsCollection(from:$f,to:$t)"
         "{contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}")
    days = {}
    for back in (1, 0):
        t = today - timedelta(days=365 * back)
        f = t - timedelta(days=364)
        cal = json.loads(gh("graphql", "-f", f"query={q}", "-f", f"l={login}",
                            "-f", f"f={f}T00:00:00Z", "-f", f"t={t}T23:59:59Z"))
        for wk in cal["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]:
            days.update({d["date"]: d["contributionCount"] for d in wk["contributionDays"] if d["contributionCount"]})
    return days, f"GitHub contribution calendar for {login}"


def from_commits(repos, today):
    since = (today - timedelta(days=800)).isoformat() + "T00:00:00Z"
    seen = {}
    for repo in repos:
        page = 1
        while True:
            rows = gh(f"repos/{repo}/commits?since={since}&per_page=100&page={page}",
                      "-q", ".[]|[.sha,.commit.author.date,.commit.author.name]|@tsv").splitlines()
            seen.update({s: t for s, t, n in (r.split("\t") for r in rows) if n in AUTHORS})
            if len(rows) < 100:
                break
            page += 1
    days = Counter(datetime.fromisoformat(t.replace("Z", "+00:00")).astimezone(TZ).date().isoformat()
                   for t in seen.values())
    return dict(sorted(days.items())), "Commits per day (Pacific time) in " + ", ".join(repos)


def shade(level):
    if level == 0:
        return EMPTY
    t = (0.26, 0.5, 0.75, 1.0)[level - 1]
    return tuple(round(b + (a - b) * t) for a, b in zip(style.ACCENT, style.BG))


def draw(days, today, dense):
    cols, bands = (56, 2) if dense else (28, 1)
    pitch = W / cols  # 7 rows per band at this pitch is exactly 396px
    gap, radius = pitch * 0.17, pitch * 0.15
    weeks = cols * bands
    start = today - timedelta(days=(today.weekday() + 1) % 7 + 7 * (weeks - 1))
    span = {start + timedelta(days=i) for i in range(weeks * 7)}
    vals = sorted(n for d, n in days.items() if date.fromisoformat(d) in span)
    cut = [vals[int(len(vals) * q)] for q in (0.25, 0.5, 0.75)] if vals else [1, 2, 3]
    k = SCALE * SS
    im = Image.new("RGB", (W * k, H * k), style.BG)
    d = ImageDraw.Draw(im)
    for i in range(weeks * 7):
        n = days.get((start + timedelta(days=i)).isoformat(), 0)
        wk, row = divmod(i, 7)
        x0, y0 = (wk % cols) * pitch + gap / 2, (wk // cols * 7 + row) * pitch + gap / 2
        box = [round(v * k) for v in (x0, y0, x0 + pitch - gap, y0 + pitch - gap)]
        d.rounded_rectangle(box, radius=radius * k, fill=shade(n and 1 + sum(n > c for c in cut)))
    return im.resize((W * SCALE, H * SCALE), Image.LANCZOS), start, len(vals), sum(vals)


def draw_growth(seed=7):
    """An illustration, not data: the grid fills and brightens from left to right."""
    import random
    rnd = random.Random(seed)
    cols, rows = 56, 14
    pitch = W / cols
    gap, radius = pitch * 0.17, pitch * 0.15
    k = SCALE * SS
    im = Image.new("RGB", (W * k, H * k), style.BG)
    d = ImageDraw.Draw(im)
    for c in range(cols):
        t = max(0.0, (c - 9) / (cols - 10))  # the first columns sit behind the profile photo and stay empty
        fill = 0.03 + 0.95 * t ** 1.6  # share of tiles lit in this column
        for r in range(rows):
            level = 0
            if t > 0 and rnd.random() < fill:
                level = min(4, max(1, round(1 + 3 * t ** 1.3 + rnd.uniform(-1.3, 1.0))))
            x0, y0 = c * pitch + gap / 2, r * pitch + gap / 2
            box = [round(v * k) for v in (x0, y0, x0 + pitch - gap, y0 + pitch - gap)]
            d.rounded_rectangle(box, radius=radius * k, fill=shade(level))
    return im.resize((W * SCALE, H * SCALE), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--calendar", metavar="LOGIN", help="refresh the data from the GitHub contribution calendar")
    ap.add_argument("--commits", nargs="+", metavar="OWNER/REPO", help="refresh the data from commits in these repos")
    ap.add_argument("--dense", action="store_true", help="112 weeks in two bands instead of 28 weeks")
    ap.add_argument("--growth", action="store_true", help="draw the left-to-right illustration instead of data")
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args()
    if a.growth:
        out = a.out or OUT.with_name("banner-growth-grid.png")
        out.parent.mkdir(parents=True, exist_ok=True)
        draw_growth().save(out, optimize=True)
        print(f"{out}: illustration, not data")
        return
    a.out = a.out or OUT
    if a.calendar or a.commits:
        today = datetime.now(TZ).date()
        days, source = from_calendar(a.calendar, today) if a.calendar else from_commits(a.commits, today)
        DATA.write_text(json.dumps({"source": source, "fetched": today.isoformat(), "days": days}, indent=1))
    data = json.loads(DATA.read_text())
    today = date.fromisoformat(data["fetched"])
    im, start, active, total = draw(data["days"], today, a.dense)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    im.save(a.out, optimize=True)
    print(f"{a.out}: {start} to {today}, {active} active days, {total} total. Source: {data['source']}")


if __name__ == "__main__":
    main()
