# Class for animating sorting algorithms (Pygame version)
# By Seth Robinson https://github.com/sethrobinson29
import array
import asyncio
import math
import pygame
from random import shuffle


def _make_tone(freq, duration_ms=80, sample_rate=44100, volume=0.25):
    n = int(sample_rate * duration_ms / 1000)
    attack, decay = max(1, n // 10), max(1, n // 10)
    buf = array.array('h')
    for i in range(n):
        t = i / sample_rate
        env = i / attack if i < attack else (n - i) / decay if i > n - decay else 1.0
        buf.append(int(32767 * volume * env * math.sin(2 * math.pi * freq * t)))
    return pygame.mixer.Sound(buffer=buf)

# swap function
def swapVals(arr, i, j):
    tmp = arr[j]
    arr[j] = arr[i]
    arr[i] = tmp

# colors for drawing values — pre-converted from hex to RGB
_hex_colors = ["#FF4400", "#FFCC00", "#88CC00", "#00CC00", "#00FF80",
               "#00FFFF", "#00CFFF", "#0080FF", "#0000FF", "#000080"]
colors = [pygame.Color(c) for c in _hex_colors]


class Sorter:
    def __init__(self, surface, width=1015, height=550):
        self.surface = surface
        self.width = width
        self.height = height
        self.vals = []
        self.numBars = 0
        self.comps = 0
        self.highlighted = []
        self.sound_enabled = True
        self.volume = 0.5
        self.descending = False
        self._tone_cache = {}
        self._mixer_ok = False

    def makeNewVals(self, length):
        self.numBars = length
        self.vals = list(range(length))
        shuffle(self.vals)
        self.comps = 0
        self.highlighted = []
        self._tone_cache = {}
        self.drawNums()

    def _get_tone(self, value):
        freq = int(220 * (2 ** (value / self.numBars * 2)))
        if freq not in self._tone_cache:
            self._tone_cache[freq] = _make_tone(freq)
        return self._tone_cache[freq]

    def _play_highlight_tone(self):
        if not self._mixer_ok or not self.sound_enabled or not self.highlighted:
            return
        value = self.vals[self.highlighted[0]]
        if value > 0:
            tone = self._get_tone(value)
            tone.set_volume(self.volume)
            tone.play()

    def drawNums(self):
        self.surface.fill((0, 0, 0))
        bar_width = max(1, self.width // self.numBars) if self.numBars else 1
        x_step = (self.width - 10) / self.numBars if self.numBars else 1

        for i in range(self.numBars):
            color_idx = (self.vals[i] % 100) // 10 if self.vals[i] > 9 else 0
            color = colors[color_idx]
            bar_height = self.vals[i]
            pygame.draw.line(
                self.surface,
                color,
                (int(10 + i * x_step), self.height),
                (int(10 + i * x_step), self.height - bar_height),
                1,
            )

        for idx in self.highlighted:
            if 0 <= idx < self.numBars:
                hx = int(10 + idx * x_step)
                pygame.draw.line(self.surface, (255, 255, 255),
                                 (hx, self.height), (hx, self.height - self.vals[idx]), 1)
        self._play_highlight_tone()

    async def final_pass(self):
        """Sweep left-to-right through the sorted array, playing notes for each bar."""
        draw_every = max(1, self.numBars // 100)
        for step, i in enumerate(range(self.numBars)):
            self.highlighted = [i]
            if step % draw_every == 0:
                self.drawNums()
                await asyncio.sleep(0)
        self.highlighted = []
        self.drawNums()
        await asyncio.sleep(0)

    async def reverse(self):
        i, j = 0, self.numBars - 1
        draw_every = max(1, self.numBars // 100)
        step = 0
        while i < j:
            swapVals(self.vals, i, j)
            i += 1
            j -= 1
            step += 1
            if step % draw_every == 0:
                self.drawNums()
                await asyncio.sleep(0)
        self.highlighted = []
        self.drawNums()
        await asyncio.sleep(0)

    async def bubbleSort(self):
        self.comps = 0
        draw_every = max(1, self.numBars // 100)
        for i in range(self.numBars - 1):
            swapped = False
            for j in range(self.numBars - i - 1):
                self.comps += 1
                if (self.vals[j] > self.vals[j + 1]) if not self.descending else (self.vals[j] < self.vals[j + 1]):
                    swapVals(self.vals, j, j + 1)
                    swapped = True
                if self.comps % draw_every == 0:
                    self.highlighted = [j, j + 1]
                    self.drawNums()
                    await asyncio.sleep(0)
            if not swapped:
                break
        await self.final_pass()

    async def selectionSort(self):
        self.comps = 0
        draw_every = max(1, self.numBars // 100)
        for i in range(self.numBars - 1):
            for j in range(i + 1, self.numBars):
                self.comps += 1
                if (self.vals[i] > self.vals[j]) if not self.descending else (self.vals[i] < self.vals[j]):
                    swapVals(self.vals, i, j)
                if self.comps % draw_every == 0:
                    self.highlighted = [i, j]
                    self.drawNums()
                    await asyncio.sleep(0)
        await self.final_pass()

    def merge(self, begin, mid, end):
        x, y = begin, mid + 1
        tmp = []
        for i in range(begin, end + 1):
            if x > mid:
                tmp.append(self.vals[y]); y += 1
            elif y > end:
                tmp.append(self.vals[x]); x += 1
            elif (self.vals[x] < self.vals[y]) if not self.descending else (self.vals[x] > self.vals[y]):
                self.comps += 1
                tmp.append(self.vals[x]); x += 1
            else:
                self.comps += 1
                tmp.append(self.vals[y]); y += 1
        for i in range(len(tmp)):
            self.vals[begin] = tmp[i]
            begin += 1

    async def mergeSort(self, begin, end):
        if begin < end:
            mid = (begin + end) // 2
            await self.mergeSort(begin, mid)
            await self.mergeSort(mid + 1, end)
            self.merge(begin, mid, end)
            self.highlighted = list(range(begin, end + 1))
            self.drawNums()
            await asyncio.sleep(0)

    async def mergeSortWrap(self):
        self.comps = 0
        await self.mergeSort(0, self.numBars - 1)
        await self.final_pass()

    async def partition(self, left, right):
        pivot = self.vals[right]
        i = left - 1
        for j in range(left, right):
            self.comps += 1
            if (self.vals[j] <= pivot) if not self.descending else (self.vals[j] >= pivot):
                i += 1
                swapVals(self.vals, i, j)
                self.highlighted = [j, right]
                self.drawNums()
                await asyncio.sleep(0)
        swapVals(self.vals, i + 1, right)
        self.highlighted = [i + 1, right]
        self.drawNums()
        await asyncio.sleep(0)
        return i + 1

    async def quicksort(self, begin, end):
        if begin < end:
            pivot = await self.partition(begin, end)
            await self.quicksort(begin, pivot - 1)
            await self.quicksort(pivot + 1, end)

    async def quickSortWrap(self):
        self.comps = 0
        await self.quicksort(0, self.numBars - 1)
        await self.final_pass()

    def countingSort(self, exp1):
        n = self.numBars
        output = [0] * n
        count = [0] * 10
        for i in range(n):
            index = self.vals[i] // exp1
            count[index % 10] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        i = n - 1
        while i >= 0:
            index = self.vals[i] // exp1
            output[count[index % 10] - 1] = self.vals[i]
            count[index % 10] -= 1
            i -= 1
        for i in range(n):
            self.vals[i] = output[i]
            self.highlighted = [i]

    async def radixSort(self):
        self.comps = 0
        max1 = max(self.vals)
        exp = 1
        while max1 // exp >= 1:
            self.countingSort(exp)
            self.drawNums()
            await asyncio.sleep(0)
            exp *= 10
        if self.descending:
            self.vals.reverse()
        await self.final_pass()
