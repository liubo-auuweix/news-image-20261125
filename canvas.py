"""A small RGB canvas: a flat pixel buffer plus the shapes the poster
needs. Coordinates are clipped to the canvas, so drawing outside the
edges is harmless. Everything here is integer math, so the picture is
identical on every run.
"""


class Canvas:
    def __init__(self, width, height, background):
        self.width = width
        self.height = height
        self.pixels = bytearray(background * (width * height))

    def set_pixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            i = (y * self.width + x) * 3
            self.pixels[i] = color[0]
            self.pixels[i + 1] = color[1]
            self.pixels[i + 2] = color[2]

    def fill_rect(self, x, y, w, h, color):
        """Fill the rectangle with corners (x, y) and (x+w, y+h)."""
        x0 = max(x, 0)
        y0 = max(y, 0)
        x1 = min(x + w, self.width)
        y1 = min(y + h, self.height)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.width + x0) * 3
            self.pixels[i : i + len(row)] = row

    def draw_rect(self, x, y, w, h, color, thickness=1):
        """Outline of a rectangle, `thickness` pixels wide."""
        self.fill_rect(x, y, w, thickness, color)
        self.fill_rect(x, y + h - thickness, w, thickness, color)
        self.fill_rect(x, y, thickness, h, color)
        self.fill_rect(x + w - thickness, y, thickness, h, color)

    def draw_line(self, x0, y0, x1, y1, color, thickness=1):
        """Bresenham line, drawn `thickness` pixels wide."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        half = thickness // 2
        while True:
            self.fill_rect(x0 - half, y0 - half, thickness, thickness, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def fill_circle(self, cx, cy, r, color):
        """Filled disc centred on (cx, cy) with radius r."""
        for dy in range(-r, r + 1):
            half = int((r * r - dy * dy) ** 0.5)
            self.fill_rect(cx - half, cy + dy, half * 2 + 1, 1, color)

    def draw_circle(self, cx, cy, r, color, thickness=1):
        """Ring centred on (cx, cy) with radius r."""
        for t in range(thickness):
            rr = r - t
            if rr <= 0:
                break
            steps = max(8, rr * 6)
            for s in range(steps):
                import math

                a = 2 * math.pi * s / steps
                px = cx + int(rr * math.cos(a))
                py = cy + int(rr * math.sin(a))
                self.set_pixel(px, py, color)

    def fill_triangle(self, p0, p1, p2, color):
        """Filled triangle from three (x, y) points, scanline by scanline."""
        points = sorted([p0, p1, p2], key=lambda p: p[1])
        (x0, y0), (x1, y1), (x2, y2) = points
        if y0 == y2:
            return
        for y in range(y0, y2 + 1):
            xa = self._interp_x(x0, y0, x2, y2, y)
            if y < y1:
                xb = self._interp_x(x0, y0, x1, y1, y)
            else:
                xb = self._interp_x(x1, y1, x2, y2, y)
            if xa > xb:
                xa, xb = xb, xa
            self.fill_rect(xa, y, xb - xa + 1, 1, color)

    @staticmethod
    def _interp_x(x0, y0, x1, y1, y):
        if y1 == y0:
            return x0
        return x0 + (x1 - x0) * (y - y0) // (y1 - y0)

    def to_bytes(self):
        return bytes(self.pixels)
