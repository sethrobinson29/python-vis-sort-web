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
    def __init__(self, track_rect, font, min_val=100, max_val=500, step=5, initial=100):
        self.track  = pygame.Rect(track_rect)
        self.font   = font
        self.min    = min_val
        self.max    = max_val
        self.step   = step
        self.value  = initial
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
        lbl = self.font.render(f"Array size: {self.value}", True, PURPLE)
        surf.blit(lbl, (self.track.x, self.track.y - 22))

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


def draw_ui(screen, sorter, sort_surf, buttons, slider, font, comp_font):
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

    # comparisons
    comp_txt = comp_font.render(f"Comparisons: {sorter.comps}", True, PURPLE)
    screen.blit(comp_txt, (40, panel_y + 14))

    # buttons
    for btn in buttons:
        btn.draw(screen)

    # slider
    slider.draw(screen)


# ── main ──────────────────────────────────────────────────────────────────────
async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("vis-sort")

    sort_surf = pygame.Surface((SORT_W, SORT_H))

    # fonts (built-in only — required for Pygbag / WASM)
    title_font = pygame.font.Font(None, 42)
    btn_font   = pygame.font.Font(None, 28)
    comp_font  = pygame.font.Font(None, 24)

    sorter = Sorter(sort_surf, SORT_W, SORT_H)

    # ── buttons ───────────────────────────────────────────────────────────────
    panel_y   = SORT_Y + SORT_H + 12
    btn_top   = panel_y + 44
    btn_h     = 34
    btn_gap   = 8
    btn_x     = 240
    sort_btns = ["Bubble", "Selection", "Merge", "Quick", "Radix"]
    buttons   = []
    for idx, name in enumerate(sort_btns):
        w   = 96
        x   = btn_x + idx * (w + btn_gap)
        btn = Button((x, btn_top, w, btn_h), name, name.lower(), btn_font)
        buttons.append(btn)

    util_y = btn_top + btn_h + 8
    buttons.append(Button((btn_x,                btn_top - 36, 150, 30), "New Array",   "new",     btn_font))
    buttons.append(Button((btn_x + 158,          btn_top - 36, 110, 30), "Reverse",     "reverse", btn_font))
    quit_btn = Button((WIN_W - 110, panel_y + 10, 80, 30), "Quit", "quit", btn_font, danger=True)
    buttons.append(quit_btn)

    slider = Slider(
        track_rect=(WIN_W - 340, panel_y + 50, 280, 16),
        font=comp_font,
        min_val=SLIDER_MIN, max_val=SLIDER_MAX, step=SLIDER_STEP,
        initial=100,
    )

    sorter.makeNewVals(slider.value)
    task_ref = [None]
    slider_released = False  # track when to regenerate on slider release

    clock = pygame.time.Clock()

    while True:
        slider_changed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # slider
            was_dragging = slider.dragging
            changed = slider.handle_event(event)
            if was_dragging and event.type == pygame.MOUSEBUTTONUP:
                # slider released — regenerate
                await cancel_task(task_ref)
                sorter.makeNewVals(slider.value)

            # button clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in buttons:
                    if btn.is_clicked(event.pos):
                        action = btn.action
                        if action == "quit":
                            return
                        elif action == "new":
                            await cancel_task(task_ref)
                            sorter.makeNewVals(slider.value)
                        elif action == "reverse":
                            await cancel_task(task_ref)
                            task_ref[0] = asyncio.create_task(sorter.reverse())
                        elif action == "bubble":
                            await cancel_task(task_ref)
                            task_ref[0] = asyncio.create_task(sorter.bubbleSort())
                        elif action == "selection":
                            await cancel_task(task_ref)
                            task_ref[0] = asyncio.create_task(sorter.selectionSort())
                        elif action == "merge":
                            await cancel_task(task_ref)
                            task_ref[0] = asyncio.create_task(sorter.mergeSortWrap())
                        elif action == "quick":
                            await cancel_task(task_ref)
                            task_ref[0] = asyncio.create_task(sorter.quickSortWrap())
                        elif action == "radix":
                            await cancel_task(task_ref)
                            task_ref[0] = asyncio.create_task(sorter.radixSort())
                        break

        draw_ui(screen, sorter, sort_surf, buttons, slider, title_font, comp_font)
        pygame.display.flip()
        await asyncio.sleep(0)


asyncio.run(main())
