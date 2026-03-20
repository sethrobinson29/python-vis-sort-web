# Win95-style reusable widget classes
import pygame
from theme import (
    WIN_GRAY, WIN_LIGHT, WIN_DARK, WIN_DARKER,
    WIN_NAVY, WIN_TEXT, WIN_WHITE, WIN_RED, WIN_NAVY2,
    draw_raised, draw_sunken,
)


# ── Button ────────────────────────────────────────────────────────────────────
class Button:
    def __init__(self, rect, label, action, font, danger=False):
        self.rect   = pygame.Rect(rect)
        self.label  = label
        self.action = action
        self.font   = font
        self.danger = danger

    def draw(self, surf, disabled=False):
        if disabled:
            draw_raised(surf, self.rect, WIN_GRAY)
            r = self.font.render(self.label, False, WIN_LIGHT)
            pos = r.get_rect(center=self.rect.center)
            surf.blit(r, pos.move(1, 1))
            surf.blit(self.font.render(self.label, False, WIN_DARK), pos)
        else:
            color = (210, 160, 160) if self.danger else WIN_GRAY
            draw_raised(surf, self.rect, color)
            txt = self.font.render(self.label, False, WIN_RED if self.danger else WIN_TEXT)
            surf.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, pos, disabled=False):
        return not disabled and self.rect.collidepoint(pos)


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

    def draw(self, surf, disabled=False):
        draw_sunken(surf, self.track, WIN_WHITE)
        if not disabled:
            fill_w = self._thumb_x - self.track.x
            if fill_w > 2:
                surf.fill(WIN_NAVY, pygame.Rect(self.track.x + 2, self.track.y + 2,
                                                fill_w - 2, self.track.height - 4))
        draw_raised(surf, self.thumb_rect(), WIN_DARK if disabled else WIN_GRAY)
        lbl_text = f"{self.label}: {self.value}"
        lbl_color = WIN_DARK if disabled else WIN_TEXT
        lbl = self.font.render(lbl_text, False, lbl_color)
        surf.blit(lbl, (self.track.x, self.track.y - 18))

    def handle_event(self, event, disabled=False):
        if disabled:
            self.dragging = False
            return False
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

    def draw(self, surf, disabled=False):
        draw_sunken(surf, self.box, WIN_WHITE)
        tick_color = WIN_DARK if disabled else WIN_TEXT
        if self.checked:
            pygame.draw.line(surf, tick_color,
                (self.box.x + 2, self.box.centery),
                (self.box.centerx - 1, self.box.bottom - 3), 2)
            pygame.draw.line(surf, tick_color,
                (self.box.centerx - 1, self.box.bottom - 3),
                (self.box.right - 2, self.box.y + 2), 2)
        txt = self.font.render(self.label, False, WIN_DARK if disabled else WIN_TEXT)
        surf.blit(txt, (self.box.right + 6, self.box.centery - txt.get_height() // 2))

    def handle_event(self, event, disabled=False):
        if disabled:
            return False
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
        """List items drop downward from the bottom of the button."""
        return pygame.Rect(
            self.rect.x,
            self.rect.bottom + i * self.rect.height,
            self.rect.width,
            self.rect.height,
        )

    def draw(self, surf, disabled=False):
        arrow_w    = 18
        text_rect  = pygame.Rect(self.rect.x, self.rect.y, self.rect.width - arrow_w, self.rect.height)
        arrow_rect = pygame.Rect(self.rect.right - arrow_w, self.rect.y, arrow_w, self.rect.height)
        text_color = WIN_DARK if disabled else WIN_TEXT
        draw_sunken(surf, text_rect, WIN_WHITE)
        draw_raised(surf, arrow_rect)
        av = self.font.render("v", False, text_color)
        surf.blit(av, av.get_rect(center=arrow_rect.center))
        label = self.options[self.selected][0]
        txt = self.font.render(label, False, text_color)
        surf.blit(txt, txt.get_rect(midleft=(text_rect.x + 4, text_rect.centery)))

        if self.open and not disabled:
            list_rect = pygame.Rect(
                self.rect.x,
                self.rect.bottom,
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

    def handle_event(self, event, disabled=False):
        if disabled:
            self.open = False
            return False
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
