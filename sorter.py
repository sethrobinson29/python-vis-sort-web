# Class for animating sorting algorithms (Pygame version)
# By Seth Robinson https://github.com/sethrobinson29
import asyncio
import pygame
from random import shuffle

# swap function
def swapVals(arr, i, j):
    tmp = arr[j]
    arr[j] = arr[i]
    arr[i] = tmp

# colors for drawing values — pre-converted from hex to RGB
_hex_colors = ["#F9035E", "#F01E5F", "#E73860", "#DE5361", "#D56E62",
               "#CC8864", "#C3A365", "#BABE66", "#B1D867", "#A8F368"]
colors = [pygame.Color(c) for c in _hex_colors]


class Sorter:
    def __init__(self, surface, width=1015, height=550):
        self.surface = surface
        self.width = width
        self.height = height
        self.vals = []
        self.numBars = 0
        self.comps = 0

    def makeNewVals(self, length):
        self.numBars = length
        self.vals = list(range(length))
        shuffle(self.vals)
        self.comps = 0
        self.drawNums()

    def drawNums(self):
        self.surface.fill((0, 0, 52))
        x = 10
        bar_width = max(1, self.width // self.numBars) if self.numBars else 1
        x_step = (self.width - 10) / self.numBars if self.numBars else 1

        for i in range(self.numBars):
            color_idx = (self.vals[i] % 100) // 10 if self.vals[i] > 9 else 0
            color = colors[color_idx]
            bar_height = self.vals[i]
            pygame.draw.line(
                self.surface,
                color,
                (int(x), self.height),
                (int(x), self.height - bar_height),
                1,
            )
            x += x_step

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
        self.drawNums()
        await asyncio.sleep(0)

    async def bubbleSort(self):
        self.comps = 0
        draw_every = max(1, self.numBars // 100)
        for i in range(self.numBars - 1):
            for j in range(self.numBars - i - 1):
                self.comps += 1
                if self.vals[j] > self.vals[j + 1]:
                    swapVals(self.vals, j, j + 1)
                if self.comps % draw_every == 0:
                    self.drawNums()
                    await asyncio.sleep(0)
        self.drawNums()
        await asyncio.sleep(0)

    async def selectionSort(self):
        self.comps = 0
        draw_every = max(1, self.numBars // 100)
        for i in range(self.numBars - 1):
            for j in range(i + 1, self.numBars):
                self.comps += 1
                if self.vals[i] > self.vals[j]:
                    swapVals(self.vals, i, j)
                if self.comps % draw_every == 0:
                    self.drawNums()
                    await asyncio.sleep(0)
        self.drawNums()
        await asyncio.sleep(0)

    def merge(self, begin, mid, end):
        x, y = begin, mid + 1
        tmp = []
        for i in range(begin, end + 1):
            if x > mid:
                tmp.append(self.vals[y]); y += 1
            elif y > end:
                tmp.append(self.vals[x]); x += 1
            elif self.vals[x] < self.vals[y]:
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
            self.drawNums()
            await asyncio.sleep(0)

    async def mergeSortWrap(self):
        self.comps = 0
        await self.mergeSort(0, self.numBars - 1)
        self.drawNums()
        await asyncio.sleep(0)

    async def partition(self, left, right):
        pivot = self.vals[right]
        i = left - 1
        for j in range(left, right):
            self.comps += 1
            if self.vals[j] <= pivot:
                i += 1
                swapVals(self.vals, i, j)
                self.drawNums()
                await asyncio.sleep(0)
        swapVals(self.vals, i + 1, right)
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
        self.drawNums()
        await asyncio.sleep(0)

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

    async def radixSort(self):
        self.comps = 0
        max1 = max(self.vals)
        exp = 1
        while max1 // exp >= 1:
            self.countingSort(exp)
            self.drawNums()
            await asyncio.sleep(0)
            exp *= 10
        self.drawNums()
        await asyncio.sleep(0)
