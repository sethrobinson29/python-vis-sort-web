import pygame
import pytest
from widgets import Button


@pytest.fixture
def font():
    return pygame.font.Font(None, 20)


def test_is_clicked_enabled(font):
    btn = Button((0, 0, 80, 28), "Start", "sort", font)
    assert btn.is_clicked((40, 14)) is True


def test_is_clicked_disabled(font):
    btn = Button((0, 0, 80, 28), "Start", "sort", font)
    assert btn.is_clicked((40, 14), disabled=True) is False


def test_is_clicked_outside(font):
    btn = Button((0, 0, 80, 28), "Start", "sort", font)
    assert btn.is_clicked((200, 200)) is False


def test_info_button_enabled_when_palette_modal_closed(font):
    btn = Button((0, 0, 28, 28), "?", "info", font)
    assert btn.is_clicked((14, 14), disabled=False) is True


def test_info_button_disabled_when_palette_modal_open(font):
    btn = Button((0, 0, 28, 28), "?", "info", font)
    assert btn.is_clicked((14, 14), disabled=True) is False
