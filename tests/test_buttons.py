import pygame
import pytest
from widgets import Button


@pytest.fixture
def font():
    return pygame.font.Font(None, 20)


def test_start_button_attrs(font):
    btn = Button((0, 0, 80, 28), "Start", "sort", font)
    assert btn.action == "sort"
    assert btn.danger is False


def test_stop_button_attrs(font):
    btn = Button((0, 0, 80, 28), "Stop", "stop", font, danger=True)
    assert btn.action == "stop"
    assert btn.danger is True


def test_new_button_attrs(font):
    btn = Button((0, 0, 80, 28), "New Array", "new", font)
    assert btn.action == "new"
    assert btn.danger is False


def test_is_clicked_enabled(font):
    btn = Button((0, 0, 80, 28), "Start", "sort", font)
    assert btn.is_clicked((40, 14)) is True


def test_is_clicked_disabled(font):
    btn = Button((0, 0, 80, 28), "Start", "sort", font)
    assert btn.is_clicked((40, 14), disabled=True) is False


def test_is_clicked_outside(font):
    btn = Button((0, 0, 80, 28), "Start", "sort", font)
    assert btn.is_clicked((200, 200)) is False


# Disable logic: (btn.action == "stop") != sorting
# stop button: disabled when not sorting, enabled when sorting
def test_stop_disabled_when_not_sorting(font):
    btn = Button((0, 0, 80, 28), "Stop", "stop", font, danger=True)
    sorting = False
    assert ((btn.action == "stop") != sorting) is True


def test_stop_enabled_when_sorting(font):
    btn = Button((0, 0, 80, 28), "Stop", "stop", font, danger=True)
    sorting = True
    assert ((btn.action == "stop") != sorting) is False


# start/new buttons: disabled when sorting, enabled when not sorting
def test_start_disabled_when_sorting(font):
    btn = Button((0, 0, 80, 28), "Start", "sort", font)
    sorting = True
    assert ((btn.action == "stop") != sorting) is True


def test_start_enabled_when_not_sorting(font):
    btn = Button((0, 0, 80, 28), "Start", "sort", font)
    sorting = False
    assert ((btn.action == "stop") != sorting) is False


# Info button
def test_info_button_attrs(font):
    btn = Button((0, 0, 28, 28), "?", "info", font)
    assert btn.action == "info"
    assert btn.danger is False


def test_info_button_label(font):
    btn = Button((0, 0, 28, 28), "?", "info", font)
    assert btn.label == "?"


def test_info_button_enabled_when_palette_modal_closed(font):
    btn = Button((0, 0, 28, 28), "?", "info", font)
    palette_modal_open = False
    assert btn.is_clicked((14, 14), disabled=palette_modal_open) is True


def test_info_button_disabled_when_palette_modal_open(font):
    btn = Button((0, 0, 28, 28), "?", "info", font)
    palette_modal_open = True
    assert btn.is_clicked((14, 14), disabled=palette_modal_open) is False
