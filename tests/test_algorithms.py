import pygame
import pytest
from sorter import Sorter


@pytest.fixture
def sorter():
    surf = pygame.Surface((100, 100))
    s = Sorter(surf, 100, 100)
    s._mixer_ok = False
    s.makeNewVals(50)
    return s


COMPARISON_ALGOS = [
    "bubbleSort",
    "selectionSort",
    "mergeSortWrap",
    "quickSortWrap",
    "insertionSort",
    "heapSort",
    "shellSort",
    "timSort",
    "cocktailSort",
    "combSort",
    "gnomeSort",
    "cycleSort",
]

ALL_ALGOS = COMPARISON_ALGOS + ["radixSort"]


@pytest.mark.parametrize("method_name", ALL_ALGOS)
async def test_sort_ascending(sorter, method_name):
    sorter.descending = False
    await getattr(sorter, method_name)()
    assert sorter.vals == list(range(50))


@pytest.mark.parametrize("method_name", ALL_ALGOS)
async def test_sort_descending(sorter, method_name):
    sorter.descending = True
    await getattr(sorter, method_name)()
    assert sorter.vals == list(range(49, -1, -1))


@pytest.mark.parametrize("method_name", COMPARISON_ALGOS)
async def test_comps_incremented(sorter, method_name):
    sorter.descending = False
    await getattr(sorter, method_name)()
    assert sorter.comps > 0
