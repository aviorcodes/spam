import tkinter as tk
import config as C


def rounded_rect(canvas, x1, y1, x2, y2, r=16, **kw):
    pts = [
        x1+r, y1, x2-r, y1, x2, y1, x2, y1+r,
        x2, y2-r, x2, y2, x2-r, y2, x1+r, y2,
        x1, y2, x1, y2-r, x1, y1+r, x1, y1,
    ]
    return canvas.create_polygon(pts, smooth=True, **kw)


class Card(tk.Frame):
    def __init__(self, master, bg=C.BG_CARD, border=C.BORDER,
                 radius=C.RADIUS, padding=16):
        super().__init__(master, bg=master["bg"])
        self._radius = radius
        self._bg     = bg
        self._border = border
        self._win    = None
        self.padding = padding
        self.canvas = tk.Canvas(self, bg=master["bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.inner = tk.Frame(self.canvas, bg=bg)
        self._win = self.canvas.create_window(
            padding, padding, anchor="nw", window=self.inner)
        self.bind("<Configure>", self._redraw)

    def _redraw(self, _=None):
        try:
            self.canvas.delete("bg")
        except tk.TclError:
            return
        w, h = self.winfo_width(), self.winfo_height()
        if w < 4 or h < 4:
            return
        rounded_rect(self.canvas, 2, 2, w-2, h-2,
                     r=self._radius, fill=self._bg,
                     outline=self._border, width=1, tags="bg")
        self.canvas.coords(self._win, self.padding, self.padding)
        self.canvas.itemconfigure(self._win,
                                  width=max(1, w - 2 * self.padding),
                                  height=max(1, h - 2 * self.padding))
        self.canvas.tag_lower("bg")


class GradientButton(tk.Frame):
    def __init__(self, master, text, command=None,
                 width=180, height=42,
                 color1=C.ACCENT, color2=C.ACCENT_2,
                 fg="white", radius=12):
        super().__init__(master, bg=master["bg"])
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.configure(width=width, height=height)

        # NEVER name any attribute starting with _w — Tkinter reserves it.
        self.bw, self.bh, self.br = width, height, radius
        self.c1, self.c2, self.fg_text = color1, color2, fg
        self._cmd  = command
        self._text = text

        self.canvas = tk.Canvas(self, bg=master["bg"],
                                highlightthickness=0, cursor="hand2")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Enter>",    lambda e: self._draw(hover=True))
        self.canvas.bind("<Leave>",    lambda e: self._draw(hover=False))
        self.canvas.bind("<Button-1>", lambda e: command() if command else None)
        self.after(10, lambda: self._draw(hover=False))

    def _draw(self, hover):
        c = self.canvas
        try:
            c.delete("all")
        except tk.TclError:
            return
        for i in range(self.bh):
            t = i / max(1, self.bh)
            r = int(int(self.c1[1:3], 16)*(1-t) + int(self.c2[1:3], 16)*t)
            g = int(int(self.c1[3:5], 16)*(1-t) + int(self.c2[3:5], 16)*t)
            b = int(int(self.c1[5:7], 16)*(1-t) + int(self.c2[5:7], 16)*t)
            c.create_line(0, i, self.bw, i, fill=f"#{r:02x}{g:02x}{b:02x}")
        for (x, y) in [(0,0), (self.bw,0), (0,self.bh), (self.bw,self.bh)]:
            c.create_oval(x-self.br, y-self.br,
                          x+self.br, y+self.br,
                          fill=self.master["bg"], outline="")
        if hover:
            rounded_rect(c, 1, 1, self.bw-1, self.bh-1,
                         r=self.br, fill="", outline="white", width=1)
        c.create_text(self.bw/2, self.bh/2, text=self._text,
                      fill=self.fg_text,
                      font=(C.FONT_FAMILY, 10, "bold"))


class Toast(tk.Toplevel):
    def __init__(self, master, message, kind="info", duration=2200):
        super().__init__(master)
        self.overrideredirect(True)
        color = {"info":    C.INFO,
                 "success": C.SUCCESS,
                 "error":   C.DANGER,
                 "warning": C.WARNING}.get(kind, C.INFO)
        f = tk.Frame(self, bg=color, padx=14, pady=10)
        f.pack()
        tk.Label(f, text=message, bg=color, fg="white",
                 font=(C.FONT_FAMILY, 10, "bold")).pack()
        self.update_idletasks()
        w = self.winfo_width()
        x = master.winfo_rootx() + master.winfo_width() - w - 30
        y0 = master.winfo_rooty() + 30
        self.geometry(f"+{x+w}+{y0}")
        self._slide(x, y0, duration)

    def _slide(self, x_target, y, duration):
        x = self.winfo_x()
        steps = 15
        def step(i=0):
            if i > steps:
                self.after(duration, self._fade_out)
                return
            x_new = x + (x_target - x) * (i / steps)
            self.geometry(f"+{int(x_new)}+{y}")
            self.after(12, lambda: step(i+1))
        step()

    def _fade_out(self, alpha=1.0):
        if alpha <= 0:
            self.destroy()
            return
        try:
            self.attributes("-alpha", alpha)
        except Exception:
            pass
        self.after(30, lambda: self._fade_out(alpha - 0.1))


def badge(master, text, color):
    return tk.Label(master, text=f" {text} ", bg=color, fg="white",
                    font=(C.FONT_FAMILY, 8, "bold"), padx=6, pady=2)