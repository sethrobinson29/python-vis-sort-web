import pygame
import pytest
from main import SORT_OPTIONS, DISPATCH_MAP
from widgets import Dropdown


@pytest.fixture
def font():
    return pygame.font.Font(None, 20)


ALL_ALGORITHMS = {
    "bubble", "cocktail", "comb", "cycle", "gnome",
    "heap", "insertion", "merge", "quick", "radix",
    "selection", "shell", "tim",
}


def test_sort_options_has_all_labels():
    labels = [lbl for lbl, _ in SORT_OPTIONS]
    for expected in (
        "Bubble", "Cocktail", "Comb", "Cycle", "Gnome",
        "Heap", "Insertion", "Merge", "Quick", "Radix",
        "Selection", "Shell", "Tim",
    ):
        assert expected in labels


def test_sort_options_has_all_actions():
    actions = {act for _, act in SORT_OPTIONS}
    assert actions == ALL_ALGORITHMS


def test_sort_options_is_alphabetically_sorted():
    labels = [lbl for lbl, _ in SORT_OPTIONS]
    assert labels == sorted(labels)


def test_dispatch_map_covers_sort_options():
    actions = {act for _, act in SORT_OPTIONS}
    assert set(DISPATCH_MAP.keys()) == actions


def test_dropdown_default_selection(font):
    dd = Dropdown(pygame.Rect(0, 0, 100, 22), SORT_OPTIONS, font)
    assert dd.selected == 0


def test_dropdown_selected_action_default(font):
    dd = Dropdown(pygame.Rect(0, 0, 100, 22), SORT_OPTIONS, font)
    assert dd.selected_action == SORT_OPTIONS[0][1]


def test_dropdown_selected_action_after_change(font):
    dd = Dropdown(pygame.Rect(0, 0, 100, 22), SORT_OPTIONS, font)
    dd.selected = 2
    assert dd.selected_action == SORT_OPTIONS[2][1]
