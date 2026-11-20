#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261119 v3 FINAL.

One front page: Thursday 19 November 2026, 46 stories, 6 continents.
Deterministic: no timestamps, no randomness, no network. All facts
hardcoded from the verified recon blueprint (46 stories, each >=2 sources).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
NAVY = (22, 40, 63)
INK = (22, 24, 29)
RED = (176, 42, 33)
GOLD = (201, 162, 39)
GREY = (90, 86, 78)
LIGHT = (233, 226, 210)
WHITE = (255, 255, 255)

F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_NUM = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def tw(draw, text, f):
    return draw.textlength(text, font=f)


# ---------------------------------------------------------------- data
# fields: n, city, cat, headline, desc, region, lon, lat, tag
LEADS = [
    (1, "SHENZHEN", "SUMMIT",
     "Three presidents, one table",
     "Trump, Xi and Putin hold the first-ever three-way summit: 90 minutes and a "
     "4-point declaration on UN reform, refined-oil supply, state immunity and a "
     "nuclear war \u201cthat cannot be won\u201d. No Ukraine deal; Trump\u2013Putin talk ~40 min.",
     "ASIA", 114.0, 22.5, None),
    (2, "WORLDWIDE", "GAMES",
     "GTA VI is out",
     "On sale worldwide at midnight local time \u2014 New Zealand first. Metacritic 99 "
     "from 150 critics, all positive; OpenCritic 99; IGN 10/10. PS5 and Xbox "
     "Series X|S, 13 years after GTA V.",
     "GLOBAL", None, None, None),
    (3, "NEW YORK", "MARKETS",
     "Anthropic\u2019s $81.3bn debut",
     "ANT lists on Nasdaq at $83 \u2014 the biggest IPO on record, above SpaceX\u2019s $75bn. "
     "Opens $111.50 (+34%), closes $97.17 (+17%). Worth ~$2tn at the open.",
     "AMERICAS", -74.0, 40.7, None),
]

MIDS = [
    (4, "THE HAGUE", "LAW", "Myanmar guilty of genocide",
     "ICJ rules 9\u20136: ~10,000 Rohingya killed. Reparations and return ordered.",
     "EUROPE", 4.3, 52.0, None),
    (5, "ANTALYA", "CLIMATE", "COP31 draft drops fossil fuels",
     "Net-zero dates and the $120bn target cut. First COP text to admit >1.5\u00b0C.",
     "EUROPE", 30.7, 36.9, "FORECAST"),
    (6, "ODISHA", "STORM", "Cyclone Akvan nears India",
     "80,000+ evacuated; landfall Friday near Gopalpur. Winds 90\u2013100, gusting 110 km/h.",
     "ASIA", 85.5, 20.0, "FORECAST"),
    (7, "SEOUL", "EDUCATION", "551,864 sit the Suneung",
     "Flights grounded for listening, 13:10\u201313:35. Anti-AI cheating crackdown; 98 caught.",
     "ASIA", 127.0, 37.5, None),
    (8, "CANBERRA", "ECONOMY", "Jobless rate jumps to 4.9%",
     "A five-year high; 43,500 jobs lost in a month.",
     "OCEANIA", 149.0, -35.3, None),
    (9, "CRIMEA", "WAR", "Bridge hit for a third time",
     "Ukraine\u2019s Neptune missiles strike the rail section; traffic halted.",
     "EUROPE", 34.0, 45.0, None),
    (10, "RIYADH", "WAR", "Missiles target Riyadh",
     "PIF Tower hit by debris; coalition intercepts. Houthis claim a new strike.",
     "MIDDLE EAST", 46.7, 24.6, "CLAIM"),
    (11, "COPENHAGEN", "SECURITY", "Arctic pact backed 109\u20130",
     "Denmark approves the US pact; Pituffik expands. Greenland stays Danish.",
     "EUROPE", 12.6, 55.7, None),
    (12, "DHAKA", "UNREST", "Bangladesh erupts: 4 killed",
     "Awami League lockdown bites across 28 districts; Yunus\u2019s ancestral home torched.",
     "ASIA", 90.4, 23.8, None),
    (13, "WASHINGTON", "POLITICS", "Senate rejects Iran war curb",
     "51\u201348, with three Republican defectors. First Iran vote since the midterms.",
     "AMERICAS", -77.0, 38.9, None),
    (14, "BOGOT\u00c1", "LABOUR", "Unions strike nationwide",
     "Protest against De la Espriella\u2019s Economic Rescue Law (bill 477).",
     "AMERICAS", -74.0, 4.7, None),
    (15, "JAKARTA", "LAW", "Asset-seizure law passes",
     "Ends an 18-year wait: non-conviction seizure from Rp1bn, covering crypto.",
     "ASIA", 106.8, -6.2, None),
]

# one-liners: (n, city, text, region, lon, lat, tag)
BRIEFS = [
    (16, "Seoul", "Top court partly voids ex-PM Han\u2019s 15-year term (9\u20133), orders retrial", "ASIA", 127.0, 37.5, None),
    (17, "Nairobi", "Marathon champion Jepchirchir banned 3 years for EPO; loses Sydney title", "AFRICA", 36.8, -1.3, None),
    (18, "Florida", "Floods shut Broward and Miami-Dade schools after 15 in of rain", "AMERICAS", -80.2, 25.8, None),
    (19, "Paris", "Greens open door to a M\u00e9lenchon-led left pact; centre-left balks", "EUROPE", 2.35, 48.85, None),
    (20, "Gaza", "Israeli tanks push past the truce line in central Gaza; Hamas cries breach", "MIDDLE EAST", 34.5, 31.5, None),
    (21, "Amman", "Record 589m children lived in conflict zones in 2025, report says", "GLOBAL", 35.9, 31.95, None),
    (22, "Rome", "Author Corrado Augias dies at 91", "EUROPE", 12.5, 41.9, None),
    (23, "Mogadishu", "Somalia expels the UAE ambassador, 72 hours to leave", "AFRICA", 45.3, 2.0, None),
    (24, "Pretoria", "Central bank holds rate at 7.25% in a 4\u20133 split vote", "AFRICA", 28.2, -25.7, None),
    (25, "Wellington", "Court: pay-equity overhaul violated women\u2019s rights", "OCEANIA", 174.8, -41.3, None),
    (26, "Zurich", "FIFA names Diallo and Tashima as Infantino challengers", "EUROPE", 8.5, 47.4, None),
    (27, "Krasnodar", "Kyiv says it hit two oil refineries, Ilsky and Afipsky", "EUROPE", 39.0, 45.0, "CLAIM"),
    (28, "Washington", "Trump: US will \u201csee what happens\u201d on Iran after 1 Jan 2027", "MIDDLE EAST", -77.0, 38.9, None),
    (29, "Tokyo", "Takaichi holds talks with Putin, agrees to keep communicating", "ASIA", 139.7, 35.7, None),
    (30, "Sanaa", "Saudi-led strikes hit Yemen after the Riyadh attack; Houthis claim 15 killed", "MIDDLE EAST", 44.2, 15.35, "CLAIM"),
    (31, "Shenzhen", "APEC adopts Shenzhen Outlook on trade, data and AI risks", "ASIA", 114.0, 22.5, None),
    (32, "London", "UK and Norway fund \u00a3100m+ fast attack boats for Ukraine", "EUROPE", -0.1, 51.5, None),
    (33, "Belgrade", "Serbia elects \u010cupi\u0107 speaker with 140 votes", "EUROPE", 20.5, 44.8, None),
    (34, "Mexico City", "Banxico minutes point to a long rate pause at 6.25%", "AMERICAS", -99.1, 19.4, None),
    (35, "Berlin", "Coalition of the Willing calls for a Black Sea and energy ceasefire", "EUROPE", 13.4, 52.5, None),
    (36, "Tonga", "Drought emergency declared for 27 days as El Ni\u00f1o bites", "OCEANIA", -175.2, -21.1, None),
    (37, "Cook Islands", "Cyclone Xavier, Cat 4, weakens near Nassau; 300+ sheltered", "OCEANIA", -159.8, -21.2, "FORECAST"),
    (38, "Gaza", "Five aid groups rate the Gaza peace plan 4 out of 26", "MIDDLE EAST", 34.5, 31.5, None),
    (39, "Moscow", "Putin rules out a Black Sea and energy truce", "EUROPE", 37.6, 55.75, None),
    (40, "Auckland", "New Zealanders are the first to play GTA VI at midnight", "OCEANIA", 174.8, -36.85, None),
    (41, "Yenne, Senegal", "Search resumes for dozens missing after a migrant boat capsizes", "AFRICA", -17.4, 14.7, None),
    (42, "Da Nang", "Russian Tu-95 bombers leave Vietnam, buzz Taiwan and Japan", "ASIA", 108.2, 16.0, None),
    (43, "Tokyo", "India and Japan hold their 4th 2+2 ministerial dialogue", "ASIA", 139.7, 35.7, None),
    (44, "Washington", "US asks Supreme Court to block restored TPS for Venezuelans", "AMERICAS", -77.0, 38.9, None),
    (45, "Berlin", "UK pledges 1,000 British-built long-range drones for Ukraine", "EUROPE", 13.4, 52.5, None),
    (46, "Shenzhen", "China pledges $20m for APEC cooperation and a study centre", "ASIA", 114.0, 22.5, None),
]

REGIONS = [("ASIA", 11), ("EUROPE", 13), ("MIDDLE EAST", 5), ("AMERICAS", 6),
           ("OCEANIA", 5), ("AFRICA", 4), ("GLOBAL", 2)]

STATS = [("3", "presidents at one table"),
         ("99", "Metacritic \u2014 GTA VI"),
         ("$81.3bn", "Anthropic IPO, a record"),
         ("9\u20136", "ICJ genocide ruling"),
         ("109\u20130", "Arctic pact vote"),
         ("4.9%", "Australia jobless rate")]

HOURS = [("00:00", "AUCKLAND", "GTA VI opens"),
         ("08:40", "SEOUL", "Suneung"),
         ("10:00", "THE HAGUE", "ICJ: genocide"),
         ("11:50", "NEW YORK", "ANT $111.50"),
         ("14:10", "ANTALYA", "COP31 draft"),
         ("PM", "SHENZHEN", "summit"),
         ("EVE", "WASHINGTON", "51\u201348")]

DATE_CHECK = ["EU \u20ac45bn Ukraine loan plan (18 Nov)",
              "Van Gogh $190.4m record; Sotheby\u2019s $777.8m night (18 Nov)",
              "Nvidia results (18 Nov)",
              "Jeffries named US speaker (18 Nov)",
              "Sudan court sentences RSF chief Hemedti to death (18 Nov)",
              "Canada\u2013China tariff relief $400m (17 Nov)",
              "Philippines $2bn defence loan fact sheet (18 Nov)",
              "Gas Husky tanker sunk off Bulgaria (17 Nov)",
              "Red giant \u201cBao\u201d swallows a star, Nature (18 Nov)",
              "US strikes on Iran\u2019s Qeshm Island (17\u201318 Nov)"]

# ---------------------------------------------------------------- helpers
def wrap_text(draw, text, f, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def trunc(draw, text, f, max_w):
    if draw.textlength(text, font=f) <= max_w:
        return text
    ell = "\u2026"
    while text and draw.textlength(text + ell, font=f) > max_w:
        text = text[:-1]
    return text + ell


def tag_chip(draw, x, y, tag):
    """Small honesty tag. Returns width used."""
    f = font(F_SANS_B, 9)
    w = draw.textlength(tag, font=f) + 8
    col = RED if tag == "CLAIM" else GOLD
    draw.rounded_rectangle([x, y, x + w, y + 12], radius=2, fill=col)
    draw.text((x + 4, y + 1), tag, font=f, fill=WHITE)
    return w


# ---------------------------------------------------------------- icons
def icon(draw, x, y, s, cat):
    """Flat 24px-ish icon drawn from primitives, by category."""
    c = NAVY
    if cat == "LAW":  # scales of justice
        draw.line([x + s / 2, y + 2, x + s / 2, y + s - 4], fill=c, width=2)
        draw.line([x + 2, y + 6, x + s - 2, y + 6], fill=c, width=2)
        draw.line([x + 3, y + 6, x + 1, y + 13], fill=c, width=1)
        draw.line([x + s - 3, y + 6, x + s - 1, y + 13], fill=c, width=1)
        draw.arc([x, y + 10, x + 8, y + 17], 0, 180, fill=c, width=2)
        draw.arc([x + s - 8, y + 10, x + s, y + 17], 0, 180, fill=c, width=2)
        draw.line([x + s / 2 - 4, y + s - 3, x + s / 2 + 4, y + s - 3], fill=c, width=2)
    elif cat == "CLIMATE":  # globe
        draw.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=c, width=2)
        draw.ellipse([x + s / 2 - 3, y + 2, x + s / 2 + 3, y + s - 2], outline=c, width=1)
        draw.line([x + 2, y + s / 2, x + s - 2, y + s / 2], fill=c, width=1)
    elif cat == "STORM":  # cyclone spiral
        for r in (9, 6, 3):
            draw.arc([x + s / 2 - r, y + s / 2 - r, x + s / 2 + r, y + s / 2 + r],
                     20, 300, fill=c, width=2)
        draw.line([x + s / 2, y + s / 2, x + s - 2, y + 2], fill=c, width=2)
    elif cat == "EDUCATION":  # graduation cap
        draw.polygon([(x + s / 2, y + 4), (x + s - 2, y + 9), (x + s / 2, y + 14),
                      (x + 2, y + 9)], outline=c, width=2)
        draw.line([x + s - 2, y + 9, x + s - 2, y + 17], fill=c, width=2)
        draw.arc([x + 4, y + 13, x + s - 4, y + 20], 0, 180, fill=c, width=2)
    elif cat == "ECONOMY":  # rising bars
        draw.rectangle([x + 3, y + 14, x + 7, y + s - 3], fill=c)
        draw.rectangle([x + 9, y + 10, x + 13, y + s - 3], fill=c)
        draw.rectangle([x + 15, y + 5, x + 19, y + s - 3], fill=RED)
        draw.line([x + 2, y + 4, x + s - 2, y + 4], fill=c, width=1)
    elif cat == "WAR":  # burst
        cx, cy = x + s / 2, y + s / 2
        for ang in range(0, 360, 45):
            import math
            r1, r2 = 4, 10
            a = math.radians(ang)
            draw.line([cx + r1 * math.cos(a), cy + r1 * math.sin(a),
                       cx + r2 * math.cos(a), cy + r2 * math.sin(a)], fill=RED, width=2)
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=c)
    elif cat == "SECURITY":  # shield
        draw.polygon([(x + s / 2, y + 2), (x + s - 2, y + 6), (x + s - 2, y + 13),
                      (x + s / 2, y + s - 2), (x + 2, y + 13), (x + 2, y + 6)],
                     outline=c, width=2)
        draw.line([x + 7, y + 11, x + 10, y + 14, x + 17, y + 7], fill=RED, width=2)
    elif cat == "UNREST":  # flame
        draw.polygon([(x + s / 2, y + 2), (x + s - 3, y + 11), (x + s - 5, y + 8),
                      (x + s - 3, y + s - 3), (x + 3, y + s - 3), (x + 5, y + 8),
                      (x + 3, y + 11)], fill=RED)
    elif cat == "POLITICS":  # capitol dome
        draw.arc([x + 5, y + 3, x + s - 5, y + 13], 180, 360, fill=c, width=2)
        draw.line([x + s / 2, y + 1, x + s / 2, y + 3], fill=c, width=2)
        draw.rectangle([x + 4, y + 13, x + s - 4, y + 16], fill=c)
        draw.line([x + 2, y + 19, x + s - 2, y + 19], fill=c, width=2)
    elif cat == "LABOUR":  # gear-ish / raised fist simplified: hammer
        draw.line([x + 6, y + 4, x + 6, y + s - 3], fill=c, width=3)
        draw.rectangle([x + 3, y + 3, x + 16, y + 8], fill=RED)
        draw.line([x + 14, y + 8, x + s - 3, y + s - 3], fill=c, width=3)
    else:  # SUMMIT / GAMES / MARKETS generic star
        draw.polygon([(x + s / 2, y + 2), (x + s / 2 + 3, y + 9), (x + s - 2, y + 9),
                      (x + s / 2 + 5, y + 13), (x + s / 2 + 7, y + s - 2),
                      (x + s / 2, y + 16), (x + s / 2 - 7, y + s - 2),
                      (x + s / 2 - 5, y + 13), (x + 2, y + 9),
                      (x + s / 2 - 3, y + 9)], fill=GOLD)


# ---------------------------------------------------------------- world map
# Land spans on a 64-col x 22-row equirectangular grid (lon -180..180, lat ~75..-55).
LAND64 = [
    (0, [(8, 13), (20, 24), (33, 34), (37, 38), (44, 58)]),
    (1, [(4, 16), (20, 23), (32, 34), (36, 60)]),
    (2, [(3, 8), (9, 19), (27, 28), (30, 34), (35, 60)]),
    (3, [(6, 18), (29, 30), (31, 36), (37, 58)]),
    (4, [(7, 17), (30, 37), (38, 57), (57, 58)]),
    (5, [(8, 17), (30, 36), (39, 50), (50, 56), (56, 58)]),
    (6, [(8, 17), (30, 35), (38, 48), (48, 55), (56, 57)]),
    (7, [(8, 16), (30, 38), (39, 45), (44, 48), (49, 54)]),
    (8, [(7, 11), (30, 39), (40, 45), (44, 48), (50, 54)]),
    (9, [(8, 12), (31, 40), (41, 44), (45, 47), (49, 53)]),
    (10, [(11, 13), (31, 40), (45, 47), (49, 53)]),
    (11, [(12, 14), (15, 20), (32, 39), (48, 54)]),
    (12, [(15, 21), (32, 39), (49, 55)]),
    (13, [(15, 21), (32, 38), (50, 54)]),
    (14, [(16, 20), (33, 38)]),
    (15, [(16, 20), (33, 38), (39, 40)]),
    (16, [(16, 19), (33, 37), (39, 40), (51, 57)]),
    (17, [(17, 19), (33, 36), (50, 58)]),
    (18, [(17, 19), (33, 35), (51, 57), (59, 60)]),
    (19, [(18, 19), (53, 56), (59, 60)]),
    (20, [(18, 19), (59, 59)]),
    (21, [(18, 18)]),
]


def lonlat_to_xy(lon, lat, mx, my, mw, mh):
    x = mx + (lon + 180.0) / 360.0 * mw
    y = my + (75.0 - lat) / 130.0 * mh
    return x, y

# ---------------------------------------------------------------- lead art
def lead_art(draw, kind, x, y, w, h):
    """Flat illustration from primitives."""
    if kind == 1:  # APEC summit: three figures at a table
        draw.rectangle([x, y, x + w, y + h], fill=NAVY)
        draw.rectangle([x, y + h - 26, x + w, y + h], fill=GOLD)
        # backdrop flags
        for i, c in enumerate((RED, WHITE, GOLD)):
            fx = x + 18 + i * 26
            draw.line([fx, y + 10, fx, y + 34], fill=c, width=2)
            draw.polygon([(fx, y + 10), (fx + 14, y + 15), (fx, y + 20)], fill=c)
        # three seated figures
        cols = [(247, 242, 231), (201, 162, 39), (176, 42, 33)]
        for i, c in enumerate(cols):
            cx = x + w // 2 + (i - 1) * 78
            draw.ellipse([cx - 13, y + 22, cx + 13, y + 48], fill=(232, 205, 170))
            draw.arc([cx - 13, y + 22, cx + 13, y + 40], 180, 360, fill=INK, width=3)
            draw.polygon([(cx - 26, y + h - 26), (cx - 14, y + 50),
                          (cx + 14, y + 50), (cx + 26, y + h - 26)], fill=c)
            draw.polygon([(cx - 5, y + 50), (cx, y + 62), (cx + 5, y + 50)], fill=WHITE)
        draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    elif kind == 2:  # GTA VI: sunset skyline, palms, big VI
        for i in range(h):
            t = i / max(h - 1, 1)
            r = int(242 + (142 - 242) * t)
            g = int(166 + (74 - 166) * t)
            b = int(90 + (122 - 90) * t)
            draw.line([x, y + i, x + w, y + i], fill=(r, g, b))
        draw.ellipse([x + w - 78, y + 8, x + w - 28, y + 58], fill=GOLD)
        # skyline
        import math
        heights = [34, 52, 28, 62, 44, 70, 38, 56, 30, 48]
        bw = w // len(heights)
        for i, hh in enumerate(heights):
            draw.rectangle([x + i * bw + 2, y + h - 22 - hh, x + (i + 1) * bw - 2,
                            y + h - 22], fill=INK)
            for wy in range(y + h - 18 - hh, y + h - 24, 9):
                draw.rectangle([x + i * bw + 6, wy, x + i * bw + 9, wy + 4], fill=GOLD)
        draw.rectangle([x, y + h - 22, x + w, y + h], fill=INK)
        # palm
        px = x + 26
        draw.line([px, y + h - 22, px + 4, y + h - 58], fill=INK, width=3)
        for a in (-50, -15, 20, 55):
            ar = math.radians(a)
            ex = px + 4 + 16 * math.cos(ar)
            ey = y + h - 58 + 8 * math.sin(ar)
            draw.line([px + 4, y + h - 58, ex, ey], fill=INK, width=2)
        f = font(F_SERIF, 58)
        draw.text((x + 12, y + 2), "VI", font=f, fill=WHITE,
                  stroke_width=2, stroke_fill=NAVY)
        draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    else:  # Anthropic: rising chart
        draw.rectangle([x, y, x + w, y + h], fill=NAVY)
        for gy in range(y + 30, y + h - 20, 12):
            draw.line([x + 6, gy, x + w - 6, gy], fill=(52, 74, 100), width=1)
        bars = [8, 12, 10, 16, 20, 18, 24]
        bw = (w - 40) // len(bars)
        for i, bh in enumerate(bars):
            bx = x + 20 + i * bw
            col = GOLD if i % 2 == 0 else (120, 200, 130)
            draw.rectangle([bx, y + h - 24 - bh, bx + bw - 6, y + h - 24], fill=col)
        pts = [(x + 20 + i * bw, y + h - 24 - b) for i, b in enumerate(bars)]
        draw.line(pts, fill=RED, width=3)
        draw.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4],
                     fill=RED)
        f1 = font(F_NUM, 26)
        draw.text((x + 12, y + 2), "$97.17", font=f1, fill=WHITE)
        f2 = font(F_SANS_B, 13)
        t2 = "+17%  \u00b7  ANT"
        draw.text((x + w - 8 - tw(draw, t2, f2), y + 10), t2, font=f2, fill=GOLD)
        draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


# ---------------------------------------------------------------- sections
def section_masthead(draw, y):
    draw.line([14, y, 1010, y], fill=GOLD, width=3)
    y += 6
    f = font(F_SERIF, 24)
    t = "THE WORLD IN ONE DAY"
    draw.text(((W - tw(draw, t, f)) / 2, y), t, font=f, fill=NAVY)
    y += 26
    f = font(F_SERIF, 42)
    t = "Thursday 19 November 2026"
    draw.text(((W - tw(draw, t, f)) / 2, y), t, font=f, fill=INK)
    y += 46
    f = font(F_SERIF_I, 15)
    t = ("Trump, Xi and Putin meet \u00b7 GTA VI goes on sale worldwide \u00b7 "
         "Anthropic debuts on Nasdaq")
    draw.text(((W - tw(draw, t, f)) / 2, y), t, font=f, fill=RED)
    y += 18
    # region strip
    draw.rectangle([14, y, 1010, y + 20], fill=NAVY)
    f = font(F_SANS_B, 12)
    parts = "  \u00b7  ".join("%s %d" % (r, n) for r, n in REGIONS)
    t = parts + "    \u2014    46 STORIES \u00b7 6 CONTINENTS"
    draw.text(((W - tw(draw, t, f)) / 2, y + 3), t, font=f, fill=PAPER)
    return y + 22


def section_stats(draw, y):
    f_n = font(F_NUM, 20)
    f_l = font(F_SANS, 10)
    cw = 996 / 6
    for i, (num, lab) in enumerate(STATS):
        cx = 14 + i * cw
        draw.text((cx + (cw - tw(draw, num, f_n)) / 2, y), num, font=f_n, fill=RED)
        draw.text((cx + (cw - tw(draw, lab, f_l)) / 2, y + 23), lab, font=f_l, fill=GREY)
        if i:
            draw.line([cx, y + 2, cx, y + 34], fill=LIGHT, width=1)
    draw.line([14, y + 38, 1010, y + 38], fill=INK, width=1)
    return y + 40


def section_leads(draw, y):
    col_w, gap = 322, 8
    for i, lead in enumerate(LEADS):
        n, city, cat, head, desc, region, lon, lat, tag = lead
        x = 14 + i * (col_w + gap)
        lead_art(draw, n, x, y, col_w, 74)
        yy = y + 78
        f = font(F_SANS_B, 11)
        draw.text((x, yy), "%s \u00b7 %s" % (city, cat), font=f, fill=RED)
        yy += 14
        f = font(F_SERIF, 25)
        for ln in wrap_text(draw, head, f, col_w)[:2]:
            draw.text((x, yy), ln, font=f, fill=INK)
            yy += 27
        f = font(F_SANS, 12)
        for ln in wrap_text(draw, desc, f, col_w)[:4]:
            draw.text((x, yy), ln, font=f, fill=INK)
            yy += 15
    return y + 78 + 14 + 54 + 60 + 4


def section_mids(draw, y):
    cw, ch, gap = 245, 82, 6
    for r in range(3):
        for c in range(4):
            m = MIDS[r * 4 + c]
            n, city, cat, head, desc, region, lon, lat, tag = m
            x = 14 + c * (cw + gap)
            yy = y + r * (ch + 4)
            draw.rectangle([x, yy, x + cw, yy + ch], fill=WHITE, outline=NAVY, width=1)
            draw.rectangle([x + 5, yy + 5, x + 21, yy + 21], fill=RED)
            f = font(F_SANS_B, 10)
            num = str(n)
            draw.text((x + 13 - tw(draw, num, f) / 2, yy + 6), num, font=f, fill=WHITE)
            f = font(F_SANS_B, 10)
            draw.text((x + 25, yy + 7), "%s \u00b7 %s" % (city, cat), font=f, fill=NAVY)
            if tag:
                tag_chip(draw, x + cw - 58, yy + 5, tag)
            else:
                icon(draw, x + cw - 28, yy + 4, 22, cat)
            f = font(F_SERIF, 15)
            ly = yy + 24
            for ln in wrap_text(draw, head, f, cw - 12)[:2]:
                draw.text((x + 6, ly), ln, font=f, fill=INK)
                ly += 16
            f = font(F_SANS, 11)
            dlines = wrap_text(draw, desc, f, cw - 12)[:2]
            for ln in dlines:
                draw.text((x + 6, ly), ln, font=f, fill=INK)
                ly += 12
    return y + 3 * ch + 2 * 4 + 2


def section_map(draw, y):
    f = font(F_SANS_B, 13)
    draw.text((14, y), "WHERE IT HAPPENED \u2014 46 STORIES, ONE DAY", font=f, fill=NAVY)
    f2 = font(F_SANS_B, 11)
    v = "THE VERDICT:  ICJ 9\u20136 \u2014 Myanmar guilty of genocide"
    draw.text((1010 - tw(draw, v, f2), y + 1), v, font=f2, fill=RED)
    y += 16
    mx, my, mw, mh = 14, y, 996, 104
    draw.rectangle([mx - 2, my - 2, mx + mw + 2, my + mh + 2], outline=NAVY, width=1)
    # dots: 128 x 22 grid from 64-col land spans
    cols, rows = 128, 22
    dx, dy = mw / cols, mh / rows
    land = set()
    for row, spans in LAND64:
        for c0, c1 in spans:
            for c in range(c0, c1 + 1):
                land.add((row, 2 * c))
                land.add((row, 2 * c + 1))
    for (row, c) in land:
        cx = mx + (c + 0.5) * dx
        cy = my + (row + 0.5) * dy
        draw.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6], fill=NAVY)
    # pins + number labels with greedy collision avoidance.
    # Stories sharing one spot (e.g. Shenzhen 1/31/46) get one grouped label.
    grouped = {}
    order = []
    for s in list(LEADS) + list(MIDS):
        key = (s[6], s[7])
        if key[0] is None:
            continue
        if key not in grouped:
            grouped[key] = []
            order.append(key)
        grouped[key].append(str(s[0]))
    for b in BRIEFS:
        key = (b[4], b[5])
        if key not in grouped:
            grouped[key] = []
            order.append(key)
        grouped[key].append(str(b[0]))
    placed = []
    fnum = font(F_SANS_B, 8)
    offsets = [(7, -11), (8, 1), (-15, -11), (7, 5), (-15, 1),
               (0, -13), (11, -6), (-17, -6), (7, -4), (-22, 3),
               (20, -12), (0, 6), (-26, -11), (24, 1)]
    for key in order:
        lon, lat = key
        label = "/".join(grouped[key])
        px, py = lonlat_to_xy(lon, lat, mx, my, mw, mh)
        draw.ellipse([px - 2.6, py - 2.6, px + 2.6, py + 2.6], fill=RED)
        lw = tw(draw, label, fnum) + 2
        lh = 9
        for ox, oy in offsets:
            lx, ly = px + ox, py + oy
            if lx < mx or lx + lw > mx + mw or ly < my or ly + lh > my + mh:
                continue
            clash = False
            for (ex, ey, ew, eh) in placed:
                if (lx < ex + ew + 2 and lx + lw > ex - 2 and
                        ly < ey + eh + 2 and ly + lh > ey - 2):
                    clash = True
                    break
            if clash:
                continue
            draw.rectangle([lx - 1, ly - 1, lx + lw + 1, ly + lh], fill=PAPER,
                           outline=RED, width=1)
            draw.text((lx + 1, ly), label, font=fnum, fill=RED)
            placed.append((lx, ly, lw, lh))
            break
    return y + mh + 6


def section_briefs(draw, y):
    f = font(F_SANS_B, 13)
    draw.text((14, y), "ALSO ON THURSDAY 19 NOVEMBER 2026", font=f, fill=NAVY)
    y += 16
    f_n = font(F_SANS_B, 11)
    f_t = font(F_SANS, 11)
    col_w = 490
    rows = 16
    for i, b in enumerate(BRIEFS):
        n, city, text, region, lon, lat, tag = b
        col = 0 if i < rows else 1
        row = i if col == 0 else i - rows
        x = 14 + col * 506
        yy = y + row * 11
        num = "%d." % n
        draw.text((x, yy), num, font=f_n, fill=RED)
        tx = x + tw(draw, num, f_n) + 3
        head = "%s \u2014 " % city
        draw.text((tx, yy), head, font=f_n, fill=INK)
        tx += tw(draw, head, f_n)
        line = text + ("  [%s]" % tag if tag else "")
        draw.text((tx, yy), trunc(draw, line, f_t, x + col_w - tx), font=f_t, fill=INK)
    return y + rows * 11 + 2


def section_hours(draw, y):
    draw.rectangle([14, y, 1010, y + 18], fill=NAVY)
    f = font(F_SANS_B, 9)
    items = ["%s %s %s" % (t, c, d) for (t, c, d) in HOURS]
    t = "BY HOURS:  " + " \u00b7 ".join(items)
    t = trunc(draw, t, f, 980)
    draw.text(((W - tw(draw, t, f)) / 2, y + 4), t, font=f, fill=PAPER)
    return y + 20


def section_datecheck(draw, y):
    f = font(F_SANS_B, 9)
    items = ["EU \u20ac45bn Ukraine loan (18 Nov)",
             "Van Gogh $190.4m (18 Nov)",
             "Nvidia results (18 Nov)",
             "Jeffries named speaker (18 Nov)",
             "Sudan sentences RSF chief Hemedti (18 Nov)"]
    t = "DATE CHECK \u2014 NOT 19 NOV:  " + "  \u00b7  ".join(items)
    draw.text((14, y), trunc(draw, t, f, 996), font=f, fill=GREY)
    return y + 13


def section_footer(draw, y):
    f = font(F_SANS, 9)
    l1 = ("SOURCES: Reuters \u00b7 AP \u00b7 BBC \u00b7 AFP \u00b7 Al Jazeera \u00b7 The Hindu \u00b7 "
          "ABS \u00b7 IMD \u00b7 Fiji Met Service \u00b7 gov.uk \u00b7 Save the Children \u00b7 AIU \u00b7 NWS")
    draw.text(((W - tw(draw, l1, f)) / 2, y), l1, font=f, fill=GREY)
    l2 = ("Every story above happened, or was first reported, on Thursday 19 November 2026 "
          "(any time zone). Claims are attributed, not stated as fact.")
    draw.text(((W - tw(draw, l2, f)) / 2, y + 11), l2, font=f, fill=GREY)
    return y + 24


# ---------------------------------------------------------------- main
def build(out_path):
    total = len(LEADS) + len(MIDS) + len(BRIEFS)
    assert total == 46, "story count %d != 46" % total
    assert sum(n for _, n in REGIONS) == 46, "region sum != 46"
    regions = {}
    for s in list(LEADS) + list(MIDS):
        regions[s[5]] = regions.get(s[5], 0) + 1
    for b in BRIEFS:
        regions[b[3]] = regions.get(b[3], 0) + 1
    for r, n in REGIONS:
        assert regions.get(r, 0) == n, "region %s: %d != %d" % (r, regions.get(r, 0), n)

    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([6, 6, W - 7, H - 7], outline=INK, width=2)
    y = 12
    y = section_masthead(draw, y)
    y = section_stats(draw, y)
    y = section_leads(draw, y)
    y = section_mids(draw, y)
    y = section_map(draw, y)
    y = section_briefs(draw, y)
    y = section_hours(draw, y)
    y = section_datecheck(draw, y)
    y = section_footer(draw, y)
    assert y <= 1014, "layout overflow: final y=%d" % y
    img.save(out_path, "PNG", optimize=True)
    return y


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    final_y = build(os.path.join(here, "entry.png"))
    print("built entry.png, final y=%d" % final_y)
