import tkinter as tk
import time
import math
import random

LYRICS = [
    (0,    "ako"),
    (0.5,  "ako"),
    (1,    "ako ang bagyooo"),
    (4,    "kulimlim ng langit"),
    (5.8,  "sa inyong dalawa"),
    (8.5,  "bulong ko sa hangin"),
    (10.5, "sana 'di kayo masaya"),
    (14,   "sa tibay ng bahay"),
    (16.3, "na titirhan niyo"),
    (20,   "tatangayin ko bawat yero"),
    (26,   "dilim ng paligid"),
    (28.5, "buhos ng emosyon"),
    (31.7, "tunog ng pag-ibig"),
    (34,   "sa sama ng panahon"),
    (37.2, "sa tibay ng bahay"),
    (40,   "na titirhan niyo"),
    (42.8, "gigibain ko mga pader nyo"),
    (48.5, "dahil ako"),
    (50.5, "ako ang bagyo"),
]

BOX_W, BOX_H     = 350, 300
FONT             = ("Helvetica", 25, "bold")
BG_COLOR         = "#315182"
FG_COLOR         = "#ffffff"
RISE_SPEED       = 109
BOTTOM_SPAWN_OFFSET = 500
STACK_SPACING    = 20

RAIN_DROP_COUNT   = 150
RAIN_SPEED_RANGE  = (400, 800)
RAIN_LENGTH_RANGE = (10, 25)
RAIN_ANGLE        = 10

THUNDER_MIN_INTERVAL  = 4.0
THUNDER_MAX_INTERVAL  = 10.0
THUNDER_FLASH_DURATION = 80
THUNDER_FLASHES       = 3

class RainOverlay:
    def __init__(self, parent, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.parent   = parent
        self.active   = True

        self.win = tk.Toplevel(parent)
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.geometry(f"{screen_w}x{screen_h}+0+0")
        self.win.configure(bg="#000001")
        try:
            self.win.attributes("-transparentcolor", "#000001")
        except tk.TclError:
            pass
        try:
            self.win.attributes("-alpha", 0.55)
        except tk.TclError:
            pass

        self.canvas = tk.Canvas(
            self.win, width=screen_w, height=screen_h,
            bg="#000001", highlightthickness=0
        )
        self.canvas.pack()

        angle_rad        = math.radians(RAIN_ANGLE)
        self.dx_per_dy   = math.tan(angle_rad)

        self.drops = []
        for _ in range(RAIN_DROP_COUNT):
            self._new_drop(random_y=True)

        self.last_time = time.time()
        self._draw()

    def _new_drop(self, random_y=False):
        speed  = random.uniform(*RAIN_SPEED_RANGE)
        length = random.randint(*RAIN_LENGTH_RANGE)
        x      = random.uniform(-50, self.screen_w + 50)
        y      = random.uniform(-self.screen_h, 0) if random_y else random.uniform(-100, -10)
        color  = random.choice(["#A8D8FF", "#C0E8FF", "#7EC8FF", "#FFFFFF"])
        self.drops.append({"x": x, "y": y, "speed": speed, "length": length, "color": color})

    def stop(self):
        self.active = False

    def _draw(self):
        now = time.time()
        dt  = now - self.last_time
        self.last_time = now

        if not self.active:
            self.canvas.delete("rain")
            try:
                self.win.destroy()
            except tk.TclError:
                pass
            return

        self.canvas.delete("rain")

        for drop in self.drops:
            drop["y"] += drop["speed"] * dt
            drop["x"] += drop["speed"] * dt * self.dx_per_dy

            x1, y1 = drop["x"], drop["y"]
            x2 = x1 - drop["length"] * self.dx_per_dy
            y2 = y1 - drop["length"]

            if drop["y"] < self.screen_h + 50:
                self.canvas.create_line(x1, y1, x2, y2,
                                        fill=drop["color"], width=1, tags="rain")
            else:
                drop["x"]      = random.uniform(-50, self.screen_w + 50)
                drop["y"]      = random.uniform(-100, -10)
                drop["speed"]  = random.uniform(*RAIN_SPEED_RANGE)
                drop["length"] = random.randint(*RAIN_LENGTH_RANGE)
                drop["color"]  = random.choice(["#A8D8FF", "#C0E8FF", "#7EC8FF", "#FFFFFF"])

        self.win.after(16, self._draw)


def make_lightning_bolt(x_start, y_start, x_end, y_end,
                        roughness=8, depth=0, max_depth=4):
    if depth >= max_depth:
        return [x_start, y_start, x_end, y_end]
    mid_x  = (x_start + x_end) / 2 + random.uniform(-roughness, roughness)
    mid_y  = (y_start + y_end) / 2
    left   = make_lightning_bolt(x_start, y_start, mid_x, mid_y,
                                  roughness * 0.6, depth + 1, max_depth)
    right  = make_lightning_bolt(mid_x, mid_y, x_end, y_end,
                                  roughness * 0.6, depth + 1, max_depth)
    return left + right[2:]


class LightningBolt:
    def __init__(self, parent, screen_w, screen_h):
        self.win = tk.Toplevel(parent)
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.geometry(f"{screen_w}x{screen_h}+0+0")
        self.win.configure(bg="#000001")
        try:
            self.win.attributes("-transparentcolor", "#000001")
        except tk.TclError:
            pass
        try:
            self.win.attributes("-alpha", 0.95)
        except tk.TclError:
            pass

        self.canvas = tk.Canvas(
            self.win, width=screen_w, height=screen_h,
            bg="#000001", highlightthickness=0
        )
        self.canvas.pack()

        x_start = random.uniform(screen_w * 0.2, screen_w * 0.8)
        y_start = 0
        x_end   = x_start + random.uniform(-screen_w * 0.2, screen_w * 0.2)
        y_end   = random.uniform(screen_h * 0.4, screen_h * 0.85)

        pts = make_lightning_bolt(x_start, y_start, x_end, y_end,
                                   roughness=40, max_depth=5)
        self.canvas.create_line(pts, fill="#FFFFAA", width=6, smooth=False)
        self.canvas.create_line(pts, fill="#FFFFFF", width=2, smooth=False)

        if len(pts) >= 8 and random.random() > 0.4:
            branch_idx = random.randrange(4, len(pts) - 4, 2)
            bx_start = pts[branch_idx];   by_start = pts[branch_idx + 1]
            bx_end   = bx_start + random.uniform(-120, 120)
            by_end   = by_start + random.uniform(80, 200)
            bpts = make_lightning_bolt(bx_start, by_start, bx_end, by_end,
                                        roughness=20, max_depth=3)
            self.canvas.create_line(bpts, fill="#FFFFAA", width=3, smooth=False)
            self.canvas.create_line(bpts, fill="#FFFFFF", width=1, smooth=False)

        self._fade_step = 0
        self._fade()

    def _fade(self):
        self._fade_step += 1
        alpha = max(0.0, 0.95 - self._fade_step * 0.15)
        try:
            self.win.attributes("-alpha", alpha)
        except tk.TclError:
            return
        if alpha > 0:
            self.win.after(40, self._fade)
        else:
            try:
                self.win.destroy()
            except tk.TclError:
                pass


class ThunderFlash:
    def __init__(self, parent, screen_w, screen_h):
        self.win = tk.Toplevel(parent)
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.geometry(f"{screen_w}x{screen_h}+0+0")
        self.win.configure(bg="#E8F4FF")
        try:
            self.win.attributes("-alpha", 0.0)
        except tk.TclError:
            pass
        self._flash_count = 0
        self._max_flashes = THUNDER_FLASHES * 2
        self._do_flash()

    def _do_flash(self):
        if self._flash_count >= self._max_flashes:
            try:
                self.win.destroy()
            except tk.TclError:
                pass
            return
        alpha = 0.35 if self._flash_count % 2 == 0 else 0.0
        try:
            self.win.attributes("-alpha", alpha)
        except tk.TclError:
            pass
        self._flash_count += 1
        self.win.after(THUNDER_FLASH_DURATION, self._do_flash)


class LightningApp:
    def __init__(self, root):
        self.root     = root
        self.screen_w = root.winfo_screenwidth()
        self.screen_h = root.winfo_screenheight()
        self.active   = True
        self._schedule_next()

    def _schedule_next(self):
        if not self.active:
            return
        delay = int(random.uniform(THUNDER_MIN_INTERVAL, THUNDER_MAX_INTERVAL) * 1000)
        self.root.after(delay, self._strike)

    def _strike(self):
        if not self.active:
            return
        ThunderFlash(self.root, self.screen_w, self.screen_h)
        self.root.after(80, lambda: LightningBolt(self.root, self.screen_w, self.screen_h))
        self._schedule_next()

    def stop(self):
        self.active = False


class LyricCard:
    def __init__(self, parent, text, x, y):
        self.win = tk.Toplevel(parent)
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.configure(bg=BG_COLOR)
        self.win.geometry(f"{BOX_W}x{BOX_H}+{int(x)}+{int(y)}")
        self.win.resizable(False, False)
        self.full_text = text
        self.label = tk.Label(
            self.win,
            text="",
            font=FONT,
            bg=BG_COLOR,
            fg=FG_COLOR,
            wraplength=BOX_W - 25,
            justify="center",
        )
        self.label.pack(expand=True, fill="both", padx=15, pady=15)
        self.typewriter_index = 0
        self.x = x
        self.y = float(y)
        self.typewriter()

    def typewriter(self):
        if self.typewriter_index <= len(self.full_text):
            self.label.config(text=self.full_text[: self.typewriter_index])
            self.typewriter_index += 1
            self.win.after(70, self.typewriter)

    def rise(self, dy):
        self.y -= dy
        self.win.geometry(f"{BOX_W}x{BOX_H}+{int(self.x)}+{int(self.y)}")

    def is_offscreen(self):
        return self.y + BOX_H < -50


class LyricFloatApp:
    def __init__(self, root, on_done=None):
        self.root         = root
        self.screen_w     = root.winfo_screenwidth()
        self.screen_h     = root.winfo_screenheight()
        self.next_lyric_idx = 0
        self.boxes        = []
        self.last_frame_time = None
        self.current_side = "left"
        self.on_done      = on_done

    def random_safe_x(self):
        center_x = self.screen_w // 2
        spacing  = BOX_W + 60
        left_x   = center_x - spacing
        right_x  = center_x + 60
        if self.current_side == "left":
            self.current_side = "right"
            return left_x
        else:
            self.current_side = "left"
            return right_x

    def lowest_y(self):
        if not self.boxes:
            return self.screen_h - BOX_H - BOTTOM_SPAWN_OFFSET
        return max(box.y for box in self.boxes) + BOX_H + STACK_SPACING

    def start(self):
        self.start_time      = time.time()
        self.last_frame_time = self.start_time
        self.tick()

    def tick(self):
        now     = time.time()
        elapsed = now - self.start_time
        dt      = now - self.last_frame_time
        self.last_frame_time = now

        while (
            self.next_lyric_idx < len(LYRICS)
            and LYRICS[self.next_lyric_idx][0] <= elapsed
        ):
            t, text = LYRICS[self.next_lyric_idx]
            x   = self.random_safe_x()
            y   = self.lowest_y()
            box = LyricCard(self.root, text, x, y)
            self.boxes.append(box)
            self.next_lyric_idx += 1

        dy = RISE_SPEED * dt
        for box in self.boxes:
            box.rise(dy)

        still_visible = []
        for box in self.boxes:
            if box.is_offscreen():
                try:
                    box.win.destroy()
                except tk.TclError:
                    pass
            else:
                still_visible.append(box)
        self.boxes = still_visible

        if self.next_lyric_idx < len(LYRICS) or self.boxes:
            self.root.after(16, self.tick)
        else:
            if self.on_done:
                self.on_done()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    rain = RainOverlay(root, screen_w, screen_h)

    lightning = LightningApp(root)

    def on_lyrics_done():
        rain.stop()
        lightning.stop()
        root.after(500, root.quit)

    lyrics_app = LyricFloatApp(root, on_done=on_lyrics_done)
    lyrics_app.start()

    root.mainloop()
