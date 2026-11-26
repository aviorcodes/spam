import tkinter as tk
from tkinter import ttk
import config as C
from widgets import Card, GradientButton
from analysis import to_df


GRADE_COLORS = {
    "A+": C.SUCCESS, "A": C.INFO, "B": C.ACCENT_3,
    "C": C.WARNING, "F": C.DANGER,
}


class StudentsView(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg=C.BG_DARK)
        self.app = app
        self.search_var = tk.StringVar()
        self._build()

    def _build(self):
        head = tk.Frame(self, bg=C.BG_DARK)
        head.pack(fill="x", padx=C.PAD, pady=(C.PAD, 8))
        tk.Label(head, text="Students", bg=C.BG_DARK, fg=C.TEXT,
                 font=C.FONT_TITLE).pack(side="left")
        GradientButton(head, "➕  Add Student",
                       command=self.app.show_add_form,
                       width=160).pack(side="right")

        search_card = Card(self, padding=10)
        search_card.pack(fill="x", padx=C.PAD, pady=(0, 8), ipady=4)
        row = tk.Frame(search_card.inner, bg=C.BG_CARD)
        row.pack(fill="x")
        tk.Label(row, text="🔎", bg=C.BG_CARD, fg=C.ACCENT_3,
                 font=(C.FONT_FAMILY, 14)).pack(side="left", padx=(4, 8))
        e = tk.Entry(row, textvariable=self.search_var,
                     bg=C.BG_INPUT, fg=C.TEXT,
                     insertbackground=C.ACCENT_3,
                     relief="flat", font=C.FONT_BODY)
        e.pack(side="left", fill="x", expand=True, ipady=6, padx=4)
        e.bind("<KeyRelease>", lambda _: self._fill())
        self.entry = e

        wrap = Card(self, padding=0)
        wrap.pack(fill="both", expand=True, padx=C.PAD, pady=(0, C.PAD))
        inner = wrap.inner

        style = ttk.Style()
        style.configure("Luxe.Treeview",
                        background=C.BG_CARD, fieldbackground=C.BG_CARD,
                        foreground=C.TEXT, rowheight=32,
                        borderwidth=0, font=C.FONT_BODY)
        style.configure("Luxe.Treeview.Heading",
                        background=C.BG_CARD_HI, foreground=C.ACCENT_3,
                        font=(C.FONT_FAMILY, 9, "bold"),
                        borderwidth=0, relief="flat", padding=8)
        style.map("Luxe.Treeview",
                  background=[("selected", C.ACCENT)],
                  foreground=[("selected", "white")])

        cols = ("ID", "Roll", "Name", "Class", "Gender",
                "Math", "Sci", "Eng", "Comp", "Soc",
                "Total", "Percent", "Grade", "Result", "Rank")
        self.tree = ttk.Treeview(inner, columns=cols, show="headings",
                                 style="Luxe.Treeview")
        widths = [40, 70, 150, 70, 70, 55, 55, 55, 60, 55, 60, 75, 60, 70, 55]
        for c, w in zip(cols, widths):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor="center")
        vs = ttk.Scrollbar(inner, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vs.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vs.pack(side="right", fill="y")

        self.tree.tag_configure("pass", background=C.BG_CARD)
        self.tree.tag_configure("fail", background="#3a0f12")

        self.tree.bind("<Double-1>", lambda _: self._edit_selected())

        btn_row = tk.Frame(self, bg=C.BG_DARK)
        btn_row.pack(fill="x", padx=C.PAD, pady=(0, C.PAD))
        GradientButton(btn_row, "✏️  Edit",
                       command=self._edit_selected,
                       width=130).pack(side="left", padx=(0, 8))
        GradientButton(btn_row, "🗑️  Delete",
                       command=self._delete_selected,
                       color1=C.DANGER, color2="#b91c1c",
                       width=130).pack(side="left")

        self._fill()

    def _fill(self):
        if not hasattr(self, "tree"):
            return
        self.tree.delete(*self.tree.get_children())
        kw = self.search_var.get().strip()
        records = self.app.db.search(kw) if kw else self.app.db.all()
        df = to_df(records)
        if df.empty:
            return
        for _, r in df.iterrows():
            tag = "fail" if r["result"] == "Fail" else "pass"
            self.tree.insert("", "end", values=(
                int(r["id"]), r["roll_no"], r["name"], r["klass"], r["gender"],
                int(r["math"]), int(r["science"]), int(r["english"]),
                int(r["computer"]), int(r["social"]),
                int(r["total"]), f"{r['percentage']}%",
                r["grade"], r["result"], int(r["rank"]),
            ), tags=(tag,))

    def _get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return int(self.tree.item(sel[0])["values"][0])

    def _edit_selected(self):
        sid = self._get_selected_id()
        if sid:
            self.app.show_edit_form(sid)

    def _delete_selected(self):
        from tkinter import messagebox
        sid = self._get_selected_id()
        if not sid:
            messagebox.showinfo("Select", "Please select a student first.")
            return
        if messagebox.askyesno("Confirm", "Delete this student?"):
            self.app.db.delete(sid)
            self.app.show_students()
            self.app.toast("Student deleted", "success")