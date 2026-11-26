import tkinter as tk
from tkinter import ttk
import config as C
from widgets import Card
from analysis import to_df, stats, class_wise_summary
from database import SUBJECTS


class AnalyticsView(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg=C.BG_DARK)
        self.app = app
        self._build()

    def _build(self):
        head = tk.Frame(self, bg=C.BG_DARK)
        head.pack(fill="x", padx=C.PAD, pady=(C.PAD, 8))
        tk.Label(head, text="Analytics", bg=C.BG_DARK, fg=C.TEXT,
                 font=C.FONT_TITLE).pack(side="left")
        tk.Label(head, text="Deep performance insights",
                 bg=C.BG_DARK, fg=C.TEXT_MUTED,
                 font=C.FONT_SMALL).pack(side="left", padx=12, pady=(10, 0))

        df = to_df(self.app.db.all())
        if df.empty:
            card = Card(self)
            card.pack(fill="both", expand=True, padx=C.PAD, pady=C.PAD)
            tk.Label(card.inner, text="No data to analyze",
                     bg=C.BG_CARD, fg=C.TEXT_MUTED,
                     font=C.FONT_H1).pack(pady=40)
            return

        st = stats(df)

        cls_card = Card(self, padding=16)
        cls_card.pack(fill="x", padx=C.PAD, pady=(0, 10))
        tk.Label(cls_card.inner, text="Class-wise Summary",
                 bg=C.BG_CARD, fg=C.ACCENT_3,
                 font=C.FONT_H2).pack(anchor="w", pady=(0, 8))

        cls_df = class_wise_summary(df)
        style = ttk.Style()
        style.configure("Summary.Treeview",
                        background=C.BG_CARD, fieldbackground=C.BG_CARD,
                        foreground=C.TEXT, rowheight=26, borderwidth=0)
        style.configure("Summary.Treeview.Heading",
                        background=C.BG_CARD_HI, foreground=C.ACCENT_3,
                        font=(C.FONT_FAMILY, 9, "bold"), borderwidth=0)
        cols = ("Class", "Students", "Avg %", "Avg Total", "Pass Rate %")
        tree = ttk.Treeview(cls_card.inner, columns=cols, show="headings",
                            height=min(len(cls_df), 8), style="Summary.Treeview")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=140, anchor="center")
        for _, r in cls_df.iterrows():
            tree.insert("", "end", values=(
                r["klass"], int(r["students"]),
                f"{r['avg_pct']:.1f}", f"{r['avg_total']:.0f}",
                f"{r['pass_rate']:.1f}"))
        tree.pack(fill="x")

        sub_card = Card(self, padding=16)
        sub_card.pack(fill="both", expand=True, padx=C.PAD, pady=(0, C.PAD))
        tk.Label(sub_card.inner, text="Subject Leaderboard",
                 bg=C.BG_CARD, fg=C.ACCENT_3,
                 font=C.FONT_H2).pack(anchor="w", pady=(0, 8))

        row = tk.Frame(sub_card.inner, bg=C.BG_CARD)
        row.pack(fill="x")
        for i, subj in enumerate(SUBJECTS):
            col = tk.Frame(row, bg=C.BG_PANEL, padx=12, pady=10)
            col.grid(row=0, column=i, sticky="nsew", padx=4)
            tk.Label(col, text=subj, bg=C.BG_PANEL, fg=C.TEXT,
                     font=(C.FONT_FAMILY, 10, "bold")).pack(anchor="w")
            tk.Label(col, text=f"Avg: {st['subject_avg'][subj]}",
                     bg=C.BG_PANEL, fg=C.INFO, font=C.FONT_SMALL).pack(anchor="w", pady=(4, 0))
            tk.Label(col, text=f"High: {st['subject_high'][subj]:.0f}",
                     bg=C.BG_PANEL, fg=C.SUCCESS, font=C.FONT_SMALL).pack(anchor="w")
            tk.Label(col, text=f"Low:  {st['subject_low'][subj]:.0f}",
                     bg=C.BG_PANEL, fg=C.DANGER, font=C.FONT_SMALL).pack(anchor="w")
        for i in range(len(SUBJECTS)):
            row.grid_columnconfigure(i, weight=1)