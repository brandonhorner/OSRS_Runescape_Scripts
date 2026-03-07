import re
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

import pyautogui
from screen_interactor import ScreenInteractor


def extract_area_labels(source_path: Path):
    """Extract area dict keys from ScreenInteractor.get_scan_area()."""
    text = source_path.read_text(encoding="utf-8")
    block_match = re.search(r"areas\s*=\s*\{(.*?)\n\s*\}", text, re.DOTALL)
    if not block_match:
        return []
    block = block_match.group(1)
    labels = re.findall(r'"([^"]+)"\s*:\s*\(', block)
    return sorted(set(labels))


class OverlayWindow:
    def __init__(self, root, width, height):
        self.root = root
        self.width = width
        self.height = height
        self.window = None

    def show(self, area_label, region, duration_ms=1800):
        if self.window is not None:
            self.window.destroy()
            self.window = None

        x, y, w, h = region
        x2 = x + w
        y2 = y + h

        self.window = tk.Toplevel(self.root)
        self.window.title("Area Overlay")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.geometry(f"{self.width}x{self.height}+0+0")

        bg_key = "#010101"
        self.window.configure(bg=bg_key)
        try:
            # Windows color-key transparency.
            self.window.wm_attributes("-transparentcolor", bg_key)
        except tk.TclError:
            # Fallback for platforms without transparent color support.
            self.window.attributes("-alpha", 0.25)

        canvas = tk.Canvas(self.window, width=self.width, height=self.height, highlightthickness=0, bg=bg_key)
        canvas.pack(fill="both", expand=True)
        canvas.create_rectangle(x, y, x2, y2, outline="#00ff66", width=3)
        text = f"{area_label}: ({x}, {y}, {w}, {h})"
        canvas.create_text(x + 8, max(12, y - 10), text=text, anchor="sw", fill="#00ff66", font=("Consolas", 11, "bold"))

        self.window.after(duration_ms, self._safe_destroy)

    def _safe_destroy(self):
        if self.window is not None:
            self.window.destroy()
            self.window = None


class AreaOverlayTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ScreenInteractor Area Overlay Tool")
        self.root.geometry("500x640")
        self.root.attributes("-topmost", True)

        self.interactor = ScreenInteractor()
        screen_w, screen_h = pyautogui.size()
        self.overlay = OverlayWindow(self.root, screen_w, screen_h)

        source_path = Path(__file__).with_name("screen_interactor.py")
        self.area_labels = extract_area_labels(source_path)
        self.filtered_labels = list(self.area_labels)

        self._build_ui()
        self._refresh_listbox()

    def _build_ui(self):
        header = tk.Label(
            self.root,
            text="Click an area to show overlay for search region",
            font=("Segoe UI", 11, "bold"),
            padx=10,
            pady=10,
        )
        header.pack(anchor="w")

        search_frame = tk.Frame(self.root, padx=10, pady=4)
        search_frame.pack(fill="x")
        tk.Label(search_frame, text="Filter:", font=("Segoe UI", 10)).pack(side="left")

        self.filter_var = tk.StringVar()
        self.filter_var.trace_add("write", lambda *_: self._apply_filter())
        filter_entry = tk.Entry(search_frame, textvariable=self.filter_var, font=("Consolas", 10))
        filter_entry.pack(side="left", fill="x", expand=True, padx=(8, 0))
        filter_entry.focus_set()

        list_frame = tk.Frame(self.root, padx=10, pady=6)
        list_frame.pack(fill="both", expand=True)

        self.listbox = tk.Listbox(list_frame, font=("Consolas", 10))
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", lambda _: self.show_selected())
        self.listbox.bind("<Double-Button-1>", lambda _: self.show_selected())

        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.configure(yscrollcommand=scrollbar.set)

        actions = tk.Frame(self.root, padx=10, pady=8)
        actions.pack(fill="x")

        tk.Button(actions, text="Show Overlay", command=self.show_selected).pack(side="left")
        tk.Button(actions, text="Close Overlay", command=self.overlay._safe_destroy).pack(side="left", padx=(8, 0))
        tk.Button(actions, text="Refresh Areas", command=self.refresh_areas).pack(side="left", padx=(8, 0))
        tk.Button(actions, text="Exit", command=self.root.destroy).pack(side="right")

        self.status_var = tk.StringVar(value="")
        status = tk.Label(self.root, textvariable=self.status_var, anchor="w", padx=10, pady=8, fg="#333333")
        status.pack(fill="x")

    def refresh_areas(self):
        source_path = Path(__file__).with_name("screen_interactor.py")
        self.area_labels = extract_area_labels(source_path)
        self._apply_filter()
        self.status_var.set(f"Reloaded {len(self.area_labels)} areas.")

    def _apply_filter(self):
        query = self.filter_var.get().strip().lower()
        if not query:
            self.filtered_labels = list(self.area_labels)
        else:
            self.filtered_labels = [label for label in self.area_labels if query in label.lower()]
        self._refresh_listbox()

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for label in self.filtered_labels:
            self.listbox.insert(tk.END, label)
        if self.filtered_labels:
            self.listbox.selection_set(0)

    def show_selected(self):
        selected = self.listbox.curselection()
        if not selected:
            return
        label = self.filtered_labels[selected[0]]
        try:
            region = self.interactor.get_scan_area(label)
            self.overlay.show(label, region)
            self.status_var.set(f"Overlay: {label} -> {region}")
        except Exception as exc:
            messagebox.showerror("Overlay Error", f"Could not compute area for '{label}':\n{exc}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    tool = AreaOverlayTool()
    tool.run()
