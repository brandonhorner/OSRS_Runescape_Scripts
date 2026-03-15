import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

import pyautogui

from screen_interactor import ScreenInteractor


PROFILE_FILE = Path(__file__).with_name("scan_area_profiles.json")


def deterministic_color(label):
    base = sum(ord(c) for c in label)
    r = 80 + (base * 37) % 175
    g = 80 + (base * 53) % 175
    b = 80 + (base * 97) % 175
    return f"#{r:02x}{g:02x}{b:02x}"


def load_profiles():
    if not PROFILE_FILE.exists():
        return {"profiles": {}}
    try:
        return json.loads(PROFILE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"profiles": {}}


def save_profiles(data):
    PROFILE_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


class AreaOverlayTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Scan Area Overlay Editor")
        self.root.geometry("560x760")
        self.root.attributes("-topmost", True)

        self.screen_w, self.screen_h = pyautogui.size()
        # Prefer runelite_closed profile when available for this resolution
        if (self.screen_w, self.screen_h) == (1920, 1080):
            self.default_profile_name = "1920x1080_runelite_closed"
        else:
            self.default_profile_name = f"{self.screen_w}x{self.screen_h}"

        self.interactor = ScreenInteractor()
        self.base_areas = self.interactor.get_all_scan_areas(include_overrides=False)
        self.areas = dict(self.base_areas)
        self.labels = sorted(self.base_areas.keys())
        self.filtered_labels = list(self.labels)
        self.visible_labels = set()

        self.drag_mode = None
        self.drag_label = None
        self.drag_start = None
        self.drag_orig_region = None
        self.item_to_label = {}
        self.item_type = {}

        self._build_overlay_canvas()
        self._build_controls()
        self._load_profile(self.default_profile_name)
        self._refresh_listbox()

    def _build_overlay_canvas(self):
        self.overlay = tk.Toplevel(self.root)
        self.overlay.title("Overlay")
        self.overlay.overrideredirect(True)
        self.overlay.attributes("-topmost", True)
        self.overlay.geometry(f"{self.screen_w}x{self.screen_h}+0+0")

        bg_key = "#010101"
        self.overlay.configure(bg=bg_key)
        try:
            self.overlay.wm_attributes("-transparentcolor", bg_key)
        except tk.TclError:
            self.overlay.attributes("-alpha", 0.25)

        self.canvas = tk.Canvas(self.overlay, width=self.screen_w, height=self.screen_h, highlightthickness=0, bg=bg_key)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self._on_canvas_press)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_canvas_release)

    def _build_controls(self):
        tk.Label(self.root, text="Scan Area Overlay Editor", font=("Segoe UI", 12, "bold"), padx=10, pady=8).pack(anchor="w")

        profile_row = tk.Frame(self.root, padx=10, pady=4)
        profile_row.pack(fill="x")
        tk.Label(profile_row, text="Profile:", width=8, anchor="w").pack(side="left")
        self.profile_var = tk.StringVar(value=self.default_profile_name)
        tk.Entry(profile_row, textvariable=self.profile_var, font=("Consolas", 10)).pack(side="left", fill="x", expand=True)
        tk.Button(profile_row, text="Load", command=self._load_profile_from_input).pack(side="left", padx=(8, 0))
        tk.Button(profile_row, text="Save", command=self._save_profile).pack(side="left", padx=(8, 0))

        filter_row = tk.Frame(self.root, padx=10, pady=4)
        filter_row.pack(fill="x")
        tk.Label(filter_row, text="Filter:", width=8, anchor="w").pack(side="left")
        self.filter_var = tk.StringVar()
        self.filter_var.trace_add("write", lambda *_: self._apply_filter())
        tk.Entry(filter_row, textvariable=self.filter_var, font=("Consolas", 10)).pack(side="left", fill="x", expand=True)

        list_frame = tk.Frame(self.root, padx=10, pady=6)
        list_frame.pack(fill="both", expand=True)
        self.listbox = tk.Listbox(list_frame, font=("Consolas", 10), selectmode=tk.EXTENDED)
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", lambda _: self._update_status_for_selection())

        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.configure(yscrollcommand=scrollbar.set)

        action_row_1 = tk.Frame(self.root, padx=10, pady=4)
        action_row_1.pack(fill="x")
        tk.Button(action_row_1, text="Show Selected", command=self._show_selected).pack(side="left")
        tk.Button(action_row_1, text="Hide Selected", command=self._hide_selected).pack(side="left", padx=(8, 0))
        tk.Button(action_row_1, text="Show All", command=self._show_all).pack(side="left", padx=(8, 0))
        tk.Button(action_row_1, text="Hide All", command=self._hide_all).pack(side="left", padx=(8, 0))

        action_row_2 = tk.Frame(self.root, padx=10, pady=4)
        action_row_2.pack(fill="x")
        self.edit_enabled = tk.BooleanVar(value=True)
        tk.Checkbutton(action_row_2, text="Enable Drag Edit", variable=self.edit_enabled).pack(side="left")
        tk.Button(action_row_2, text="Reset Selected To Default", command=self._reset_selected_to_default).pack(side="left", padx=(12, 0))
        tk.Button(action_row_2, text="Exit", command=self._close).pack(side="right")

        help_text = (
            "Overlay interactions:\n"
            "- Drag inside a box to move.\n"
            "- Drag the small square (bottom-right) to resize.\n"
            "- Save writes only changed areas for this profile."
        )
        tk.Label(self.root, text=help_text, justify="left", fg="#333333", padx=10, pady=8).pack(anchor="w")

        self.status_var = tk.StringVar(value="")
        tk.Label(self.root, textvariable=self.status_var, anchor="w", padx=10, pady=8, fg="#1f1f1f").pack(fill="x")

    def _apply_filter(self):
        query = self.filter_var.get().strip().lower()
        if not query:
            self.filtered_labels = list(self.labels)
        else:
            self.filtered_labels = [label for label in self.labels if query in label.lower()]
        self._refresh_listbox()

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for label in self.filtered_labels:
            self.listbox.insert(tk.END, label)
        if self.filtered_labels:
            self.listbox.selection_set(0)
            self._update_status_for_selection()

    def _selected_labels(self):
        return [self.filtered_labels[i] for i in self.listbox.curselection()]

    def _show_selected(self):
        for label in self._selected_labels():
            self.visible_labels.add(label)
        self._render_overlay()

    def _hide_selected(self):
        for label in self._selected_labels():
            self.visible_labels.discard(label)
        self._render_overlay()

    def _show_all(self):
        self.visible_labels = set(self.labels)
        self._render_overlay()

    def _hide_all(self):
        self.visible_labels.clear()
        self._render_overlay()

    def _reset_selected_to_default(self):
        selected = self._selected_labels()
        if not selected:
            return
        for label in selected:
            self.areas[label] = tuple(self.base_areas[label])
        self._render_overlay()
        self.status_var.set(f"Reset {len(selected)} selected area(s) to default.")

    def _render_overlay(self):
        self.canvas.delete("all")
        self.item_to_label.clear()
        self.item_type.clear()

        for label in sorted(self.visible_labels):
            if label not in self.areas:
                continue
            x, y, w, h = self.areas[label]
            color = deterministic_color(label)
            rect = self.canvas.create_rectangle(x, y, x + w, y + h, outline=color, width=2)
            text = self.canvas.create_text(x + 6, max(12, y - 6), text=label, anchor="sw", fill=color, font=("Consolas", 10, "bold"))
            handle = self.canvas.create_rectangle(x + w - 7, y + h - 7, x + w + 7, y + h + 7, fill=color, outline=color)

            self.item_to_label[rect] = label
            self.item_to_label[text] = label
            self.item_to_label[handle] = label
            self.item_type[rect] = "rect"
            self.item_type[text] = "text"
            self.item_type[handle] = "handle"

    def _on_canvas_press(self, event):
        if not self.edit_enabled.get():
            return
        hits = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if not hits:
            return
        top_item = hits[-1]
        label = self.item_to_label.get(top_item)
        item_type = self.item_type.get(top_item)
        if not label or label not in self.areas:
            return

        self.drag_label = label
        self.drag_start = (event.x, event.y)
        self.drag_orig_region = self.areas[label]
        if item_type == "handle":
            self.drag_mode = "resize"
        else:
            self.drag_mode = "move"

    def _on_canvas_drag(self, event):
        if not self.drag_mode or not self.drag_label or not self.drag_start or not self.drag_orig_region:
            return

        sx, sy = self.drag_start
        ox, oy, ow, oh = self.drag_orig_region
        dx = event.x - sx
        dy = event.y - sy

        if self.drag_mode == "move":
            nx = max(0, min(ox + dx, self.screen_w - 1))
            ny = max(0, min(oy + dy, self.screen_h - 1))
            nx = min(nx, self.screen_w - max(5, ow))
            ny = min(ny, self.screen_h - max(5, oh))
            self.areas[self.drag_label] = (int(nx), int(ny), int(ow), int(oh))
        elif self.drag_mode == "resize":
            nw = max(5, min(self.screen_w - ox, ow + dx))
            nh = max(5, min(self.screen_h - oy, oh + dy))
            self.areas[self.drag_label] = (int(ox), int(oy), int(nw), int(nh))

        self._render_overlay()
        self.status_var.set(f"{self.drag_label}: {self.areas[self.drag_label]}")

    def _on_canvas_release(self, _event):
        self.drag_mode = None
        self.drag_label = None
        self.drag_start = None
        self.drag_orig_region = None

    def _load_profile_from_input(self):
        profile = self.profile_var.get().strip()
        if not profile:
            messagebox.showerror("Invalid Profile", "Profile name cannot be empty.")
            return
        self._load_profile(profile)

    def _load_profile(self, profile_name):
        data = load_profiles()
        profile = data.get("profiles", {}).get(profile_name, {})
        self.areas = dict(self.base_areas)
        for label, region in profile.items():
            if label in self.areas and isinstance(region, (list, tuple)) and len(region) == 4:
                self.areas[label] = tuple(int(v) for v in region)

        self.visible_labels = set(self.labels)
        self._render_overlay()
        self.status_var.set(f"Loaded profile '{profile_name}' with {len(profile)} override(s).")

    def _save_profile(self):
        profile_name = self.profile_var.get().strip()
        if not profile_name:
            messagebox.showerror("Invalid Profile", "Profile name cannot be empty.")
            return

        overrides = {}
        for label, region in self.areas.items():
            if tuple(region) != tuple(self.base_areas[label]):
                overrides[label] = [int(v) for v in region]

        data = load_profiles()
        if "profiles" not in data or not isinstance(data["profiles"], dict):
            data["profiles"] = {}
        data["profiles"][profile_name] = overrides
        save_profiles(data)
        self.status_var.set(f"Saved profile '{profile_name}' with {len(overrides)} override(s) to {PROFILE_FILE.name}.")

    def _update_status_for_selection(self):
        selected = self._selected_labels()
        if not selected:
            return
        label = selected[0]
        self.status_var.set(f"{label}: {self.areas.get(label)}")

    def _close(self):
        try:
            self.overlay.destroy()
        except Exception:
            pass
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    AreaOverlayTool().run()
