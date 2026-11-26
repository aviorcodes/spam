import tkinter as tk
import config as C
from widgets import Toast
from database import Database

from views.dashboard import DashboardView
from views.students  import StudentsView
from views.form      import FormView


class App:
    def __init__(self, root):
        self.root = root
        self.db   = Database()

        self._build_sidebar()
        self.body = tk.Frame(root, bg=C.BG_DARK)
        self.body.pack(side="left", fill="both", expand=True)

        self.show_dashboard()

    def _build_sidebar(self):
        bar = tk.Frame(self.root, bg=C.BG_PANEL, width=C.SIDEBAR_W)
        bar.pack(side="left", fill="y")
        bar.pack_propagate(False)

        logo = tk.Frame(bar, bg=C.BG_PANEL)
        logo.pack(fill="x", pady=(24, 30), padx=20)
        tk.Label(logo, text="🎓", bg=C.BG_PANEL, fg=C.ACCENT_3,
                 font=(C.FONT_FAMILY, 24)).pack(anchor="w")
        tk.Label(logo, text="SMRAS Pro", bg=C.BG_PANEL, fg=C.TEXT,
                 font=(C.FONT_FAMILY, 16, "bold")).pack(anchor="w")
        tk.Label(logo, text="Student Management\n& Result Analysis",
                 bg=C.BG_PANEL, fg=C.TEXT_MUTED,
                 font=C.FONT_SMALL, justify="left").pack(anchor="w")

        self._nav_btn(bar, "📊   Dashboard",   self.show_dashboard)
        self._nav_btn(bar, "👥   Students",    self.show_students)
        self._nav_btn(bar, "➕   Add Student", self.show_add_form)
        self._nav_btn(bar, "📈   Analytics",   self.show_analytics)
        self._nav_btn(bar, "⚙️   Settings",    self.show_settings)

        tk.Frame(bar, bg=C.BG_PANEL).pack(expand=True)

        self._nav_btn(bar, "📤   Export CSV", self.export_csv)

        tk.Label(bar, text="v1.0   •   Python 3.14",
                 bg=C.BG_PANEL, fg=C.TEXT_DIM,
                 font=C.FONT_TINY).pack(pady=10)

    def _nav_btn(self, parent, text, cmd):
        b = tk.Button(parent, text=text, command=cmd,
                      bg=C.BG_PANEL, fg=C.TEXT,
                      activebackground=C.BG_CARD,
                      activeforeground=C.ACCENT_3,
                      relief="flat", anchor="w",
                      font=(C.FONT_FAMILY, 10),
                      padx=22, pady=10, bd=0, cursor="hand2")
        b.pack(fill="x", padx=8, pady=2)
        b.bind("<Enter>", lambda _: b.config(bg=C.BG_CARD))
        b.bind("<Leave>", lambda _: b.config(bg=C.BG_PANEL))

    def _clear(self):
        for w in self.body.winfo_children():
            w.destroy()

    def show_dashboard(self):
        self._clear()
        DashboardView(self.body, self).pack(fill="both", expand=True)

    def show_students(self):
        self._clear()
        StudentsView(self.body, self).pack(fill="both", expand=True)

    def show_add_form(self):
        self._clear()
        FormView(self.body, self).pack(fill="both", expand=True)

    def show_analytics(self):
        from views.analytics import AnalyticsView
        self._clear()
        AnalyticsView(self.body, self).pack(fill="both", expand=True)

    def show_settings(self):
        from views.settings import SettingsView
        self._clear()
        SettingsView(self.body, self).pack(fill="both", expand=True)

    def show_edit_form(self, student_id):
        student = self.db.get(student_id)
        if not student:
            return
        self._clear()
        FormView(self.body, self, student=student).pack(fill="both", expand=True)

    def toast(self, message, kind="info"):
        try:
            Toast(self.root, message, kind=kind)
        except Exception:
            pass

    def export_csv(self):
        from tkinter import filedialog, messagebox
        from analysis import to_df, export_csv as _export
        records = self.db.all()
        if not records:
            messagebox.showinfo("Export", "No students to export.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="students_export.csv")
        if not path:
            return
        _export(to_df(records), path)
        self.toast("Exported successfully", "success")