import tkinter as tk
import config as C
from gui import App


def main():
    root = tk.Tk()
    root.title("SMRAS Pro — Student Management & Result Analysis")
    root.geometry("1280x760")
    root.minsize(1100, 700)
    root.configure(bg=C.BG_DARK)
    try:
        root.iconbitmap(default="")
    except Exception:
        pass
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()