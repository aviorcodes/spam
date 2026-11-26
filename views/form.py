import tkinter as tk
import config as C
from widgets import Card, GradientButton
from database import SUBJECTS


class FormView(tk.Frame):
    def __init__(self, master, app, student=None):
        super().__init__(master, bg=C.BG_DARK)
        self.app = app
        self.student = student
        self.is_edit = student is not None
        self.fields = {}
        self._build()

    def _build(self):
        title = "Edit Student" if self.is_edit else "Add Student"
        head = tk.Frame(self, bg=C.BG_DARK)
        head.pack(fill="x", padx=C.PAD, pady=(C.PAD, 8))
        tk.Label(head, text=title, bg=C.BG_DARK, fg=C.TEXT,
                 font=C.FONT_TITLE).pack(side="left")
        tk.Label(head, text="All fields required",
                 bg=C.BG_DARK, fg=C.TEXT_MUTED,
                 font=C.FONT_SMALL).pack(side="left", padx=12, pady=(10, 0))

        card = Card(self, padding=24)
        card.pack(fill="both", expand=True, padx=C.PAD, pady=(0, C.PAD))
        body = card.inner

        row1 = tk.Frame(body, bg=C.BG_CARD)
        row1.pack(fill="x", pady=(0, 10))
        self._make_entry(row1, "Roll No", "roll_no", 0)
        self._make_entry(row1, "Class", "klass", 1)
        self._make_entry(row1, "Gender", "gender", 2)

        row2 = tk.Frame(body, bg=C.BG_CARD)
        row2.pack(fill="x", pady=(0, 10))
        self._make_entry(row2, "Full Name", "name", 0, width=60)

        tk.Label(body, text="Subject Marks (0 – 100)",
                 bg=C.BG_CARD, fg=C.ACCENT_3,
                 font=C.FONT_H2).pack(anchor="w", pady=(15, 6))

        marks_frame = tk.Frame(body, bg=C.BG_CARD)
        marks_frame.pack(fill="x")
        for i, subj in enumerate(SUBJECTS):
            col = i % 3
            row = i // 3
            self._make_entry(marks_frame, subj, subj.lower(), col, row,
                             width=10, is_marks=True)

        btn_row = tk.Frame(body, bg=C.BG_CARD)
        btn_row.pack(fill="x", pady=(24, 0))
        GradientButton(btn_row,
                       "💾  Save" if not self.is_edit else "💾  Update",
                       command=self._save,
                       width=160).pack(side="left")
        GradientButton(btn_row, "Cancel",
                       command=self.app.show_students,
                       color1=C.BG_CARD_HI, color2=C.BORDER_HI,
                       width=130).pack(side="left", padx=10)

        if self.is_edit:
            self._prefill()

    def _make_entry(self, parent, label, key, col, row=0,
                    width=22, is_marks=False):
        wrap = tk.Frame(parent, bg=C.BG_CARD)
        wrap.grid(row=row, column=col, sticky="w", padx=(0, 20), pady=4)
        tk.Label(wrap, text=label, bg=C.BG_CARD, fg=C.TEXT_MUTED,
                 font=C.FONT_SMALL).pack(anchor="w", pady=(0, 3))
        var = tk.StringVar()
        e = tk.Entry(wrap, textvariable=var, width=width,
                     bg=C.BG_INPUT, fg=C.TEXT,
                     insertbackground=C.ACCENT_3,
                     relief="flat", font=C.FONT_BODY)
        e.pack(ipady=6, padx=2)
        if is_marks:
            e.bind("<KeyRelease>", self._validate_marks)
        self.fields[key] = var

    def _prefill(self):
        s = self.student
        self.fields["roll_no"].set(s.get("roll_no", ""))
        self.fields["name"].set(s.get("name", ""))
        self.fields["klass"].set(s.get("klass", ""))
        self.fields["gender"].set(s.get("gender", "Male"))
        for subj in SUBJECTS:
            self.fields[subj.lower()].set(str(int(s.get(subj.lower(), 0))))

    def _validate_marks(self, event):
        w = event.widget
        v = w.get()
        if v == "":
            return
        try:
            n = float(v)
            if n < 0 or n > 100:
                w.configure(fg=C.DANGER)
            else:
                w.configure(fg=C.TEXT)
        except ValueError:
            w.configure(fg=C.DANGER)

    def _save(self):
        from tkinter import messagebox
        try:
            data = {
                "roll_no": self.fields["roll_no"].get().strip(),
                "name":    self.fields["name"].get().strip(),
                "klass":   self.fields["klass"].get().strip(),
                "gender":  self.fields["gender"].get().strip() or "Other",
            }
            if not data["roll_no"] or not data["name"] or not data["klass"]:
                raise ValueError("Roll No, Name and Class are required.")

            for subj in SUBJECTS:
                raw = self.fields[subj.lower()].get().strip()
                if raw == "":
                    raise ValueError(f"{subj} marks are required.")
                v = float(raw)
                if not 0 <= v <= 100:
                    raise ValueError(f"{subj} marks must be between 0 and 100.")
                data[subj.lower()] = v

            if self.is_edit:
                self.app.db.update(self.student["id"], data)
                self.app.toast(f"Updated {data['name']}", "success")
            else:
                self.app.db.add(data)
                self.app.toast(f"Added {data['name']}", "success")

            self.app.show_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))