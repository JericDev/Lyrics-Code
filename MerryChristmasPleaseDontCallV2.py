import tkinter as tk
import math
import random

# ---------------- config ----------------
W, H = 620, 320
BG = "#05060D"

lyrics = [
    ("You know it's true", 0.07, 2.3),
    ("Yeah i miss you", 0.08, 3.2),
    ("You know it's true", 0.09, 3.1),
    ("So, What if i call?", 0.06, 2.7),
    ("And you pick up the phone", 0.06, 2.9),
    ("And i use this holiday", 0.06, 1.8),
    ("To make my way to your ghost", 0.08, 3.4),
    ("Oh, what if you're lonely?", 0.07, 2.9),
    ("You know i am too", 0.06, 2.8),
    ("And i get the chance to say", 0.05, 2.4),
    ("Merry Christmas i miss you", 0.08, 3.8),
    ("I MISS YOU", 0.09, 1.4),
]

root = tk.Tk()
root.title("Merry Christmas I miss you")
root.configure(bg=BG)
root.resizable(False, False)

sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{W}x{H}+{(sw - W) // 2}+{(sh - H) // 2}")

canvas = tk.Canvas(root, width=W, height=H, bg=BG, highlightthickness=0)
canvas.pack()

label = tk.Label(root, text="", font=("Helvetica", 22, "bold"),
                 fg="#FFFFFF", bg=BG, wraplength=W - 80, justify="center")
label.place(relx=0.5, rely=0.5, anchor="center")

# ---------------- particles ----------------
particles = []


def create_particles(num=150):
    for _ in range(num):
        x = random.randint(0, W)
        y = random.randint(-H, H)
        kind = random.choices(
            ["raindrop", "snow", "sparkle", "butterfly"],
            weights=[45, 25, 25, 5]
        )[0]

        if kind == "raindrop":
            length = random.randint(8, 15)
            item = canvas.create_line(
                x, y, x, y + length, width=1,
                fill=random.choice(["#87CEFA", "#4682B4", "#B0C4DE"])
            )
            particles.append({"id": item, "kind": kind,
                              "len": length, "speed": random.uniform(4, 8)})

        elif kind == "snow":
            size = random.randint(2, 6)
            item = canvas.create_text(
                x, y, text="❆", font=("Helvetica", size),
                fill=random.choice(["#FFF8DC", "#F0FFFF", "#D3D3D3"])
            )
            particles.append({"id": item, "kind": kind,
                              "speed": random.uniform(0.6, 1.6),
                              "drift": random.uniform(-0.4, 0.4)})

        elif kind == "sparkle":
            size = random.randint(2, 6)
            item = canvas.create_text(
                x, y, text="✦", font=("Helvetica", size),
                fill=random.choice(["#304379", "#6D68A1", "#3E6579"])
            )
            particles.append({"id": item, "kind": kind,
                              "speed": random.uniform(0.3, 1.0),
                              "drift": random.uniform(-0.3, 0.3)})

        else:  # butterfly
            size = random.randint(3, 6)
            item = canvas.create_text(
                x, y, text="🦋", font=("Helvetica", size + 4),
                fill=random.choice(["#7571B8", "#4F448B", "#FFF8DC"])
            )
            particles.append({"id": item, "kind": kind,
                              "speed": random.uniform(0.5, 1.2),
                              "t": random.uniform(0, math.tau)})


def animate_particles():
    for p in particles:
        item, kind = p["id"], p["kind"]

        if kind == "raindrop":
            canvas.move(item, 0, p["speed"])
            _, y1, _, _ = canvas.coords(item)
            if y1 > H:
                nx = random.randint(0, W)
                canvas.coords(item, nx, -p["len"], nx, 0)

        elif kind == "butterfly":
            p["t"] += 0.08
            canvas.move(item, math.sin(p["t"]) * 1.8, p["speed"] * 0.7)
            _, y = canvas.coords(item)
            if y > H + 20:
                canvas.coords(item, random.randint(0, W), -20)

        else:  # snow / sparkle
            canvas.move(item, p["drift"], p["speed"])
            x, y = canvas.coords(item)
            if y > H + 20:
                canvas.coords(item, random.randint(0, W), -10)
            elif x < -20:
                canvas.coords(item, W + 20, y)
            elif x > W + 20:
                canvas.coords(item, -20, y)

    root.after(30, animate_particles)


def twinkle_particles():
    palette = ["#7571B8", "#4F448B", "#FFF8DC", "#6D68A1", "#B0C4DE"]
    for p in particles:
        if p["kind"] in ("snow", "sparkle"):
            canvas.itemconfig(p["id"], fill=random.choice(palette))
    root.after(450, twinkle_particles)


# ---------------- glow ----------------
GLOW_A = (255, 255, 255)   # bright
GLOW_B = (150, 160, 255)   # cool blue


def glow_effect(t=0.0):
    k = (math.sin(t) + 1) / 2
    r, g, b = (int(a + (c - a) * k) for a, c in zip(GLOW_A, GLOW_B))
    label.config(fg=f"#{r:02x}{g:02x}{b:02x}")
    root.after(40, glow_effect, t + 0.08)


# ---------------- typewriter (main thread) ----------------
def typewriter(loop=True):
    state = {"line": 0, "char": 0, "phase": "typing"}

    def step():
        li = state["line"]
        if li >= len(lyrics):
            if loop:
                state.update(line=0, char=0, phase="typing")
                root.after(1200, step)
            return

        line, char_delay, line_delay = lyrics[li]

        if state["phase"] == "typing":
            state["char"] += 1
            label.config(text=line[:state["char"]])
            if state["char"] >= len(line):
                state["phase"] = "hold"
                root.after(int(line_delay * 1000), step)
            else:
                root.after(int(char_delay * 1000), step)
        else:  # hold finished -> clear and move on
            label.config(text="")
            state.update(line=li + 1, char=0, phase="typing")
            root.after(250, step)

    step()


# ---------------- go ----------------
create_particles(150)
animate_particles()
twinkle_particles()
glow_effect()
root.after(500, typewriter)

root.mainloop()
