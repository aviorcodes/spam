import tkinter as tk
from tkinter import messagebox, filedialog
import shutil
import config as C
from widgets import Card, GradientButton


class SettingsView(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg=C.BG_DARK)
        self.app = app
        self._build()

    def _build(self):
        head = tk.Frame(self, bg=C.BG_DARK)
        head.pack(fill="x", padx=C.PAD, pady=(C.PAD, 8))
        tk.Label(head, text="Settings", bg=C.BG_DARK, fg=C.TEXT,
                 font=C.FONT_TITLE).pack(side="left")

        card1 = Card(self, padding=20)
        card1.pack(fill="x", padx=C.PAD, pady=(0, 10))
        tk.Label(card1.inner, text="Database Backup",
                 bg=C.BG_CARD, fg=C.ACCENT_3,
                 font=C.FONT_H2).pack(anchor="w")
        tk.Label(card1.inner, text="Save a copy of students.db to a safe location.",
                 bg=C.BG_CARD, fg=C.TEXT_MUTED,
                 font=C.FONT_BODY).pack(anchor="w", pady=(4, 10))
        GradientButton(card1.inner, "💾  Backup Database",
                       command=self._backup, width=200).pack(anchor="w")

        card2 = Card(self, padding=20)
        card2.pack(fill="x", padx=C.PAD, pady=(0, 10))
        tk.Label(card2.inner, text="Restore Database",
                 bg=C.BG_CARD, fg=C.ACCENT_3,
                 font=C.FONT_H2).pack(anchor="w")
        tk.Label(card2.inner, text="Replace current data with a backup file. Use with caution.",
                 bg=C.BG_CARD, fg=C.TEXT_MUTED,
                 font=C.FONT_BODY).pack(anchor="w", pady=(4, 10))
        GradientButton(card2.inner, "📥  Restore from Backup",
                       command=self._restore,
                       color1=C.WARNING, color2="#d97706",
                       width=220).pack(anchor="w")

        card3 = Card(self, padding=20)
        card3.pack(fill="both", expand=True, padx=C.PAD, pady=(0, C.PAD))
        tk.Label(card3.inner, text="About SMRAS Pro",
                 bg=C.BG_CARD, fg=C.ACCENT_3,
                 font=C.FONT_H2).pack(anchor="w")
        about = (
            "SMRAS Pro v1.0\n"
            "Student Management & Result Analysis System\n\n"
            "Built with:  Python 3.12+ | Tkinter | SQLite | NumPy | Pandas | Matplotlib\n"
            "Theme:  Deep Space Luxe\n\n"
            "Features:\n"
            "• Add / edit / delete / search student records\n"
            "• Automatic total, percentage, grade, rank, pass/fail\n"
            "• Real-time dashboards with charts and KPIs\n"
            "• Class-wise analytics\n"
            "• CSV export\n"
            "• Database backup / restore\n\n"
            "Developed by:  Shruti Jha"
        )
        tk.Label(card3.inner, text=about, bg=C.BG_CARD, fg=C.TEXT,
                 font=C.FONT_BODY, justify="left").pack(anchor="w", pady=(8, 0))

    def _backup(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("SQLite DB", "*.db")],
            initialfile="students_backup.db")
        if not path:
            return
        try:
            shutil.copyfile(self.app.db.db_name, path)
            self.app.toast("Database backed up", "success")
        except Exception as e:
            messagebox.showerror("Backup failed", str(e))

    def _restore(self):
        path = filedialog.askopenfilename(
            filetypes=[("SQLite DB", "*.db")])
        if not path:
            return
        if not messagebox.askyesno("Confirm",
                "This will replace the current database. Continue?"):
            return
        try:
            shutil.copyfile(path, self.app.db.db_name)
            self.app.toast("Database restored", "success")
            self.app.show_dashboard()
        except Exception as e:
            messagebox.showerror("Restore failed", str(e))