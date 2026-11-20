#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news infographic (build time only).

Own layout: gold masthead with the date, one wide lead card, a 2x2 grid of
stories, a two-column bottom strip and a sources footer. Pillow only.
Run: python3 draw_news.py  -> writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
BG = (14, 27, 46)
PANEL = (22, 40, 63)
PANEL2 = (27, 48, 74)
GOLD = (232, 184, 75)
INK = (242, 242, 237)
MUTED = (169, 184, 204)
RULE = (58, 86, 122)
ACCENTS = [(232, 184, 75), (94, 180, 214), (224, 122, 95), (126, 200, 148)]


def font(name, size):
    for path in (
        f"/usr/share/fonts/truetype/dejavu/{name}.ttf",
        f"/usr/share/fonts/{name}.ttf",
    ):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F_TITLE = font("DejaVuSans-Bold", 46)
F_DATE = font("DejaVuSans-Bold", 40)
F_KICKER = font("DejaVuSans-Bold", 21)
F_HEAD = font("DejaVuSans-Bold", 25)
F_BODY = font("DejaVuSans", 18)
F_SMALL = font("DejaVuSans", 17)
F_STRIP_HEAD = font("DejaVuSans-Bold", 20)
F_STRIP = font("DejaVuSans", 18)
F_FOOT = font("DejaVuSans", 15)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def cyclone(draw, cx, cy, r, color):
    for i in range(5):
        rr = r - i * r / 5
        draw.arc(
            [cx - rr, cy - rr, cx + rr, cy + rr],
            start=200 + i * 55, end=200 + i * 55 + 250,
            fill=color, width=4,
        )


def flame(draw, cx, cy, s, color):
    pts = [
        (cx, cy - s), (cx + s * 0.55, cy - s * 0.1), (cx + s * 0.35, cy + s * 0.45),
        (cx + s * 0.7, cy + s * 0.25), (cx + s * 0.35, cy + s),
        (cx - s * 0.35, cy + s), (cx - s * 0.7, cy + s * 0.25),
        (cx - s * 0.35, cy + s * 0.45), (cx - s * 0.55, cy - s * 0.1),
    ]
    draw.polygon(pts, fill=color)


def ship(draw, x, y, w, color):
    draw.polygon(
        [(x, y), (x + w, y), (x + w * 0.86, y + 26), (x + w * 0.14, y + 26)],
        fill=color,
    )
    draw.rectangle([x + w * 0.3, y - 26, x + w * 0.7, y], fill=color)
    draw.rectangle([x + w * 0.42, y - 44, x + w * 0.58, y - 26], fill=color)


def bat_ball(draw, cx, cy, color):
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=color, width=5)
    draw.line([cx - 26, cy + 26, cx + 26, cy - 26], fill=color, width=3)
    draw.ellipse([cx + 34, cy - 44, cx + 62, cy - 16], fill=color)


def building(draw, x, y, w, h, color):
    draw.rectangle([x, y, x + w, y + h], outline=color, width=4)
    for i in range(4):
        for j in range(6):
            draw.rectangle(
                [x + 8 + i * (w - 16) / 4, y + 10 + j * (h - 20) / 6,
                 x + 8 + i * (w - 16) / 4 + 12, y + 10 + j * (h - 20) / 6 + 12],
                fill=color,
            )


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.text((36, 26), "THE WORLD IN ONE IMAGE", font=F_KICKER, fill=GOLD)
    d.text((36, 56), "FRIDAY 20 NOVEMBER 2026", font=F_DATE, fill=INK)
    d.line([(36, 132), (988, 132)], fill=RULE, width=3)

    # ---- lead: Cyclone Akvan ----
    d.rounded_rectangle([36, 150, 988, 420], radius=14, fill=PANEL)
    d.rectangle([36, 150, 988, 158], fill=GOLD)
    cyclone(d, 905, 285, 62, (94, 180, 214))
    d.text((60, 172), "CYCLONE AKVAN HITS ODISHA", font=F_TITLE, fill=INK)
    lead = wrap(
        d,
        "Severe Cyclonic Storm Akvan makes landfall near Gopalpur around noon, "
        "with winds of 90-100 km/h, gusting to 110.",
        F_BODY, 800,
    )
    y = text_block(d, 60, 240, lead, F_BODY, INK, 28)
    lead2 = wrap(
        d,
        "More than 300,000 people evacuated to shelters; 423 rescue teams "
        "deployed; 69 trains cancelled.",
        F_BODY, 800,
    )
    text_block(d, 60, y + 10, lead2, F_BODY, MUTED, 28)

    # ---- 2x2 grid ----
    cards = [
        ("TAIZ, YEMEN", "Voices from the besieged city",
         "The BBC reaches seven people trapped in Taiz, ringed by Houthi "
         "fighters. About 800,000 are cut off from aid.", "flame"),
        ("STRAIT OF HORMUZ", "Tankers ablaze after mine strikes",
         "Iran's army says two oil tankers caught fire after hitting naval "
         "mines east of the strait. Claims unverified.", "ship"),
        ("WELLINGTON", "Nicholls & Phillips rescue NZ",
         "Day 2 of the 1st Test: New Zealand reach 317 for 6 at lunch. "
         "Nicholls 146 not out, Phillips 118.", "bat"),
        ("BRUSSELS", "EU summons Russia's envoy",
         "Russian strikes damaged the Austrian and Dutch embassies in Kyiv, "
         "so the EU calls in Moscow's ambassador.", "building"),
    ]
    gx, gy = 36, 436
    cw, ch, gap = 466, 187, 20
    for i, (kicker, head, body, icon) in enumerate(cards):
        x = gx + (i % 2) * (cw + gap)
        yy = gy + (i // 2) * (ch + 16)
        accent = ACCENTS[i]
        d.rounded_rectangle([x, yy, x + cw, yy + ch], radius=12, fill=PANEL2)
        d.rectangle([x, yy, x + cw, yy + 7], fill=accent)
        d.text((x + 18, yy + 18), kicker, font=F_KICKER, fill=accent)
        d.text((x + 18, yy + 46), head, font=F_HEAD, fill=INK)
        lines = wrap(d, body, F_BODY, cw - 110)
        text_block(d, x + 18, yy + 80, lines[:3], F_BODY, MUTED, 25)
        ix, iy = x + cw - 78, yy + ch - 62
        if icon == "flame":
            flame(d, ix + 28, iy + 8, 26, accent)
        elif icon == "ship":
            ship(d, ix - 6, iy + 22, 72, accent)
        elif icon == "bat":
            bat_ball(d, ix + 28, iy + 22, accent)
        else:
            building(d, ix + 2, iy - 8, 52, 62, accent)

    # ---- bottom strip ----
    sy = 842
    d.rounded_rectangle([36, sy, 988, sy + 104], radius=12, fill=PANEL)
    d.line([(512, sy + 14), (512, sy + 90)], fill=RULE, width=2)
    d.text((60, sy + 12), "MARKETS", font=F_STRIP_HEAD, fill=GOLD)
    strip_l = wrap(
        d,
        "Anthropic's record $81bn share sale closes today, a day after its "
        "Nasdaq debut ended 17% up at $97.17.",
        F_STRIP, 420,
    )
    text_block(d, 60, sy + 40, strip_l[:3], F_STRIP, INK, 24)
    d.text((536, sy + 12), "ALSO TODAY", font=F_STRIP_HEAD, fill=GOLD)
    strip_r = wrap(
        d,
        "20 November is World Children's Day — and the UN climate talks "
        "in Türkiye reach their final stretch.",
        F_STRIP, 420,
    )
    text_block(d, 536, sy + 40, strip_r[:3], F_STRIP, INK, 24)

    # ---- footer ----
    d.line([(36, 962), (988, 962)], fill=RULE, width=2)
    d.text(
        (36, 974),
        "Sources: The Hindu · India Today · BBC · Al Jazeera · Anadolu · Reuters · Cricbuzz",
        font=F_FOOT, fill=MUTED,
    )
    d.text(
        (36, 996),
        "All events of 20 November 2026 · Drawn by an AI agent for make.fun",
        font=F_FOOT, fill=MUTED,
    )

    img.save(OUT, "PNG")
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
