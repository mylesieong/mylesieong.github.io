#!/usr/bin/env python3
"""Generate one Open Graph image per page.

Every page gets its own card -- the brief rules out a single shared default.
Cards use real product screenshots where a product has them, and type on a flat
background where it does not. No stock photography anywhere.

    python3 gen_og.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "assets", "og")
W, H = 1200, 630

BG = (19, 17, 16)
FG = (243, 239, 233)
MUTED = (150, 142, 133)
ACCENT = (255, 138, 76)

BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
REG = "/System/Library/Fonts/Supplemental/Arial.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def card(name, title, kicker="Sai vs. Reality", footer="Building in public. Failing with documentation.",
         shot=None, accent=ACCENT):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)

    text_w = 1000
    if shot:
        p = os.path.join(ROOT, shot.lstrip("/"))
        if os.path.exists(p):
            s = Image.open(p).convert("RGB")
            target_h = 470
            ratio = target_h / s.height
            s = s.resize((max(1, int(s.width * ratio)), target_h), Image.LANCZOS)
            max_w = 330
            if s.width > max_w:
                left = (s.width - max_w) // 2
                s = s.crop((left, 0, left + max_w, target_h))
            x = W - s.width - 70
            rounded = Image.new("L", s.size, 0)
            ImageDraw.Draw(rounded).rounded_rectangle([0, 0, s.width, s.height], 18, fill=255)
            im.paste(s, (x, (H - target_h) // 2), rounded)
            text_w = x - 140

    d.rectangle([0, 0, 10, H], fill=accent)

    fk = font(BOLD, 26)
    d.text((70, 66), kicker.upper(), font=fk, fill=accent)

    size = 74
    while size > 34:
        ft = font(BOLD, size)
        lines = wrap(d, title, ft, text_w)
        if len(lines) * (size + 14) <= 340:
            break
        size -= 4
    ft = font(BOLD, size)
    lines = wrap(d, title, ft, text_w)

    total = len(lines) * (size + 14)
    y = (H - total) // 2 + 10
    for ln in lines:
        d.text((70, y), ln, font=ft, fill=FG)
        y += size + 14

    ff = font(REG, 25)
    d.text((70, H - 88), footer, font=ff, fill=MUTED)

    im.save(os.path.join(OUT, name), "PNG", optimize=True)
    return name


# --------------------------------------------------------------------------
# Product icons. Most are artwork on a transparent background, and several are
# light-on-transparent, so they disappear against a dark page. Flatten each one
# onto a plate chosen for contrast against its own artwork, at a fixed size, so
# the same file works in light and dark mode.
# --------------------------------------------------------------------------

ICON_SRC = [
    ("runout-rank", "/products/runout-rank/assets/img/icon-512.png"),
    ("pool-billiards-self-trainer", "/assets/images/logo_pool&biiliards.png"),
    ("snooker-self-trainer", "/assets/images/logo_snooker.png"),
    ("bible-project", "/assets/images/logo_bible.webp"),
    ("flexi", "/assets/images/flexi_logo.png"),
    ("tacet", "/products/tacet/assets/apple-touch-icon.png"),
    ("calmly-news", "/assets/images/calmly_news_logo.png"),
]

ICON_OUT = os.path.join(ROOT, "assets", "icons")
ICON_SIZE = 96


def build_icons():
    if not os.path.isdir(ICON_OUT):
        os.makedirs(ICON_OUT)
    for slug, src in ICON_SRC:
        p = os.path.join(ROOT, src.lstrip("/"))
        if not os.path.exists(p):
            print("   missing", src)
            continue
        im = Image.open(p).convert("RGBA")
        im = im.resize((ICON_SIZE, ICON_SIZE), Image.LANCZOS)

        px = im.load()
        tot = n = 0
        for y in range(0, ICON_SIZE, 3):
            for x in range(0, ICON_SIZE, 3):
                r, g, b, a = px[x, y]
                if a > 40:
                    tot += 0.2126 * r + 0.7152 * g + 0.0722 * b
                    n += 1
        lum = (tot / n) if n else 128
        plate = (28, 25, 23) if lum > 150 else (255, 255, 255)

        out = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), plate + (255,))
        out.alpha_composite(im)
        out.convert("RGB").save(os.path.join(ICON_OUT, slug + ".png"), "PNG", optimize=True)
        print("   icon %-30s plate=%s lum=%d" % (slug, "dark" if lum > 150 else "light", lum))


CARDS = [
    ("home.png", "Building in public. Failing with documentation.", None,
     "Products across unrelated categories, including the ones Reality killed."),
    ("products.png", "Every product, and where it actually stands", None, None),
    ("killed.png", "The products Reality closed, with the evidence", None,
     "They keep their URLs. They are never redirected."),
    ("about.png", "I'm not trying to become successful. I'm trying to become less stupid.", None, None),
    ("calmly-news.png", "Ten stories a day. Then the feed locks.",
     "/assets/images/calmly_news_1.jpg", "Calmly News · free on iOS and Android"),
    ("harness-survey.png", "Your survey talks back", None,
     "Harness Survey · it writes the follow-up question itself"),
    ("case-studies.png", "Case studies from four-week builds", None, "Sai Studio"),
    ("case-bible.png", "Follow the breadcrumb: micro innovation on a proven genre",
     "/assets/images/bible1.png", "Sai Studio · case study"),
    ("case-web3.png", "Build a production level social network in 4 weeks", None,
     "Sai Studio · case study"),
    ("sai-studio.png", "MVP builds for founders without a technical co-founder", None,
     "Sai Studio"),
    ("chatengage.png", "Send a package. Start the conversation.", None,
     "Chatengage · still being built"),
    ("founders-note.png", "Killed during ideation, before it was built", None,
     "Founder's Note · with the post-mortem attached"),
    ("field-notes.png", "Vancouver Field Notes", None,
     "A private journal between two friends."),
]


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    build_icons()
    for name, title, shot, footer in CARDS:
        kw = {}
        if footer:
            kw["footer"] = footer
        card(name, title, shot=shot, **kw)
        print("  ", name)
    print("generated %d og images" % len(CARDS))


if __name__ == "__main__":
    main()
