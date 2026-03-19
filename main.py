# Pygame sorting visualizer — web-compatible via Pygbag
# By Seth Robinson https://github.com/sethrobinson29
import asyncio
import pygame
from sorter import Sorter

# ── palette (Windows 95/98) ───────────────────────────────────────────────────
WIN_GRAY    = (192, 192, 192)   # classic silver / window background
WIN_LIGHT   = (255, 255, 255)   # button highlight (top-left edges)
WIN_DARK    = (128, 128, 128)   # button shadow (inner bottom-right)
WIN_DARKER  = (64, 64, 64)      # dark shadow (outer bottom-right)
WIN_NAVY    = (0, 0, 128)       # title bar / active selection
WIN_NAVY2   = (16, 132, 208)    # title bar gradient end (Win98)
WIN_TEXT    = (0, 0, 0)         # normal black text
WIN_WHITE   = (255, 255, 255)   # title bar / light text
WIN_RED     = (128, 0, 0)       # danger text

# short aliases
BG    = WIN_GRAY
WHITE = WIN_WHITE
RED   = WIN_RED

# ── layout constants ──────────────────────────────────────────────────────────
WIN_W, WIN_H      = 1100, 750
SORT_W, SORT_H    = 1015, 500
SORT_X, SORT_Y    = 42, 80

SLIDER_MIN, SLIDER_MAX, SLIDER_STEP = 100, 500, 5

# ── bottom panel layout ───────────────────────────────────────────────────────
# panel_y = SORT_Y + SORT_H + 12 = 592  →  panel height = 750 - 592 - 10 = 148px
#
# Columns (absolute x):
#   col_a = 34    buttons: Start / Stop / New Array
#   col_b = 148   Descending cb / Dropdown / Array size slider
#   col_c = 418   Sound label / Volume slider
#   col_d = 622   Comparisons
#
# Rows (offset from panel_y):
#   +14   Start, Descending cb, Sound label, Comparisons
#   +48   Stop, Dropdown
#   +82   New Array, slider labels
#   +100  slider tracks

COL_A, COL_B, COL_C, COL_D = 34, 148, 418, 622
BTN_W, BTN_H = 100, 28
ROW1, ROW2, ROW3, TRACK_ROW = 14, 48, 82, 100
ARRAY_SLIDER_W = 250
VOL_SLIDER_W   = 180
DROPDOWN_W     = 170


# ── font helper ───────────────────────────────────────────────────────────────
def _font(px_size, bold=False):
    """Try MS Sans Serif (Win95 system font), fall back to Pygame built-in."""
    try:
        return pygame.font.SysFont("microsoftsansserif,mssansserif,arial", px_size, bold=bold)
    except Exception:
        return pygame.font.Font(None, px_size + 10)


# ── Win95 3D drawing helpers ──────────────────────────────────────────────────
def draw_raised(surf, rect, color=None):
    r = pygame.Rect(rect)
    surf.fill(WIN_GRAY if color is None else color, r)
    pygame.draw.line(surf, WIN_LIGHT,  r.topleft,                  (r.right - 1, r.top))
    pygame.draw.line(surf, WIN_LIGHT,  r.topleft,                  (r.left, r.bottom - 1))
    pygame.draw.line(surf, WIN_DARK,   (r.right - 2, r.top + 1),   (r.right - 2, r.bottom - 2))
    pygame.draw.line(surf, WIN_DARK,   (r.left + 1, r.bottom - 2), (r.right - 2, r.bottom - 2))
    pygame.draw.line(surf, WIN_DARKER, (r.right - 1, r.top),       (r.right - 1, r.bottom - 1))
    pygame.draw.line(surf, WIN_DARKER, (r.left, r.bottom - 1),     (r.right - 1, r.bottom - 1))


def draw_sunken(surf, rect, color=None):
    r = pygame.Rect(rect)
    surf.fill(WIN_GRAY if color is None else color, r)
    pygame.draw.line(surf, WIN_DARKER, r.topleft,                  (r.right - 1, r.top))
    pygame.draw.line(surf, WIN_DARKER, r.topleft,                  (r.left, r.bottom - 1))
    pygame.draw.line(surf, WIN_DARK,   (r.left + 1, r.top + 1),    (r.right - 2, r.top + 1))
    pygame.draw.line(surf, WIN_DARK,   (r.left + 1, r.top + 1),    (r.left + 1, r.bottom - 2))
    pygame.draw.line(surf, WIN_LIGHT,  (r.right - 1, r.top),       (r.right - 1, r.bottom - 1))
    pygame.draw.line(surf, WIN_LIGHT,  (r.left, r.bottom - 1),     (r.right - 1, r.bottom - 1))


# ── Button ────────────────────────────────────────────────────────────────────
class Button:
    def __init__(self, rect, label, action, font, danger=False):
        self.rect   = pygame.Rect(rect)
        self.label  = label
        self.action = action
        self.font   = font
        self.danger = danger

    def draw(self, surf):
        color = (210, 160, 160) if self.danger else WIN_GRAY
        draw_raised(surf, self.rect, color)
        txt = self.font.render(self.label, False, WIN_RED if self.danger else WIN_TEXT)
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# ── Slider ────────────────────────────────────────────────────────────────────
class Slider:
    def __init__(self, track_rect, font, min_val=100, max_val=500, step=5, initial=100, label="Value"):
        self.track    = pygame.Rect(track_rect)
        self.font     = font
        self.min      = min_val
        self.max      = max_val
        self.step     = step
        self.value    = initial
        self.label    = label
        self.dragging = False

    @property
    def _thumb_x(self):
        ratio = (self.value - self.min) / (self.max - self.min)
        return int(self.track.x + ratio * self.track.width)

    def thumb_rect(self):
        tx = self._thumb_x
        ty = self.track.centery
        return pygame.Rect(tx - 8, ty - 10, 16, 20)

    def draw(self, surf):
        draw_sunken(surf, self.track, WIN_WHITE)       # white track background
        draw_raised(surf, self.thumb_rect())
        lbl = self.font.render(f"{self.label}: {self.value}", False, WIN_TEXT)
        surf.blit(lbl, (self.track.x, self.track.y - 18))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.thumb_rect().collidepoint(event.pos) or self.track.collidepoint(event.pos):
                self.dragging = True
                self._update_value(event.pos[0])
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False
                return True
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_value(event.pos[0])
            return True
        return False

    def _update_value(self, mouse_x):
        clamped = max(self.track.x, min(mouse_x, self.track.x + self.track.width))
        ratio   = (clamped - self.track.x) / self.track.width
        raw     = self.min + ratio * (self.max - self.min)
        self.value = int(round(raw / self.step) * self.step)
        self.value = max(self.min, min(self.max, self.value))


# ── Checkbox ─────────────────────────────────────────────────────────────────
class Checkbox:
    def __init__(self, x, y, label, font, checked=False):
        self.box     = pygame.Rect(x, y, 16, 16)
        self.label   = label
        self.font    = font
        self.checked = checked

    def _hit_rect(self):
        lw = self.font.size(self.label)[0]
        return pygame.Rect(self.box.x, self.box.y, self.box.width + 6 + lw, self.box.height)

    def draw(self, surf):
        draw_sunken(surf, self.box, WIN_WHITE)
        if self.checked:
            pygame.draw.line(surf, WIN_TEXT,
                (self.box.x + 2, self.box.centery),
                (self.box.centerx - 1, self.box.bottom - 3), 2)
            pygame.draw.line(surf, WIN_TEXT,
                (self.box.centerx - 1, self.box.bottom - 3),
                (self.box.right - 2, self.box.y + 2), 2)
        txt = self.font.render(self.label, False, WIN_TEXT)
        surf.blit(txt, (self.box.right + 6, self.box.centery - txt.get_height() // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._hit_rect().collidepoint(event.pos):
                self.checked = not self.checked
                return True
        return False


# ── Dropdown ──────────────────────────────────────────────────────────────────
class Dropdown:
    def __init__(self, rect, options, font):
        self.rect     = pygame.Rect(rect)
        self.options  = options
        self.font     = font
        self.selected = 0
        self.open     = False

    @property
    def selected_action(self):
        return self.options[self.selected][1]

    def _item_rect(self, i):
        n = len(self.options)
        return pygame.Rect(
            self.rect.x,
            self.rect.y - (n - i) * self.rect.height,
            self.rect.width,
            self.rect.height,
        )

    def draw(self, surf):
        # Win95 ComboBox: sunken white text field + raised arrow button
        arrow_w  = 18
        text_rect  = pygame.Rect(self.rect.x, self.rect.y, self.rect.width - arrow_w, self.rect.height)
        arrow_rect = pygame.Rect(self.rect.right - arrow_w, self.rect.y, arrow_w, self.rect.height)
        draw_sunken(surf, text_rect, WIN_WHITE)
        draw_raised(surf, arrow_rect)
        av = self.font.render("v", False, WIN_TEXT)
        surf.blit(av, av.get_rect(center=arrow_rect.center))
        label = self.options[self.selected][0]
        txt = self.font.render(label, False, WIN_TEXT)
        surf.blit(txt, txt.get_rect(midleft=(text_rect.x + 4, text_rect.centery)))

        if self.open:
            list_rect = pygame.Rect(
                self.rect.x,
                self.rect.y - len(self.options) * self.rect.height,
                self.rect.width,
                len(self.options) * self.rect.height,
            )
            pygame.draw.rect(surf, WIN_WHITE, list_rect)
            pygame.draw.rect(surf, WIN_DARKER, list_rect, 1)
            for i, (lbl, _) in enumerate(self.options):
                ir = self._item_rect(i)
                if i == self.selected:
                    pygame.draw.rect(surf, WIN_NAVY, ir)
                    t = self.font.render(lbl, False, WIN_WHITE)
                else:
                    t = self.font.render(lbl, False, WIN_TEXT)
                surf.blit(t, t.get_rect(midleft=(ir.x + 6, ir.centery)))

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return False
        if self.rect.collidepoint(event.pos):
            self.open = not self.open
            return True
        if self.open:
            for i in range(len(self.options)):
                if self._item_rect(i).collidepoint(event.pos):
                    self.selected = i
                    self.open = False
                    return True
            self.open = False
            return True
        return False


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
    dispatch = {
        "bubble":    sorter.bubbleSort,
        "selection": sorter.selectionSort,
        "merge":     sorter.mergeSortWrap,
        "quick":     sorter.quickSortWrap,
        "radix":     sorter.radixSort,
    }
    if action in dispatch:
        task_ref[0] = asyncio.create_task(dispatch[action]())


def draw_ui(screen, sorter, sort_surf, buttons, desc_cb, dropdown,
            size_slider, vol_slider, font, comp_font, title_grad):
    screen.fill(WIN_GRAY)

    # title bar
    screen.blit(title_grad, (0, 0))
    title = font.render("Sorting Algorithm Visualizer", False, WIN_WHITE)
    screen.blit(title, title.get_rect(midleft=(12, 34)))
    for i, lbl in enumerate(["-", "O", "X"]):
        br = pygame.Rect(WIN_W - 74 + i * 23, 8, 20, 16)
        draw_raised(screen, br)
        bt = comp_font.render(lbl, False, WIN_TEXT)
        screen.blit(bt, bt.get_rect(center=br.center))

    # sort canvas
    border = pygame.Rect(SORT_X - 4, SORT_Y - 4, SORT_W + 8, SORT_H + 8)
    draw_sunken(screen, border)
    screen.blit(sort_surf, (SORT_X, SORT_Y))

    # bottom panel
    panel_y    = SORT_Y + SORT_H + 12
    panel_rect = pygame.Rect(20, panel_y, WIN_W - 40, WIN_H - panel_y - 10)
    draw_raised(screen, panel_rect)

    # col D — comparisons (top-right of panel)
    comp_txt = comp_font.render(f"Comparisons: {sorter.comps}", False, WIN_TEXT)
    screen.blit(comp_txt, (COL_D, panel_y + ROW1 + 2))

    # col C — sound label + mute state
    mute_color = WIN_NAVY if sorter.sound_enabled else WIN_RED
    sound_txt = comp_font.render(
        "[M] Sound: ON" if sorter.sound_enabled else "[M] Sound: OFF", False, mute_color)
    screen.blit(sound_txt, (COL_C, panel_y + ROW1 + 2))

    # buttons, checkbox, slider, dropdown
    for btn in buttons:
        btn.draw(screen)
    desc_cb.draw(screen)
    size_slider.draw(screen)
    vol_slider.draw(screen)
    dropdown.draw(screen)   # last — renders on top when open


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

    sort_surf = pygame.Surface((SORT_W, SORT_H))

    title_font = _font(13, bold=True)
    btn_font   = _font(11)
    comp_font  = _font(11)

    sorter = Sorter(sort_surf, SORT_W, SORT_H)
    sorter._mixer_ok = _mixer_ok

    # pre-render title-bar gradient
    title_grad = pygame.Surface((WIN_W, 68))
    for i in range(WIN_W):
        t = i / (WIN_W - 1)
        c = (int(WIN_NAVY[0] + t * (WIN_NAVY2[0] - WIN_NAVY[0])),
             int(WIN_NAVY[1] + t * (WIN_NAVY2[1] - WIN_NAVY[1])),
             int(WIN_NAVY[2] + t * (WIN_NAVY2[2] - WIN_NAVY[2])))
        pygame.draw.line(title_grad, c, (i, 0), (i, 67))

    # ── layout ────────────────────────────────────────────────────────────────
    panel_y = SORT_Y + SORT_H + 12   # 592

    # Col A — stacked buttons (Start / Stop / New Array)
    buttons = [
        Button((COL_A, panel_y + ROW1,  BTN_W, BTN_H), "Start",     "sort", btn_font),
        Button((COL_A, panel_y + ROW2,  BTN_W, BTN_H), "Stop",      "stop", btn_font, danger=True),
        Button((COL_A, panel_y + ROW3,  BTN_W, BTN_H), "New Array", "new",  btn_font),
    ]

    # Col B row 1 — Descending checkbox (vertically centered with Start button)
    desc_cb = Checkbox(COL_B, panel_y + ROW1 + (BTN_H - 16) // 2, "Descending", btn_font)

    # Col B row 2 — algorithm dropdown
    sort_options = [
        ("Bubble",    "bubble"),
        ("Selection", "selection"),
        ("Merge",     "merge"),
        ("Quick",     "quick"),
        ("Radix",     "radix"),
    ]
    dropdown = Dropdown((COL_B, panel_y + ROW2, DROPDOWN_W, BTN_H), sort_options, btn_font)

    # Col B row 3 — array size slider  (label auto-placed 18px above track)
    size_slider = Slider(
        track_rect=(COL_B, panel_y + TRACK_ROW, ARRAY_SLIDER_W, 14),
        font=comp_font,
        min_val=SLIDER_MIN, max_val=SLIDER_MAX, step=SLIDER_STEP,
        initial=100, label="Array size",
    )

    # Col C row 3 — volume slider  (sound label drawn in draw_ui at row 1)
    vol_slider = Slider(
        track_rect=(COL_C, panel_y + TRACK_ROW, VOL_SLIDER_W, 14),
        font=comp_font,
        min_val=0, max_val=100, step=5,
        initial=50, label="Volume",
    )
    sorter.volume = vol_slider.value / 100

    sorter.makeNewVals(size_slider.value)
    task_ref = [None]

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    sorter.sound_enabled = not sorter.sound_enabled

            size_was_dragging = size_slider.dragging
            size_slider.handle_event(event)
            if size_was_dragging and event.type == pygame.MOUSEBUTTONUP:
                await cancel_task(task_ref)
                sorter.makeNewVals(size_slider.value)

            vol_changed = vol_slider.handle_event(event)
            if vol_changed:
                sorter.volume = vol_slider.value / 100

            if desc_cb.handle_event(event):
                sorter.descending = desc_cb.checked

            if dropdown.handle_event(event):
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in buttons:
                    if btn.is_clicked(event.pos):
                        action = btn.action
                        if action == "stop":
                            await cancel_task(task_ref)
                        elif action == "new":
                            await cancel_task(task_ref)
                            sorter.makeNewVals(size_slider.value)
                        elif action == "sort":
                            await run_sort(sorter, dropdown.selected_action, task_ref)
                        break

        draw_ui(screen, sorter, sort_surf, buttons, desc_cb, dropdown, size_slider, vol_slider,
                title_font, comp_font, title_grad)
        pygame.display.flip()
        await asyncio.sleep(0)


asyncio.run(main())
