import pygame
import pytest
from info_modal import InfoModal, ALGO_INFO, ALGO_ORDER


ALL_ALGO_KEYS = {
    "bubble", "cocktail", "comb", "cycle", "gnome",
    "heap", "insertion", "merge", "quick", "radix",
    "selection", "shell", "tim",
}

REQUIRED_FIELDS = ("name", "complexity", "creator", "usages", "summary", "diagram")


@pytest.fixture(scope="module")
def modal():
    font = pygame.font.Font(None, 20)
    return InfoModal(font, font)


# ── ALGO_INFO data ─────────────────────────────────────────────────────────────

def test_algo_info_has_all_13_algorithms():
    assert set(ALGO_INFO.keys()) == ALL_ALGO_KEYS


@pytest.mark.parametrize("key", sorted(ALL_ALGO_KEYS))
def test_algo_info_entry_has_required_fields(key):
    entry = ALGO_INFO[key]
    for field in REQUIRED_FIELDS:
        assert field in entry, f"{key!r} missing field {field!r}"


@pytest.mark.parametrize("key", sorted(ALL_ALGO_KEYS))
def test_algo_info_complexity_has_four_rows(key):
    rows = ALGO_INFO[key]["complexity"]
    assert len(rows) == 4


@pytest.mark.parametrize("key", sorted(ALL_ALGO_KEYS))
def test_algo_info_usages_is_nonempty(key):
    assert len(ALGO_INFO[key]["usages"]) >= 1


@pytest.mark.parametrize("key", sorted(ALL_ALGO_KEYS))
def test_algo_info_diagram_key_matches_algo_key(key):
    assert ALGO_INFO[key]["diagram"] == key


# ── ALGO_ORDER ─────────────────────────────────────────────────────────────────

def test_algo_order_contains_all_algorithms():
    assert set(ALGO_ORDER) == ALL_ALGO_KEYS


def test_algo_order_has_no_duplicates():
    assert len(ALGO_ORDER) == len(set(ALGO_ORDER))


def test_algo_order_is_alphabetically_sorted():
    assert ALGO_ORDER == sorted(ALGO_ORDER)


# ── InfoModal lifecycle ────────────────────────────────────────────────────────

def test_modal_starts_closed(modal):
    assert modal.is_open is False


def test_modal_open_sets_is_open(modal):
    modal.open("bubble")
    assert modal.is_open is True
    modal.close()


def test_modal_open_sets_algo_key(modal):
    modal.open("merge")
    assert modal._algo_key == "merge"
    modal.close()


def test_modal_open_builds_content_surf(modal):
    modal.open("quick")
    assert modal._content_surf is not None
    modal.close()


def test_modal_close_sets_is_open_false(modal):
    modal.open("bubble")
    modal.close()
    assert modal.is_open is False


@pytest.mark.parametrize("key", sorted(ALL_ALGO_KEYS))
def test_modal_open_accepts_all_algorithm_keys(key, modal):
    modal.open(key)
    assert modal._algo_key == key
    assert modal.is_open is True
    modal.close()


# ── InfoModal geometry ─────────────────────────────────────────────────────────

def test_modal_rect_is_centered_horizontally(modal):
    from theme import WIN_W
    assert modal.rect.centerx == WIN_W // 2


def test_modal_height_positive(modal):
    assert modal.H > 0


# ── InfoModal handle_event ─────────────────────────────────────────────────────

def _make_click(pos, button=1):
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": pos, "button": button})
    return event


def test_handle_event_x_button_returns_close(modal):
    modal.open("bubble")
    center = modal._x_btn.center
    assert modal.handle_event(_make_click(center)) == "close"
    modal.close()


def test_handle_event_close_button_returns_close(modal):
    modal.open("bubble")
    center = modal._close_btn.center
    assert modal.handle_event(_make_click(center)) == "close"
    modal.close()


def test_handle_event_prev_button_returns_prev(modal):
    modal.open("bubble")
    center = modal._prev_btn.center
    assert modal.handle_event(_make_click(center)) == "prev"
    modal.close()


def test_handle_event_next_button_returns_next(modal):
    modal.open("bubble")
    center = modal._next_btn.center
    assert modal.handle_event(_make_click(center)) == "next"
    modal.close()


def test_handle_event_outside_rect_returns_close(modal):
    modal.open("bubble")
    outside = (modal.rect.right + 50, modal.rect.bottom + 50)
    assert modal.handle_event(_make_click(outside)) == "close"
    modal.close()


def test_handle_event_right_click_returns_none(modal):
    modal.open("bubble")
    center = modal._close_btn.center
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": center, "button": 3})
    assert modal.handle_event(event) is None
    modal.close()


def test_handle_event_keydown_returns_none(modal):
    modal.open("bubble")
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE, "mod": 0, "unicode": ""})
    assert modal.handle_event(event) is None
    modal.close()


def test_handle_event_click_inside_content_area_returns_none(modal):
    modal.open("bubble")
    inside = modal._content_rect.center
    assert modal.handle_event(_make_click(inside)) is None
    modal.close()


# ── ALGO_INFO content completeness ────────────────────────────────────────────

@pytest.mark.parametrize("key", sorted(ALL_ALGO_KEYS))
def test_algo_info_name_is_nonempty_string(key):
    assert isinstance(ALGO_INFO[key]["name"], str)
    assert len(ALGO_INFO[key]["name"]) > 0


@pytest.mark.parametrize("key", sorted(ALL_ALGO_KEYS))
def test_algo_info_creator_is_nonempty_string(key):
    assert isinstance(ALGO_INFO[key]["creator"], str)
    assert len(ALGO_INFO[key]["creator"]) > 0


@pytest.mark.parametrize("key", sorted(ALL_ALGO_KEYS))
def test_algo_info_summary_is_nonempty_string(key):
    assert isinstance(ALGO_INFO[key]["summary"], str)
    assert len(ALGO_INFO[key]["summary"]) > 0


@pytest.mark.parametrize("key", sorted(ALL_ALGO_KEYS))
def test_algo_info_complexity_labels(key):
    labels = [row[0] for row in ALGO_INFO[key]["complexity"]]
    assert "Worst" in labels
    assert "Best" in labels
    assert "Average" in labels
    assert "Space" in labels


@pytest.mark.parametrize("key", sorted(ALL_ALGO_KEYS))
def test_algo_info_complexity_values_nonempty(key):
    for label, value in ALGO_INFO[key]["complexity"]:
        assert len(value) > 0, f"{key!r} complexity row {label!r} has empty value"
