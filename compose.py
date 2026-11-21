#!/usr/bin/env python3
"""Compose the 20 November 2026 front page: THE WORLD in one image.

Reads three freshly generated illustrations from assets/ and lays out a
1024x1024 newspaper front page with PIL. Deterministic: same inputs give
the same PNG bytes every run.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
W, H = 1024, 1024

PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (164, 30, 34)
NAVY = (31, 56, 100)
GREY = (90, 86, 78)
RULE = (60, 56, 50)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, max_w, text, fnt, leading, fill=INK):
    """Draw wrapped paragraph; return y after the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centre(draw, y, text, fnt, fill=INK, cx=W // 2):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)
    return y + fnt.size


def rule(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def cover_crop(img, tw, th, focus_y=0.45):
    """Crop img to the target aspect, centred horizontally and at focus_y."""
    iw, ih = img.size
    target = tw / th
    if iw / ih > target:
        nw = int(ih * target)
        x0 = (iw - nw) // 2
        box = (x0, 0, x0 + nw, ih)
    else:
        nh = int(iw / target)
        cy = int(ih * focus_y)
        y0 = max(0, min(ih - nh, cy - nh // 2))
        box = (0, y0, iw, y0 + nh)
    return img.crop(box).resize((tw, th), Image.LANCZOS)


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    mx = 24  # page margin
    rx = W - mx

    # ---- Masthead -------------------------------------------------------
    rule(d, mx, rx, 8, width=4)
    centre(d, 14, "THE WORLD", font(SERIF_B, 76))
    d.text((mx, 100), "FRIDAY, 20 NOVEMBER 2026",
           font=font(SANS_B, 16), fill=INK)
    tag = "THE DAY IN ONE IMAGE"
    d.text((rx - d.textlength(tag, font=font(SANS_B, 16)), 100), tag,
           font=font(SANS_B, 16), fill=INK)
    rule(d, mx, rx, 124, width=2)

    # ---- Main headline --------------------------------------------------
    centre(d, 132, "TRUMP, XI AND PUTIN SIGN", font(SERIF_B, 46))
    centre(d, 178, "JOINT PEACE DECLARATION", font(SERIF_B, 46))
    deck = ("The first three-way summit in Shenzhen ends in a four-point "
            "declaration \u2014 as Europe warns no deal should be struck "
            "over its head.")
    y = 228
    for line in wrap(d, deck, font(SERIF, 18), 940):
        centre(d, y, line, font(SERIF, 18))
        y += 24

    # ---- Lead picture ---------------------------------------------------
    summit = Image.open(os.path.join(
        ASSETS,
        "media-generation-summit-0-43002816-96c9-482b-917b-a9597b82cba0.png"))
    pic = cover_crop(summit, 976, 190, focus_y=0.55)
    page.paste(pic, (mx, 276))
    d.rectangle([mx, 276, rx, 466], outline=RULE, width=2)
    caption = ("The three presidents sign the joint declaration in Shenzhen. "
               "Illustration.")
    d.text((mx, 472), caption, font=font(SERIF, 14), fill=GREY)
    rule(d, mx, rx, 494, width=2)

    # ---- Three columns --------------------------------------------------
    col_w = 312
    col_x = [mx, 356, 688]
    top = 506
    img_h = 140

    # Column 1: ICJ ruling (typographic panel in the picture slot)
    x = col_x[0]
    d.rectangle([x, top, x + col_w, top + img_h], fill=NAVY)
    centre(d, top + 22, "ICJ", font(SERIF_B, 52), fill=PAPER,
           cx=x + col_w // 2)
    centre(d, top + 92, "THE HAGUE", font(SANS_B, 14), fill=PAPER,
           cx=x + col_w // 2)
    y = top + img_h + 10
    d.text((x, y), "JUSTICE", font=font(SANS_B, 14), fill=RED)
    y += 24
    y = para(d, x, y, col_w, "MYANMAR GUILTY OF GENOCIDE",
             font(SERIF_B, 27), 32)
    para(d, x, y + 4, col_w,
         "The world court rules Myanmar committed genocide against the "
         "Rohingya \u2014 a first against a state.",
         font(SERIF, 17), 22)

    # Column 2: Kyiv
    x = col_x[1]
    kyiv = Image.open(os.path.join(
        ASSETS,
        "media-generation-kyiv-0-76337d4b-a6ae-4263-a807-f2befe8dcf2c.png"))
    page.paste(cover_crop(kyiv, col_w, img_h, focus_y=0.6), (x, top))
    d.rectangle([x, top, x + col_w, top + img_h], outline=RULE, width=2)
    y = top + img_h + 10
    d.text((x, y), "UKRAINE  \u00b7  WAR", font=font(SANS_B, 14), fill=RED)
    y += 24
    y = para(d, x, y, col_w, "MISSILES RAIN ON KYIV",
             font(SERIF_B, 27), 32)
    para(d, x, y + 4, col_w,
         "Eight killed as overnight strikes hit Dnipro bridges; Poland "
         "reports its airspace breached.",
         font(SERIF, 17), 22)

    # Column 3: Riyadh
    x = col_x[2]
    riyadh = Image.open(os.path.join(
        ASSETS,
        "media-generation-riyadh-0-8fa6609a-5691-4326-a8d2-1e7a14754bfc.png"))
    page.paste(cover_crop(riyadh, col_w, img_h, focus_y=0.45), (x, top))
    d.rectangle([x, top, x + col_w, top + img_h], outline=RULE, width=2)
    y = top + img_h + 10
    d.text((x, y), "SAUDI ARABIA  \u00b7  CONFLICT",
           font=font(SANS_B, 14), fill=RED)
    y += 24
    y = para(d, x, y, col_w, "MISSILE HITS RIYADH TOWER",
             font(SERIF_B, 27), 32)
    para(d, x, y + 4, col_w,
         "A Houthi missile damages the PIF tower in the financial "
         "district as the Iran war enters its ninth month.",
         font(SERIF, 17), 22)

    # Column dividers (columns region only)
    for gx in (344, 676):
        d.line([(gx, top), (gx, 824)], fill=RULE, width=1)

    # ---- Bottom band ----------------------------------------------------
    rule(d, mx, rx, 834, width=2)
    by = 844

    # Markets box
    x = col_x[0]
    d.text((x, by), "MARKETS", font=font(SANS_B, 14), fill=RED)
    y = by + 22
    y = para(d, x, y, col_w, "NIKKEI \u22124.8%", font(SERIF_B, 26), 32)
    para(d, x, y + 4, col_w,
         "The S&P 500 slides for a fifth straight session on AI "
         "valuation doubts.",
         font(SERIF, 16), 20)

    # Cyclone box
    x = col_x[1]
    d.text((x, by), "CYCLONE AKVAN", font=font(SANS_B, 14), fill=RED)
    y = by + 22
    y = para(d, x, y, col_w, "300,000 EVACUATED", font(SERIF_B, 24), 32)
    para(d, x, y + 4, col_w,
         "Cyclone Akvan hits India's Odisha coast; 9,341 shelters readied.",
         font(SERIF, 16), 20)

    # Elsewhere box
    x = col_x[2]
    d.text((x, by), "ELSEWHERE", font=font(SANS_B, 14), fill=RED)
    y = by + 22
    y = para(d, x, y, col_w, "EU\u2013UK SUMMIT",
             font(SERIF_B, 20), 26)
    para(d, x, y + 6, col_w,
         "EU and UK leaders meet in Brussels; Iraqi forces move on a "
         "militia stronghold.",
         font(SERIF, 16), 20)

    for gx in (344, 676):
        d.line([(gx, by), (gx, 942)], fill=RULE, width=1)

    # ---- In brief strip + footer ---------------------------------------
    rule(d, mx, rx, 952, width=1)
    briefs = ("IN BRIEF:  COP31 draft drops the call to phase out fossil "
              "fuels  \u00b7  Kenya discharges its last Ebola patient; a "
              "42-day countdown begins  \u00b7  Tanker ablaze in the Strait "
              "of Hormuz.")
    y = 960
    for line in wrap(d, briefs, font(SERIF, 14), 976):
        d.text((mx, y), line, font=font(SERIF, 14), fill=INK)
        y += 18
    centre(d, 1002, "Compiled from wire reports  \u00b7  Illustrations "
           "generated for this front page",
           font(SANS, 11), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    page.save(out, "PNG", optimize=True, compress_level=9)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
