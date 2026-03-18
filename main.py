# Pygame sorting visualizer — web-compatible via Pygbag
# By Seth Robinson https://github.com/sethrobinson29
import asyncio
import pygame
from sorter import Sorter

# ── palette ──────────────────────────────────────────────────────────────────
BG          = (41, 115, 115)    # #297373
PANEL       = (0, 0, 52)        # #000034
HEADER      = (46, 41, 78)      # #2e294e
PURPLE      = (190, 151, 198)   # #be97c6
WHITE       = (255, 255, 255)
RED         = (220, 50, 50)

# ── layout constants ──────────────────────────────────────────────────────────
WIN_W, WIN_H      = 1100, 750
SORT_W, SORT_H    = 1015, 550
SORT_X, SORT_Y    = 42, 80       # where the sort surface is blitted

SLIDER_MIN, SLIDER_MAX, SLIDER_STEP = 100, 500, 5


# ── Button ────────────────────────────────────────────────────────────────────
class Button:
    def __init__(self, rect, label, action, font, danger=False):
        self.rect   = pygame.Rect(rect)
        self.label  = label
        self.action = action
        self.font   = font
        self.danger = danger

    def draw(self, surf):
        color = RED if self.danger else PURPLE
        pygame.draw.rect(surf, color, self.rect, border_radius=4)
        pygame.draw.rect(surf, HEADER, self.rect, width=2, border_radius=4)
        txt = self.font.render(self.label, True, PANEL if not self.danger else WHITE)
        r   = txt.get_rect(center=self.rect.center)
        surf.blit(txt, r)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# ── Slider ────────────────────────────────────────────────────────────────────
class Slider:
    def __init__(self, track_rect, font, min_val=100, max_val=500, step=5, initial=100, label="Value"):
        self.track  = pygame.Rect(track_rect)
        self.font   = font
        self.min    = min_val
        self.max    = max_val
        self.step   = step
        self.value  = initial
        self.label  = label
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
        # track
        pygame.draw.rect(surf, HEADER, self.track, border_radius=4)
        pygame.draw.rect(surf, PURPLE, self.track, width=2, border_radius=4)
        # thumb
        pygame.draw.rect(surf, PURPLE, self.thumb_rect(), border_radius=3)
        # label
        lbl = self.font.render(f"{self.label}: {self.value}", True, PURPLE)
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


# ── Dropdown ──────────────────────────────────────────────────────────────────
class Dropdown:
    def __init__(self, rect, options, font):
        self.rect    = pygame.Rect(rect)
        self.options = options  # list of (label, action)
        self.font    = font
        self.selected = 0
        self.open    = False

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
        pygame.draw.rect(surf, PURPLE, self.rect, border_radius=4)
        pygame.draw.rect(surf, HEADER, self.rect, width=2, border_radius=4)
        label = self.options[self.selected][0]
        txt = self.font.render(label + " [v]", True, PANEL)
        surf.blit(txt, txt.get_rect(center=self.rect.center))

        if self.open:
            for i, (lbl, _) in enumerate(self.options):
                ir = self._item_rect(i)
                bg = HEADER if i == self.selected else PANEL
                pygame.draw.rect(surf, bg, ir, border_radius=3)
                pygame.draw.rect(surf, PURPLE, ir, width=1, border_radius=3)
                t = self.font.render(lbl, True, PURPLE)
                surf.blit(t, t.get_rect(center=ir.center))

    def handle_event(self, event):
        """Returns True if the event was consumed."""
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
    """Cancel any running sort task."""
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


def draw_ui(screen, sorter, sort_surf, buttons, dropdown, size_slider, vol_slider, font, comp_font):
    screen.fill(BG)

    # header
    header_rect = pygame.Rect(0, 0, WIN_W, 68)
    pygame.draw.rect(screen, HEADER, header_rect)
    pygame.draw.rect(screen, PANEL, header_rect, width=4)
    title = font.render("Sorting Algorithm Visualizer", True, PURPLE)
    screen.blit(title, title.get_rect(center=(WIN_W // 2, 34)))

    # sort canvas border + surface
    border = pygame.Rect(SORT_X - 3, SORT_Y - 3, SORT_W + 6, SORT_H + 6)
    pygame.draw.rect(screen, HEADER, border, border_radius=3)
    screen.blit(sort_surf, (SORT_X, SORT_Y))

    # bottom panel
    panel_y = SORT_Y + SORT_H + 12
    panel_rect = pygame.Rect(20, panel_y, WIN_W - 40, WIN_H - panel_y - 10)
    pygame.draw.rect(screen, PANEL, panel_rect, border_radius=6)
    pygame.draw.rect(screen, HEADER, panel_rect, width=3, border_radius=6)

    # comparisons + sound status (right of sort button)
    comp_txt = comp_font.render(f"Comparisons: {sorter.comps}", True, PURPLE)
    screen.blit(comp_txt, (530, panel_y + 14))

    mute_color = PURPLE if sorter.sound_enabled else RED
    mute_txt = comp_font.render(
        "[M] Sound: ON" if sorter.sound_enabled else "[M] Sound: OFF", True, mute_color)
    screen.blit(mute_txt, (530, panel_y + 32))

    # regular buttons
    for btn in buttons:
        btn.draw(screen)

    # sliders
    size_slider.draw(screen)
    vol_slider.draw(screen)

    # dropdown drawn last so it renders on top of everything
    dropdown.draw(screen)


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

    # fonts (built-in only — required for Pygbag / WASM)
    title_font = pygame.font.Font(None, 42)
    btn_font   = pygame.font.Font(None, 28)
    comp_font  = pygame.font.Font(None, 24)

    sorter = Sorter(sort_surf, SORT_W, SORT_H)
    sorter._mixer_ok = _mixer_ok

    # ── layout ────────────────────────────────────────────────────────────────
    panel_y  = SORT_Y + SORT_H + 12   # = 642
    btn_y    = panel_y + 8             # = 650
    btn_h    = 30

    # ── buttons ───────────────────────────────────────────────────────────────
    buttons = [
        Button((40,  btn_y, 120, btn_h), "New Array", "new",     btn_font),
        Button((168, btn_y, 100, btn_h), "Reverse",   "reverse", btn_font),
        Button((444, btn_y,  80, btn_h), "Sort >",     "sort",  btn_font),
        Button((WIN_W - 110, btn_y, 80, btn_h), "Quit", "quit",  btn_font, danger=True),
    ]

    # ── dropdown ──────────────────────────────────────────────────────────────
    sort_options = [
        ("Bubble",    "bubble"),
        ("Selection", "selection"),
        ("Merge",     "merge"),
        ("Quick",     "quick"),
        ("Radix",     "radix"),
    ]
    dropdown = Dropdown((276, btn_y, 160, btn_h), sort_options, btn_font)

    # ── sliders ───────────────────────────────────────────────────────────────
    track_y = panel_y + 66

    size_slider = Slider(
        track_rect=(40, track_y, 280, 16),
        font=comp_font,
        min_val=SLIDER_MIN, max_val=SLIDER_MAX, step=SLIDER_STEP,
        initial=100, label="Array size",
    )
    vol_slider = Slider(
        track_rect=(340, track_y, 200, 16),
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

            # sliders
            size_was_dragging = size_slider.dragging
            size_slider.handle_event(event)
            if size_was_dragging and event.type == pygame.MOUSEBUTTONUP:
                await cancel_task(task_ref)
                sorter.makeNewVals(size_slider.value)

            vol_changed = vol_slider.handle_event(event)
            if vol_changed:
                sorter.volume = vol_slider.value / 100

            # dropdown (consume event before buttons if open)
            if dropdown.handle_event(event):
                continue

            # button clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in buttons:
                    if btn.is_clicked(event.pos):
                        action = btn.action
                        if action == "quit":
                            return
                        elif action == "new":
                            await cancel_task(task_ref)
                            sorter.makeNewVals(size_slider.value)
                        elif action == "reverse":
                            await cancel_task(task_ref)
                            task_ref[0] = asyncio.create_task(sorter.reverse())
                        elif action == "sort":
                            await run_sort(sorter, dropdown.selected_action, task_ref)
                        break

        draw_ui(screen, sorter, sort_surf, buttons, dropdown, size_slider, vol_slider,
                title_font, comp_font)
        pygame.display.flip()
        await asyncio.sleep(0)


asyncio.run(main())
