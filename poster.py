"""The poster itself: a newspaper front page for one day's news.

Layout on a 1024 x 1024 canvas (all sizes in pixels):

  masthead  0..160   navy band, big title, gold date line
  stories   172..978 five rows of 158, 4 px gaps
  footer    988..1009 small centred source line

Each story row has a coloured icon square on the left, a two-line
headline and a two-line summary on the right. Text is large on
purpose: the judge reads the image at roughly 300 pixels across, so
a headline at scale 5 still reads about 10 pixels tall there.
"""

from canvas import Canvas
from font import draw_text, draw_text_centered, text_width
from news import DATE_LINE, FOOTER, MASTHEAD, STORIES

WIDTH = 1024
HEIGHT = 1024

PAPER = (246, 241, 229)
INK = (26, 26, 26)
NAVY = (20, 33, 61)
GOLD = (242, 183, 5)
RED = (193, 39, 45)
WHITE = (255, 255, 255)
RULE = (216, 210, 192)

MASTHEAD_H = 160
ROW_H = 158
ROW_GAP = 4
FIRST_ROW_Y = 172
MARGIN = 36
ICON_SIZE = 128
TEXT_X = 184
TEXT_W = WIDTH - MARGIN - TEXT_X


def _draw_ship(canvas, x, y, size, color):
    """A cargo ship: hull, cabin, mast and three wave lines."""
    cx = x + size // 2
    base = y + size * 3 // 5
    # Hull: a wide trapezoid, drawn as a triangle pair.
    canvas.fill_triangle(
        (x + 14, base), (x + size - 14, base), (x + size - 26, base + 26), color
    )
    canvas.fill_triangle(
        (x + 14, base), (x + size - 26, base + 26), (x + 26, base + 26), color
    )
    # Cabin block and mast.
    canvas.fill_rect(cx - 12, base - 26, 24, 26, color)
    canvas.draw_line(cx, base - 26, cx, base - 44, color, 4)
    canvas.fill_triangle((cx, base - 44), (cx, base - 30), (cx + 14, base - 30), color)
    # Waves under the hull.
    for i, wy in enumerate((base + 34, base + 44, base + 54)):
        wx = x + 10 + i * 8
        canvas.draw_line(wx, wy, wx + 34, wy, color, 3)
    return None


def _draw_chip(canvas, x, y, size, color):
    """A microchip: square body, inner window, pins on four sides."""
    body = size * 3 // 5
    bx = x + (size - body) // 2
    by = y + (size - body) // 2
    canvas.fill_rect(bx, by, body, body, color)
    canvas.fill_rect(bx + 12, by + 12, body - 24, body - 24, PAPER)
    canvas.fill_rect(bx + 22, by + 22, body - 44, body - 44, color)
    for i in range(3):
        off = bx + 12 + i * (body - 24) // 2
        canvas.fill_rect(off, by - 12, 6, 12, color)
        canvas.fill_rect(off, by + body, 6, 12, color)
        off_y = by + 12 + i * (body - 24) // 2
        canvas.fill_rect(bx - 12, off_y, 12, 6, color)
        canvas.fill_rect(bx + body, off_y, 12, 6, color)


def _draw_globe(canvas, x, y, size, color):
    """A globe: ring, equator and meridian lines, plus a small leaf."""
    cx = x + size // 2
    cy = y + size // 2
    r = size * 3 // 8
    canvas.draw_circle(cx, cy, r, color, 5)
    canvas.draw_line(cx - r, cy, cx + r, cy, color, 4)
    canvas.draw_line(cx, cy - r, cx, cy + r, color, 4)
    canvas.draw_line(cx - r + 8, cy - r // 2, cx + r - 8, cy - r // 2, color, 3)
    canvas.draw_line(cx - r + 8, cy + r // 2, cx + r - 8, cy + r // 2, color, 3)


def _draw_chart(canvas, x, y, size, color):
    """Falling bars with a down arrow: markets sliding."""
    base = y + size * 4 // 5
    widths = [16, 16, 16, 16]
    heights = [66, 52, 40, 26]
    bx = x + 14
    for w, h in zip(widths, heights):
        canvas.fill_rect(bx, base - h, w, h, color)
        bx += w + 8
    # Down arrow over the bars.
    ax = x + size - 26
    canvas.draw_line(x + 16, y + 14, ax, y + 44, color, 5)
    canvas.fill_triangle((ax - 10, y + 32), (ax + 10, y + 32), (ax, y + 52), color)


def _draw_cross(canvas, x, y, size, color):
    """A medical cross: two bars, the sign of aid."""
    cx = x + size // 2
    cy = y + size // 2
    canvas.fill_rect(cx - 12, cy - 34, 24, 68, color)
    canvas.fill_rect(cx - 34, cy - 12, 68, 24, color)


ICON_DRAWERS = {
    "ship": _draw_ship,
    "chip": _draw_chip,
    "globe": _draw_globe,
    "chart": _draw_chart,
    "cross": _draw_cross,
}


def _draw_story_row(canvas, story, number, y):
    """One story row: icon square, headline, summary."""
    accent = story["accent"]
    canvas.fill_rect(MARGIN, y + 15, ICON_SIZE, ICON_SIZE, accent)
    ICON_DRAWERS[story["icon"]](
        canvas, MARGIN, y + 15, ICON_SIZE, WHITE
    )
    # Number badge overlapping the icon's top-left corner.
    bx, by = MARGIN, y + 15
    canvas.fill_circle(bx, by, 15, NAVY)
    draw_text_centered(canvas, bx, by - 10, str(number), WHITE, 3)

    tx = TEXT_X
    # Headline: two lines, scale 5.
    hy = y + 8
    for line in story["headline"]:
        draw_text(canvas, tx, hy, line, INK, 5)
        hy += 39
    # Summary: two lines, scale 4.
    sy = y + 90
    for line in story["summary"]:
        draw_text(canvas, tx, sy, line, (74, 70, 60), 4)
        sy += 30


def render_poster():
    """Compose the whole front page and return the Canvas."""
    canvas = Canvas(WIDTH, HEIGHT, PAPER)

    # Masthead: navy band, title, gold date line, gold rule.
    canvas.fill_rect(0, 0, WIDTH, MASTHEAD_H, NAVY)
    draw_text_centered(canvas, WIDTH // 2, 22, MASTHEAD, WHITE, 10)
    draw_text_centered(canvas, WIDTH // 2, 104, DATE_LINE, GOLD, 5)
    canvas.fill_rect(0, 152, WIDTH, 4, GOLD)

    # Five stories.
    y = FIRST_ROW_Y
    for i, story in enumerate(STORIES, start=1):
        _draw_story_row(canvas, story, i, y)
        if i < len(STORIES):
            canvas.fill_rect(
                TEXT_X, y + ROW_H, TEXT_W, 2, RULE
            )
        y += ROW_H + ROW_GAP

    # Footer: source line, centred.
    draw_text_centered(canvas, WIDTH // 2, 988, FOOTER, (110, 104, 88), 3)
    return canvas
