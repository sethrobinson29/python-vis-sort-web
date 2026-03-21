# Visual constants and stateless drawing utilities (Win95 style)
import pygame

# ── palette (Windows 95/98) ───────────────────────────────────────────────────
WIN_GRAY    = (192, 192, 192)
WIN_LIGHT   = (255, 255, 255)
WIN_DARK    = (128, 128, 128)
WIN_DARKER  = (64, 64, 64)
WIN_NAVY    = (0, 0, 128)
WIN_NAVY2   = (16, 132, 208)
WIN_TEXT    = (0, 0, 0)
WIN_WHITE   = (255, 255, 255)
WIN_RED     = (128, 0, 0)

BG    = WIN_GRAY
WHITE = WIN_WHITE
RED   = WIN_RED

# ── layout constants ──────────────────────────────────────────────────────────
WIN_W, WIN_H   = 1100, 820
SORT_W, SORT_H = 1015, 550

FRAME_X = 28   # desktop gap — outer window frame margin (≈1.75 crosshatch tiles)
FRAME_Y = 20
_IX = FRAME_X + 2   # inner content left edge (= 16)
_IY = FRAME_Y + 2   # inner content top edge  (= 16)

TITLE_H = 22            # title bar height
PANEL_H = 148           # control panel height (fixed — content-driven)
PANEL_Y = _IY + TITLE_H + 4   # control panel top  (= 64)
SORT_X   = 42
SORT_Y   = PANEL_Y + PANEL_H + 8  # canvas top — reduced gap to make room for taskbar
STATUS_H = 20                      # status bar height
TASKBAR_H = 28                     # Win95 taskbar at screen bottom

SLIDER_MIN, SLIDER_MAX, SLIDER_STEP = 100, 500, 5

# ── control panel column / row layout ────────────────────────────────────────
# Window frame at (FRAME_X, FRAME_Y) floats on teal desktop.
# Panel: y=64, height=148  →  canvas: y=220, height=550  →  bottom gap ~22px
#
# Columns (absolute x):
#   COL_A = 34    buttons: Start / Stop / New Array
#   COL_B = 176   Descending cb / "Algorithm:" + Dropdown / Array size slider
#   COL_C = 490   Sound label / Volume slider
#   COL_D = 740   Comparisons
#
# Rows (offset from PANEL_Y):
#   ROW1 = 12     Start, Descending cb, Sound label, Comparisons
#   ALG  = 44     "Algorithm:" label
#   ROW2 = 58     Stop, Dropdown
#   ROW3 = 100    New Array, slider labels
#   TRK  = 118    slider tracks

COL_A, BTN_W  = 44, 110
COL_B          = 176
COL_C          = 490
COL_D          = 740
BTN_H          = 28
DROPDOWN_W     = 180
ARRAY_SLIDER_W = 290
VOL_SLIDER_W   = 210
ROW1           = 12
ALG_LABEL_ROW  = 44
ROW2           = 58
ROW3           = 100
TRACK_ROW      = 118

# ── palette selector (COL_D column, pushed to bottom of panel) ────────────────
# Layout built bottom-up from PANEL_H=148:
#   8px below inset → 8px inset bottom pad → swatches(14) → 10px gap →
#   buttons(20) → 6px inset top pad → 4px gap → label
PAL_LABEL_ROW  = 64   # unused (groupbox label replaced it)
PAL_BTN_ROW    = 20   # buttons near top of groupbox (below label+border ~12px)
PAL_SWATCH_ROW = 50   # swatches: 10px below button bottom (20+20+10)
PAL_BTN_W      = 76
PAL_BTN_H      = 20
PAL_BTN_GAP    = 4
SWATCH_W       = 20
SWATCH_H       = 14

SAVE_FILE      = "palettes.json"
NUM_SLOTS      = 5


# ── font helper ───────────────────────────────────────────────────────────────
def _font(px_size, bold=False):
    try:
        return pygame.font.SysFont("microsoftsansserif,mssansserif,arial", px_size, bold=bold)
    except Exception:
        return pygame.font.Font(None, px_size + 10)


# ── background tile ───────────────────────────────────────────────────────────
def _make_bg_tile():
    C_LINE   = (0,  48, 56)
    C_FILL   = (0,  96, 112)
    C_ACCENT = (32, 80, 128)
    S = 16
    tile = pygame.Surface((S, S))
    for y in range(S):
        for x in range(S):
            on_d1  = (x + y) % S < 2
            on_d2  = (x - y) % S < 2
            at_ctr = ((x + y) % S == 8) and ((x - y) % S == 8)
            if on_d1 or on_d2:
                c = C_LINE
            elif at_ctr:
                c = C_ACCENT
            else:
                c = C_FILL
            tile.set_at((x, y), c)
    return tile


def _make_bg_surf(tile):
    surf = pygame.Surface((WIN_W, WIN_H))
    tw, th = tile.get_size()
    for ty in range(0, WIN_H, th):
        for tx in range(0, WIN_W, tw):
            surf.blit(tile, (tx, ty))
    return surf


# ── Win95 3D drawing helpers ──────────────────────────────────────────────────
def draw_groupbox(surf, rect, label, font):
    """Win95 GroupBox: etched border (gray outer + white inner) with label clipped into top."""
    r = pygame.Rect(rect)
    lbl = font.render(label, False, WIN_DARK)   # gray label — subtle on WIN_GRAY bg
    lbl_h = lbl.get_height()
    lbl_x = r.x + 8
    by = r.y + lbl_h // 2   # border top at midpoint of label height
    gl = lbl_x - 2           # gap left
    gr = lbl_x + lbl.get_width() + 2  # gap right

    # outer border — WIN_DARK (medium gray, not harsh black)
    if gl > r.x:
        pygame.draw.line(surf, WIN_DARK, (r.x, by),       (gl,          by))
    if gr < r.right:
        pygame.draw.line(surf, WIN_DARK, (gr, by),        (r.right - 1, by))
    pygame.draw.line(surf, WIN_DARK, (r.x,       by), (r.x,       r.bottom - 1))
    pygame.draw.line(surf, WIN_DARK, (r.right-1, by), (r.right-1, r.bottom - 1))
    pygame.draw.line(surf, WIN_DARK, (r.x, r.bottom-1),  (r.right-1, r.bottom-1))

    # inner border — WIN_LIGHT, 1 px inset (gives the etched-into-gray illusion)
    by1 = by + 1
    if gl > r.x + 1:
        pygame.draw.line(surf, WIN_LIGHT, (r.x+1, by1), (gl,          by1))
    if gr < r.right - 1:
        pygame.draw.line(surf, WIN_LIGHT, (gr,    by1), (r.right - 2, by1))
    pygame.draw.line(surf, WIN_LIGHT, (r.x+1,     by1), (r.x+1,     r.bottom-2))
    pygame.draw.line(surf, WIN_LIGHT, (r.right-2, by1), (r.right-2, r.bottom-2))
    pygame.draw.line(surf, WIN_LIGHT, (r.x+1, r.bottom-2), (r.right-2, r.bottom-2))

    surf.blit(lbl, (lbl_x, r.y))



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
