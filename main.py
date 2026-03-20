# Pygame sorting visualizer — web-compatible via Pygbag
# By Seth Robinson https://github.com/sethrobinson29
import asyncio
import json
import time
import pygame
from sorter import Sorter
from theme import *
from theme import _IX, _IY, _font, _make_bg_tile, _make_bg_surf
from widgets import Button, Slider, Checkbox, Dropdown
from info_modal import InfoModal, ALGO_ORDER

try:
    import js as _js
    _WEB = True
except ImportError:
    _js = None
    _WEB = False

TTL_MS = 30 * 24 * 3600 * 1000   # 1-month localStorage TTL

# ── module-level constants ─────────────────────────────────────────────────────
SORT_OPTIONS = [
    ("Bubble",    "bubble"),
    ("Cocktail",  "cocktail"),
    ("Comb",      "comb"),
    ("Cycle",     "cycle"),
    ("Gnome",     "gnome"),
    ("Heap",      "heap"),
    ("Insertion", "insertion"),
    ("Merge",     "merge"),
    ("Quick",     "quick"),
    ("Radix",     "radix"),
    ("Selection", "selection"),
    ("Shell",     "shell"),
    ("Tim",       "tim"),
]

DISPATCH_MAP = {
    "bubble":    "bubbleSort",
    "selection": "selectionSort",
    "merge":     "mergeSortWrap",
    "quick":     "quickSortWrap",
    "radix":     "radixSort",
    "insertion": "insertionSort",
    "heap":      "heapSort",
    "shell":     "shellSort",
    "tim":       "timSort",
    "cocktail":  "cocktailSort",
    "comb":      "combSort",
    "gnome":     "gnomeSort",
    "cycle":     "cycleSort",
}

PALETTES = {
    "default": [pygame.Color(c) for c in [
        "#FF4400", "#FFCC00", "#88CC00", "#00CC00", "#00FF80",
        "#00FFFF", "#00CFFF", "#0080FF", "#0000FF", "#000080",
    ]],
    "phosphor": [pygame.Color(c) for c in [
        "#001800", "#003300", "#005500", "#007700", "#009900",
        "#00BB00", "#00DD00", "#33FF33", "#77FF77", "#AAFFAA",
    ]],
}


# ── saved palette I/O ─────────────────────────────────────────────────────────
def _validate_palette_data(data, result):
    """Validate a raw JSON list into result[]. Returns True if any entries were invalid."""
    needs_resave = False
    if not isinstance(data, list):
        return False
    for i, slot in enumerate(data[:NUM_SLOTS]):
        if slot is None:
            continue
        if not isinstance(slot, list) or not slot:
            needs_resave = True
            continue
        colors, valid = [], True
        for triplet in slot:
            if (isinstance(triplet, list) and len(triplet) == 3
                    and all(isinstance(v, int) and 0 <= v <= 255 for v in triplet)):
                colors.append(pygame.Color(triplet[0], triplet[1], triplet[2]))
            else:
                valid = False
                break
        if valid and colors:
            result[i] = colors
        else:
            needs_resave = True
    return needs_resave


def _load_palettes():
    """Read saved palettes; return list of NUM_SLOTS entries (each None or list[Color]).
    Uses localStorage (with 1-month TTL) in browser, JSON file natively.
    Any invalid entry is dropped and storage is re-saved."""
    result = [None] * NUM_SLOTS
    needs_resave = False
    try:
        if _WEB:
            raw = _js.localStorage.getItem("palettes")
            if not raw:
                return result
            parsed = json.loads(raw)
            ts = parsed.get("ts", 0)
            if int(time.time() * 1000) - ts > TTL_MS:
                _js.localStorage.removeItem("palettes")
                return result
            data = parsed.get("data", [])
        else:
            with open(SAVE_FILE) as f:
                data = json.load(f)
        needs_resave = _validate_palette_data(data, result)
    except Exception:
        pass
    if needs_resave:
        _save_palettes(result)
    return result


def _save_palettes(saved_slots):
    """Persist saved_slots. Uses localStorage with TTL timestamp in browser, JSON file natively."""
    try:
        data = [[[c.r, c.g, c.b] for c in slot] if slot else None
                for slot in saved_slots]
        if _WEB:
            payload = json.dumps({"ts": int(time.time() * 1000), "data": data})
            _js.localStorage.setItem("palettes", payload)
        else:
            with open(SAVE_FILE, "w") as f:
                json.dump(data, f)
    except Exception:
        pass


# ── Win95 tab helper ──────────────────────────────────────────────────────────
def _draw_tab(surf, rect, active):
    """Draw a single Win95-style tab. Active tab omits the bottom border."""
    r = pygame.Rect(rect)
    surf.fill(WIN_GRAY, r)
    pygame.draw.line(surf, WIN_LIGHT,  r.topleft,              (r.right - 1, r.top))
    pygame.draw.line(surf, WIN_LIGHT,  r.topleft,              (r.left,      r.bottom - 1))
    pygame.draw.line(surf, WIN_DARK,   (r.right - 2, r.top + 1), (r.right - 2, r.bottom - 1))
    pygame.draw.line(surf, WIN_DARKER, (r.right - 1, r.top),   (r.right - 1, r.bottom - 1))
    if not active:
        pygame.draw.line(surf, WIN_DARK,   (r.left + 1, r.bottom - 2), (r.right - 2, r.bottom - 2))
        pygame.draw.line(surf, WIN_DARKER, r.bottomleft,               (r.right - 1, r.bottom - 1))


# ── ColorPickerModal ──────────────────────────────────────────────────────────
class ColorPickerModal:
    W, H, TITLE_H, TAB_H = 500, 350, 22, 22

    def __init__(self, btn_font, comp_font):
        self.btn_font  = btn_font
        self.comp_font = comp_font
        self.is_open   = False

        mx = (WIN_W - self.W) // 2
        my = (WIN_H - self.H) // 2
        self.rect = pygame.Rect(mx, my, self.W, self.H)

        self.tab_colors   = [None] * NUM_SLOTS   # per-tab working palettes
        self.active_tab   = 0
        self.working_colors = [pygame.Color(128, 128, 128)] * 5
        self.selected_slot  = 0                  # which color entry is being edited

        # pre-render title bar gradient
        _gw = self.W - 4
        self._title_grad = pygame.Surface((_gw, self.TITLE_H))
        for i in range(_gw):
            t = i / max(_gw - 1, 1)
            c = (int(WIN_NAVY[0] + t * (WIN_NAVY2[0] - WIN_NAVY[0])),
                 int(WIN_NAVY[1] + t * (WIN_NAVY2[1] - WIN_NAVY[1])),
                 int(WIN_NAVY[2] + t * (WIN_NAVY2[2] - WIN_NAVY[2])))
            pygame.draw.line(self._title_grad, c, (i, 0), (i, self.TITLE_H - 1))

        # dim overlay
        self._overlay = pygame.Surface((WIN_W, WIN_H))
        self._overlay.set_alpha(80)
        self._overlay.fill((0, 0, 0))

        # tab strip geometry
        self._tab_y = my + self.TITLE_H + 8          # absolute y of tab row
        self._tab_w = (self.W - 8) // NUM_SLOTS      # = 98px each

        # content top — below tab strip
        ct = self._tab_y + self.TAB_H
        self._ct = ct

        # count dropdown
        count_opts = [(str(i), str(i)) for i in range(1, 11)]
        self.count_dd = Dropdown(pygame.Rect(mx + 72, ct, 50, 22), count_opts, comp_font)
        self.count_dd.selected = 4   # default 5 colors

        # pick-color inset
        self._inset_rect = pygame.Rect(mx + 14, ct + 60, 380, 126)

        # RGB sliders (label 18px above track; R label at ct+74, 14px from inset top)
        sx, sw = mx + 22, 218
        self.r_slider = Slider((sx, ct + 92,  sw, 14), comp_font, 0, 255, 1, 128, "R")
        self.g_slider = Slider((sx, ct + 126, sw, 14), comp_font, 0, 255, 1, 128, "G")
        self.b_slider = Slider((sx, ct + 160, sw, 14), comp_font, 0, 255, 1, 128, "B")

        # live swatch (inside inset, right of sliders)
        self._swatch_rect = pygame.Rect(mx + 252, ct + 64, 124, 114)

        # full-palette preview
        self._preview_label_y = ct + 200
        self._preview_y       = ct + 216
        self._preview_x       = mx + 14
        self._preview_total_w = self.W - 28

        # OK / Cancel
        btn_y = ct + 248
        self.ok_btn     = Button((mx + self.W - 184, btn_y, 80, 26), "OK",     "ok",     btn_font)
        self.cancel_btn = Button((mx + self.W -  96, btn_y, 80, 26), "Cancel", "cancel", btn_font)

        # title-bar X button
        self._x_btn = pygame.Rect(self.rect.right - 4 - 20,
                                  self.rect.y + 3 + (self.TITLE_H - 16) // 2, 20, 16)

    # ── geometry helpers ──────────────────────────────────────────────────────
    def _tab_rect(self, i):
        return pygame.Rect(self.rect.x + 4 + i * self._tab_w,
                           self._tab_y, self._tab_w, self.TAB_H)

    def _pal_slot_rect(self, i):
        return pygame.Rect(self.rect.x + 14 + i * 24, self._ct + 30, 20, 20)

    # ── preview ───────────────────────────────────────────────────────────────
    def preview_colors(self):
        """Working colors with the current slider value substituted for the selected slot."""
        colors = list(self.working_colors)
        if self.selected_slot < len(colors):
            colors[self.selected_slot] = self._live_color()
        return colors

    # ── colour helpers ────────────────────────────────────────────────────────
    def _live_color(self):
        return pygame.Color(self.r_slider.value, self.g_slider.value, self.b_slider.value)

    def _sync_sliders(self):
        c = self.working_colors[self.selected_slot]
        self.r_slider.value = c.r
        self.g_slider.value = c.g
        self.b_slider.value = c.b

    def _read_sliders(self):
        self.working_colors[self.selected_slot] = self._live_color()

    # ── tab management ────────────────────────────────────────────────────────
    def _save_tab(self):
        self._read_sliders()
        self.tab_colors[self.active_tab] = list(self.working_colors)

    def _load_tab(self):
        tab = self.tab_colors[self.active_tab]
        if tab is not None:
            self.working_colors = [pygame.Color(c.r, c.g, c.b) for c in tab]
            n = len(self.working_colors)
            for j, (lbl, _) in enumerate(self.count_dd.options):
                if lbl == str(n):
                    self.count_dd.selected = j
                    break
        else:
            self.working_colors = [pygame.Color(128, 128, 128)] * 5
            self.count_dd.selected = 4
        self.count_dd.open = False
        self.selected_slot = min(self.selected_slot, len(self.working_colors) - 1)
        self._sync_sliders()

    # ── lifecycle ─────────────────────────────────────────────────────────────
    def open(self, saved_slots):
        self.tab_colors = [
            [pygame.Color(c.r, c.g, c.b) for c in slot] if slot else None
            for slot in saved_slots
        ]
        self.active_tab    = 0
        self.selected_slot = 0
        self._load_tab()
        self.is_open = True

    def close(self):
        self.is_open = False

    # ── draw ──────────────────────────────────────────────────────────────────
    def draw(self, screen, font):
        screen.blit(self._overlay, (0, 0))
        draw_raised(screen, self.rect)

        # title bar
        screen.blit(self._title_grad, (self.rect.x + 2, self.rect.y + 2))
        title_txt = font.render("Custom Palette", False, WIN_WHITE)
        screen.blit(title_txt, title_txt.get_rect(
            midleft=(self.rect.x + 10, self.rect.y + 2 + self.TITLE_H // 2)))
        draw_raised(screen, self._x_btn)
        xt = self.btn_font.render("X", False, WIN_TEXT)
        screen.blit(xt, xt.get_rect(center=self._x_btn.center))

        # tab separator line (drawn first; active tab covers its portion)
        sep_y = self._tab_y + self.TAB_H - 1
        pygame.draw.line(screen, WIN_DARKER,
                         (self.rect.x + 2, sep_y), (self.rect.right - 3, sep_y))

        # inactive tabs (slightly smaller and lower)
        for i in range(NUM_SLOTS):
            if i == self.active_tab:
                continue
            tr = self._tab_rect(i)
            _draw_tab(screen, (tr.x + 1, tr.y + 2, tr.w - 1, tr.h - 2), active=False)
            has = self.tab_colors[i] is not None
            lbl = font.render(f"Slot {i + 1}", False, WIN_TEXT if has else WIN_DARK)
            screen.blit(lbl, lbl.get_rect(center=(tr.x + tr.w // 2, tr.y + 2 + (tr.h - 2) // 2)))

        # active tab (full height, covers separator line at bottom)
        tr = self._tab_rect(self.active_tab)
        _draw_tab(screen, (tr.x - 1, tr.y, tr.w + 1, tr.h + 1), active=True)
        screen.fill(WIN_GRAY, pygame.Rect(tr.x, sep_y, tr.w - 1, 2))  # erase separator under tab
        has = self.tab_colors[self.active_tab] is not None
        lbl = font.render(f"Slot {self.active_tab + 1}", False, WIN_TEXT if has else WIN_DARK)
        screen.blit(lbl, lbl.get_rect(center=(tr.x + tr.w // 2, tr.y + tr.h // 2)))

        ct = self._ct

        # "Colors:" label + color entry slots
        clbl = self.comp_font.render("Colors:", False, WIN_TEXT)
        screen.blit(clbl, (self.rect.x + 14, ct + 4))
        for i in range(len(self.working_colors)):
            sr = self._pal_slot_rect(i)
            c  = self._live_color() if i == self.selected_slot else self.working_colors[i]
            (draw_sunken if i == self.selected_slot else draw_raised)(screen, sr, c)

        # pick-color inset + sliders
        draw_sunken(screen, self._inset_rect)
        self.r_slider.draw(screen)
        self.g_slider.draw(screen)
        self.b_slider.draw(screen)

        # live swatch
        live = self._live_color()
        pygame.draw.rect(screen, live, self._swatch_rect)
        pygame.draw.rect(screen, WIN_DARKER, self._swatch_rect, 1)

        # full-palette preview
        n   = len(self.working_colors)
        sw  = max(1, self._preview_total_w // n)
        screen.blit(self.comp_font.render("Preview:", False, WIN_TEXT),
                    (self._preview_x, self._preview_label_y))
        for i, c in enumerate(self.working_colors):
            col = live if i == self.selected_slot else c
            pr  = pygame.Rect(self._preview_x + i * sw, self._preview_y, sw, 18)
            pygame.draw.rect(screen, col, pr)
            pygame.draw.rect(screen, WIN_DARKER, pr, 1)

        self.ok_btn.draw(screen)
        self.cancel_btn.draw(screen)
        self.count_dd.draw(screen)   # last so open list renders on top

    # ── events ────────────────────────────────────────────────────────────────
    def handle_event(self, event):
        # count dropdown first
        prev_sel = self.count_dd.selected
        if self.count_dd.handle_event(event):
            if not self.count_dd.open and self.count_dd.selected != prev_sel:
                new_n = int(self.count_dd.options[self.count_dd.selected][0])
                self._read_sliders()
                while len(self.working_colors) < new_n:
                    self.working_colors.append(pygame.Color(self.working_colors[-1]))
                self.working_colors = self.working_colors[:new_n]
                self.selected_slot  = min(self.selected_slot, new_n - 1)
                self._sync_sliders()
            return None

        self.r_slider.handle_event(event)
        self.g_slider.handle_event(event)
        self.b_slider.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # tab clicks
            for i in range(NUM_SLOTS):
                if self._tab_rect(i).collidepoint(event.pos) and i != self.active_tab:
                    self._save_tab()
                    self.active_tab = i
                    self._load_tab()
                    return None

            # palette entry slot clicks
            for i in range(len(self.working_colors)):
                if self._pal_slot_rect(i).collidepoint(event.pos) and i != self.selected_slot:
                    self._read_sliders()
                    self.selected_slot = i
                    self._sync_sliders()
                    return None

            if self._x_btn.collidepoint(event.pos):
                return "cancel"
            if self.ok_btn.is_clicked(event.pos):
                self._save_tab()
                return "ok"
            if self.cancel_btn.is_clicked(event.pos):
                return "cancel"

        return None


# ── helpers ───────────────────────────────────────────────────────────────────
async def cancel_task(task_ref):
    if task_ref[0] is not None and not task_ref[0].done():
        task_ref[0].cancel()
        try:
            await task_ref[0]
        except asyncio.CancelledError:
            pass
    task_ref[0] = None


async def run_sort(sorter, action, task_ref):
    await cancel_task(task_ref)
    if action in DISPATCH_MAP:
        method = getattr(sorter, DISPATCH_MAP[action])
        task_ref[0] = asyncio.create_task(method())


def draw_ui(screen, sorter, sort_surf, buttons, desc_cb, dropdown,
            size_slider, vol_slider, font, comp_font, title_grad, bg_surf,
            pal_btns, palette_state, modal, info_btn, info_modal, sorting=False):
    screen.blit(bg_surf, (0, 0))

    # outer window frame — fills interior gray, floats on teal desktop
    frame_rect = pygame.Rect(FRAME_X, FRAME_Y, WIN_W - 2 * FRAME_X, WIN_H - 2 * FRAME_Y)
    draw_raised(screen, frame_rect)

    # title bar gradient (inner top of frame)
    screen.blit(title_grad, (_IX, _IY))
    title = font.render("Sorting Algorithm Visualizer", False, WIN_WHITE)
    screen.blit(title, title.get_rect(midleft=(_IX + 8, _IY + TITLE_H // 2)))
    btn_y_cap = _IY + 4
    cap_right = WIN_W - FRAME_X - 2 - 4
    for i, lbl in enumerate(["-", "O", "X"]):
        br = pygame.Rect(cap_right - 62 + i * 22, btn_y_cap, 20, 16)
        draw_raised(screen, br)
        bt = comp_font.render(lbl, False, WIN_TEXT)
        screen.blit(bt, bt.get_rect(center=br.center))

    # control panel (below title bar, inside window frame — sunken like the canvas)
    panel_rect = pygame.Rect(_IX + 4, PANEL_Y, WIN_W - 2 * (_IX + 4), PANEL_H)
    draw_sunken(screen, panel_rect)

    # "Algorithm:" label
    alg_lbl = comp_font.render("Algorithm:", False, WIN_DARK if sorting else WIN_TEXT)
    screen.blit(alg_lbl, (COL_B, PANEL_Y + ALG_LABEL_ROW))

    # sound label
    mute_color = WIN_NAVY if sorter.sound_enabled else WIN_RED
    sound_txt = comp_font.render(
        "[M] Sound: ON" if sorter.sound_enabled else "[M] Sound: OFF", False, mute_color)
    screen.blit(sound_txt, (COL_C, PANEL_Y + ROW1 + 2))

    # comparisons
    comp_txt = comp_font.render(f"Comparisons: {sorter.comps}", False, WIN_TEXT)
    screen.blit(comp_txt, (COL_D, PANEL_Y + ROW1 + 2))

    # palette selector — label sits above the inset, inset wraps buttons + swatches
    _HPAD, _VTOP, _VBOT = 6, 6, 8
    _inset_w = 3 * PAL_BTN_W + 2 * PAL_BTN_GAP + _HPAD * 2
    pal_inset = pygame.Rect(
        COL_D - _HPAD,
        PANEL_Y + PAL_BTN_ROW - _VTOP,
        _inset_w,
        PAL_SWATCH_ROW - PAL_BTN_ROW + SWATCH_H + _VTOP + _VBOT,
    )
    draw_sunken(screen, pal_inset)
    pal_lbl = comp_font.render("Palette:", False, WIN_TEXT)
    screen.blit(pal_lbl, (COL_D, PANEL_Y + PAL_LABEL_ROW))

    # palette buttons
    for pb in pal_btns:
        selected = pb["key"] == palette_state["current"]
        if selected:
            draw_sunken(screen, pb["rect"])
        else:
            draw_raised(screen, pb["rect"], WIN_GRAY)
        t = comp_font.render(pb["label"], False, WIN_TEXT)
        screen.blit(t, t.get_rect(center=pb["rect"].center))

    # palette swatches
    for i, c in enumerate(palette_state["colors"]):
        sx = COL_D + i * (SWATCH_W + 1)
        sy = PANEL_Y + PAL_SWATCH_ROW
        pygame.draw.rect(screen, c, (sx, sy, SWATCH_W, SWATCH_H))
        pygame.draw.rect(screen, WIN_DARKER, (sx, sy, SWATCH_W, SWATCH_H), 1)

    blocked = sorting or modal.is_open
    for btn in buttons:
        btn.draw(screen, disabled=((btn.action == "stop") != sorting) or modal.is_open)
    desc_cb.draw(screen, disabled=blocked)
    size_slider.draw(screen, disabled=blocked)
    vol_slider.draw(screen)

    # sort canvas drawn before dropdown so open list renders on top of it
    border = pygame.Rect(SORT_X - 4, SORT_Y - 4, SORT_W + 8, SORT_H + 8)
    draw_sunken(screen, border)
    screen.blit(sort_surf, (SORT_X, SORT_Y))
    dropdown.draw(screen, disabled=blocked)
    info_btn.draw(screen, disabled=modal.is_open)

    if modal.is_open:
        modal.draw(screen, font)

    if info_modal.is_open:
        info_modal.draw(screen, font)


# ── main ──────────────────────────────────────────────────────────────────────
async def main():
    pygame.init()

    _mixer_ok = False
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
        _mixer_ok = True
    except Exception:
        pass

    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("vis-sort")

    # ── colour palettes ────────────────────────────────────────────────────────
    palette_state = {"current": "default", "colors": PALETTES["default"]}

    sort_surf = pygame.Surface((SORT_W, SORT_H))

    title_font = _font(12, bold=True)
    btn_font   = _font(11)
    comp_font  = _font(11)

    sorter = Sorter(sort_surf, SORT_W, SORT_H)
    sorter._mixer_ok = _mixer_ok

    modal = ColorPickerModal(btn_font, comp_font)
    info_modal = InfoModal(btn_font, comp_font)

    # pre-render background and title bar gradient
    bg_surf    = _make_bg_surf(_make_bg_tile())
    title_w    = WIN_W - 2 * _IX
    title_grad = pygame.Surface((title_w, TITLE_H))
    for i in range(title_w):
        t = i / (title_w - 1)
        c = (int(WIN_NAVY[0] + t * (WIN_NAVY2[0] - WIN_NAVY[0])),
             int(WIN_NAVY[1] + t * (WIN_NAVY2[1] - WIN_NAVY[1])),
             int(WIN_NAVY[2] + t * (WIN_NAVY2[2] - WIN_NAVY[2])))
        pygame.draw.line(title_grad, c, (i, 0), (i, TITLE_H - 1))

    # ── layout ────────────────────────────────────────────────────────────────
    # Col A — stacked buttons
    buttons = [
        Button((COL_A, PANEL_Y + ROW1, BTN_W, BTN_H), "Start",     "sort", btn_font),
        Button((COL_A, PANEL_Y + ROW2, BTN_W, BTN_H), "Stop",      "stop", btn_font, danger=True),
        Button((COL_A, PANEL_Y + ROW3, BTN_W, BTN_H), "New Array", "new",  btn_font),
    ]

    desc_cb = Checkbox(COL_B, PANEL_Y + ROW1 + (BTN_H - 16) // 2, "Descending", btn_font)

    dropdown = Dropdown((COL_B, PANEL_Y + ROW2, DROPDOWN_W, BTN_H), SORT_OPTIONS, btn_font)
    info_btn = Button((COL_B + DROPDOWN_W + 4, PANEL_Y + ROW2, BTN_H, BTN_H), "?", "info", btn_font)

    size_slider = Slider(
        track_rect=(COL_B, PANEL_Y + TRACK_ROW, ARRAY_SLIDER_W, 14),
        font=comp_font,
        min_val=SLIDER_MIN, max_val=SLIDER_MAX, step=SLIDER_STEP,
        initial=100, label="Array size",
    )

    vol_slider = Slider(
        track_rect=(COL_C, PANEL_Y + TRACK_ROW, VOL_SLIDER_W, 14),
        font=comp_font,
        min_val=0, max_val=100, step=5,
        initial=30, label="Volume",
    )
    sorter.volume = vol_slider.value / 100

    saved_slots = _load_palettes()

    pal_btns = [
        {"label": "Default",   "key": "default",
         "rect": pygame.Rect(COL_D,                                PANEL_Y + PAL_BTN_ROW, PAL_BTN_W, PAL_BTN_H)},
        {"label": "Phosphor",  "key": "phosphor",
         "rect": pygame.Rect(COL_D + PAL_BTN_W + PAL_BTN_GAP,     PANEL_Y + PAL_BTN_ROW, PAL_BTN_W, PAL_BTN_H)},
        {"label": "Custom...", "key": "custom",
         "rect": pygame.Rect(COL_D + 2 * (PAL_BTN_W + PAL_BTN_GAP), PANEL_Y + PAL_BTN_ROW, PAL_BTN_W, PAL_BTN_H)},
    ]

    sorter.makeNewVals(size_slider.value)
    task_ref = [None]
    _pre_modal_colors = list(sorter.colors)
    _pre_modal_key    = palette_state["current"]

    clock = pygame.time.Clock()

    while True:
        sorting = task_ref[0] is not None and not task_ref[0].done()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    sorter.sound_enabled = not sorter.sound_enabled

            # info modal intercepts all events while open
            if info_modal.is_open:
                _im_result = info_modal.handle_event(event)
                if _im_result == "close":
                    info_modal.close()
                elif _im_result in ("prev", "next"):
                    _cur_idx = ALGO_ORDER.index(info_modal._algo_key)
                    _delta   = -1 if _im_result == "prev" else 1
                    _new_key = ALGO_ORDER[(_cur_idx + _delta) % len(ALGO_ORDER)]
                    dropdown.selected = next(
                        i for i, (_, k) in enumerate(SORT_OPTIONS) if k == _new_key
                    )
                    await cancel_task(task_ref)
                    sorter.makeNewVals(size_slider.value)
                    info_modal.open(_new_key)
                continue

            # palette modal intercepts all events while open
            if modal.is_open:
                result = modal.handle_event(event)
                if result == "ok":
                    for i, tab in enumerate(modal.tab_colors):
                        if tab is not None:
                            saved_slots[i] = tab
                    active_colors = modal.tab_colors[modal.active_tab]
                    if active_colors:
                        palette_state["current"] = "custom"
                        palette_state["colors"]  = active_colors
                        sorter.colors            = active_colors
                    _save_palettes(saved_slots)
                    modal.close()
                    sorter.drawNums()
                elif result == "cancel":
                    sorter.colors            = _pre_modal_colors
                    palette_state["current"] = _pre_modal_key
                    palette_state["colors"]  = _pre_modal_colors
                    modal.close()
                    sorter.drawNums()
                continue

            # dropdown first — its continue prevents sliders/buttons seeing the same click
            prev_alg = dropdown.selected
            if dropdown.handle_event(event, disabled=sorting):
                if not dropdown.open and dropdown.selected != prev_alg:
                    await cancel_task(task_ref)
                    sorter.makeNewVals(size_slider.value)
                continue

            size_was_dragging = size_slider.dragging
            size_slider.handle_event(event, disabled=sorting)
            if size_was_dragging and not sorting and event.type == pygame.MOUSEBUTTONUP:
                await cancel_task(task_ref)
                sorter.makeNewVals(size_slider.value)

            vol_changed = vol_slider.handle_event(event)
            if vol_changed:
                sorter.volume = vol_slider.value / 100

            if desc_cb.handle_event(event, disabled=sorting):
                sorter.descending = desc_cb.checked

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for pb in pal_btns:
                    if not pb["rect"].collidepoint(event.pos):
                        continue
                    if pb["key"] == "custom":
                        _pre_modal_colors = list(sorter.colors)
                        _pre_modal_key    = palette_state["current"]
                        modal.open(saved_slots)
                    elif pb["key"] != palette_state["current"]:
                        palette_state["current"] = pb["key"]
                        palette_state["colors"]  = PALETTES[pb["key"]]
                        sorter.colors            = palette_state["colors"]
                        sorter.drawNums()
                    break

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if info_btn.is_clicked(event.pos, disabled=modal.is_open):
                    info_modal.open(dropdown.selected_action)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in buttons:
                    if btn.is_clicked(event.pos, disabled=((btn.action == "stop") != sorting)):
                        action = btn.action
                        if action == "stop":
                            await cancel_task(task_ref)
                        elif action == "new":
                            await cancel_task(task_ref)
                            sorter.makeNewVals(size_slider.value)
                        elif action == "sort":
                            await run_sort(sorter, dropdown.selected_action, task_ref)
                        break

        # cursor: show "no" when hovering over a disabled widget
        mp = pygame.mouse.get_pos()
        disabled_rects = [b.rect for b in buttons if (b.action == "stop") != sorting]
        if sorting:
            disabled_rects += [
                desc_cb._hit_rect(), dropdown.rect,
                size_slider.track, size_slider.thumb_rect(),
            ]
        if any(r.collidepoint(mp) for r in disabled_rects):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if modal.is_open:
            sorter.colors = modal.preview_colors()
            sorter.drawNums()

        draw_ui(screen, sorter, sort_surf, buttons, desc_cb, dropdown, size_slider, vol_slider,
                title_font, comp_font, title_grad, bg_surf,
                pal_btns, palette_state, modal, info_btn, info_modal, sorting=sorting)
        pygame.display.flip()
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
