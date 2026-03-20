import pygame
import pytest
from main import PALETTES, _validate_palette_data, ColorPickerModal
from theme import NUM_SLOTS


# ── PALETTES ──────────────────────────────────────────────────────────────────

def test_palettes_has_default_and_phosphor():
    assert "default" in PALETTES
    assert "phosphor" in PALETTES


def test_default_palette_length():
    assert len(PALETTES["default"]) == 10


def test_phosphor_palette_length():
    assert len(PALETTES["phosphor"]) == 10


def test_default_palette_first_color():
    assert PALETTES["default"][0] == pygame.Color("#FF4400")


def test_default_palette_last_color():
    assert PALETTES["default"][-1] == pygame.Color("#000080")


def test_phosphor_palette_green_dominant():
    for c in PALETTES["phosphor"]:
        assert c.g >= c.r
        assert c.g >= c.b


# ── color index formula ───────────────────────────────────────────────────────
# Matches sorter.py: ((val % 100) // 10 if val > 9 else 0) % len(colors)

def _color_idx(val, n_colors=10):
    return ((val % 100) // 10 if val > 9 else 0) % n_colors


def test_color_index_zero():
    assert _color_idx(0) == 0


def test_color_index_nine():
    assert _color_idx(9) == 0


def test_color_index_ten():
    assert _color_idx(10) == 1


def test_color_index_ninety_nine():
    assert _color_idx(99) == 9


def test_color_index_hundred():
    assert _color_idx(100) == 0


def test_color_index_short_palette():
    assert _color_idx(50, 3) == 2  # (50%100)//10 = 5, 5%3 = 2


# ── _validate_palette_data ────────────────────────────────────────────────────

def test_validate_valid_data():
    result = [None] * NUM_SLOTS
    needs_resave = _validate_palette_data([[[255, 0, 0], [0, 255, 0]]], result)
    assert needs_resave is False
    assert result[0] is not None
    assert len(result[0]) == 2


def test_validate_not_a_list():
    result = [None] * NUM_SLOTS
    needs_resave = _validate_palette_data("not a list", result)
    assert needs_resave is False  # returns early with False


def test_validate_invalid_slot_type():
    result = [None] * NUM_SLOTS
    needs_resave = _validate_palette_data(["bad_slot"], result)
    assert needs_resave is True
    assert result[0] is None


def test_validate_out_of_range_rgb():
    result = [None] * NUM_SLOTS
    needs_resave = _validate_palette_data([[[300, 0, 0]]], result)
    assert needs_resave is True
    assert result[0] is None


def test_validate_none_slot_skipped():
    result = [None] * NUM_SLOTS
    needs_resave = _validate_palette_data([None], result)
    assert needs_resave is False
    assert result[0] is None


# ── ColorPickerModal ──────────────────────────────────────────────────────────

@pytest.fixture
def modal():
    font = pygame.font.Font(None, 20)
    return ColorPickerModal(font, font)


def test_modal_closed_by_default(modal):
    assert modal.is_open is False


def test_modal_opens(modal):
    modal.open([None] * NUM_SLOTS)
    assert modal.is_open is True


def test_modal_has_5_tabs():
    assert NUM_SLOTS == 5


def test_modal_preview_colors_nonempty(modal):
    modal.open([None] * NUM_SLOTS)
    colors = modal.preview_colors()
    assert len(colors) > 0


def test_modal_cancel_closes(modal):
    modal.open([None] * NUM_SLOTS)
    modal.close()
    assert modal.is_open is False
