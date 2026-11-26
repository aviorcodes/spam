import tkinter as tk
import config as C
from widgets import Card
from analysis import to_df, stats
from charts import subject_bar, pass_pie, top_students_bar


class DashboardView(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg=C.BG_DARK)
        self.app = app
        self._build()

    def _build(self):
        head = tk.Frame(self, bg=C.BG_DARK)
        head.pack(fill="x", padx=C.PAD, pady=(C.PAD, 8))
        tk.Label(head, text="Dashboard", bg=C.BG_DARK, fg=C.TEXT,
                 font=C.FONT_TITLE).pack(side="left")
        tk.Label(head, text="Real-time performance overview",
                 bg=C.BG_DARK, fg=C.TEXT_MUTED,
                 font=C.FONT_SMALL).pack(side="left", padx=12, pady=(10, 0))

        df = to_df(self.app.db.all())
        st = stats(df)

        kpis = tk.Frame(self, bg=C.BG_DARK)
        kpis.pack(fill="x", padx=C.PAD, pady=8)
        data = [
            ("Total Students", st["students"], C.ACCENT_3, "🎓"),
            ("Class Average",  f"{st['avg']}%", C.INFO, "📈"),
            ("Highest Score",  f"{st['high']}%", C.SUCCESS, "🏅"),
            ("Pass Rate",      f"{st['pass_rate']}%",
             C.SUCCESS if st["pass_rate"] >= 40 else C.DANGER, "✅"),
        ]
        for i, (t, v, c, icon) in enumerate(data):
            card = Card(kpis, bg=C.BG_CARD, border=c)
            card.grid(row=0, column=i, sticky="nsew", padx=6)
            tk.Label(card.inner, text=f"{icon}  {t}",
                     bg=C.BG_CARD, fg=C.TEXT_MUTED,
                     font=C.FONT_SMALL).pack(anchor="w")
            tk.Label(card.inner, text=str(v), bg=C.BG_CARD, fg=c,
                     font=(C.FONT_FAMILY, 26, "bold")).pack(anchor="w", pady=(4, 0))
        for i in range(4):
            kpis.grid_columnconfigure(i, weight=1)
        kpis.configure(height=110)
        kpis.pack_propagate(False)

        if st.get("top"):
            t = st["top"]
            banner = tk.Frame(self, bg=C.BG_CARD,
                              highlightbackground=C.GOLD,
                              highlightthickness=1)
            banner.pack(fill="x", padx=C.PAD, pady=8)
            tk.Label(banner,
                     text=f"🏆   Class Topper:   {t['name']}  ({t['roll_no']})",
                     bg=C.BG_CARD, fg=C.GOLD,
                     font=(C.FONT_FAMILY, 12, "bold")).pack(side="left", padx=14, pady=10)
            tk.Label(banner,
                     text=f"Total: {int(t['total'])}   •   {t['percentage']}%   •   Grade {t['grade']}",
                     bg=C.BG_CARD, fg=C.TEXT,
                     font=C.FONT_BODY).pack(side="left", padx=8)

        if df.empty:
            card = Card(self, bg=C.BG_CARD)
            card.pack(fill="both", expand=True, padx=C.PAD, pady=C.PAD)
            tk.Label(card.inner, text="📊", bg=C.BG_CARD, fg=C.TEXT_MUTED,
                     font=(C.FONT_FAMILY, 60)).pack(pady=(40, 10))
            tk.Label(card.inner, text="No data yet",
                     bg=C.BG_CARD, fg=C.TEXT,
                     font=C.FONT_H1).pack()
            tk.Label(card.inner, text="Click 'Add Student' in the sidebar to begin.",
                     bg=C.BG_CARD, fg=C.TEXT_MUTED,
                     font=C.FONT_BODY).pack(pady=(4, 40))
            return

        row = tk.Frame(self, bg=C.BG_DARK)
        row.pack(fill="both", expand=True, padx=C.PAD, pady=8)
        left = Card(row); left.pack(side="left", fill="both", expand=True, padx=(0, 6))
        right = Card(row); right.pack(side="left", fill="both", expand=True, padx=(6, 0))
        subject_bar(left.inner, st)
        pass_pie(right.inner, st)

        card = Card(self)
        card.pack(fill="both", expand=True, padx=C.PAD, pady=(8, C.PAD))
        top_students_bar(card.inner, df)