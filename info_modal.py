import pygame
from theme import (
    WIN_GRAY, WIN_LIGHT, WIN_DARK, WIN_DARKER,
    WIN_NAVY, WIN_NAVY2, WIN_TEXT, WIN_WHITE, WIN_RED,
    WIN_W, WIN_H,
    draw_raised, draw_sunken, _font,
)

# ── Algorithm data ────────────────────────────────────────────────────────────
ALGO_INFO = {
    "bubble": {
        "name": "Bubble Sort",
        "complexity": [
            ("Worst",   "O(n²)"),
            ("Best",    "O(n)"),
            ("Average", "O(n²)"),
            ("Space",   "O(1)"),
        ],
        "creator": "Independently described by multiple authors; earliest known formal analysis by Iverson (1962) in 'A Programming Language'.",
        "usages": [
            "Educational tool to introduce sorting concepts",
            "Useful for nearly-sorted small datasets",
            "Embedded systems where code simplicity matters more than speed",
        ],
        "summary": (
            "Bubble sort repeatedly steps through the list comparing adjacent elements and "
            "swapping them if they are in the wrong order. Larger elements 'bubble' toward "
            "the end of the array with each pass. The algorithm terminates early if a full "
            "pass completes without any swaps, indicating the list is already sorted."
        ),
        "diagram": "bubble",
    },
    "selection": {
        "name": "Selection Sort",
        "complexity": [
            ("Worst",   "O(n²)"),
            ("Best",    "O(n²)"),
            ("Average", "O(n²)"),
            ("Space",   "O(1)"),
        ],
        "creator": "Unknown origin; described informally in early computing literature. Knuth discussed it in 'The Art of Computer Programming' (1973).",
        "usages": [
            "Small arrays where auxiliary memory is very limited",
            "Minimizing the number of writes (swaps) to storage",
            "Teaching comparisons vs. swaps as separate cost metrics",
        ],
        "summary": (
            "Selection sort divides the array into a sorted left portion and an unsorted right "
            "portion. On each pass it scans the unsorted section to find the minimum element, "
            "then swaps it into the first unsorted position. This is repeated until the entire "
            "array is sorted. The number of swaps is always O(n), even though comparisons remain O(n²)."
        ),
        "diagram": "selection",
    },
    "merge": {
        "name": "Merge Sort",
        "complexity": [
            ("Worst",   "O(n log n)"),
            ("Best",    "O(n log n)"),
            ("Average", "O(n log n)"),
            ("Space",   "O(n)"),
        ],
        "creator": "Invented by John von Neumann in 1945 while working at the Institute for Advanced Study, Princeton.",
        "usages": [
            "Sorting linked lists efficiently",
            "External sorting of data too large to fit in memory",
            "Stable sort requirement in language standard libraries (e.g. Python's sort)",
            "Parallel sorting algorithms as a divide-and-conquer base",
        ],
        "summary": (
            "Merge sort is a divide-and-conquer algorithm that recursively splits the array "
            "in half until each sub-array contains a single element, then merges the sub-arrays "
            "back together in sorted order. The merge step compares the front elements of two "
            "sorted halves and builds a combined sorted result. It is stable and guarantees "
            "O(n log n) performance regardless of input order."
        ),
        "diagram": "merge",
    },
    "quick": {
        "name": "Quick Sort",
        "complexity": [
            ("Worst",   "O(n²)"),
            ("Best",    "O(n log n)"),
            ("Average", "O(n log n)"),
            ("Space",   "O(log n)"),
        ],
        "creator": "Invented by Tony Hoare in 1959 while working at Moscow State University, published 1961.",
        "usages": [
            "General-purpose in-place sorting (C stdlib qsort, C++ std::sort)",
            "Database query engines for in-memory record sorting",
            "Situations where average-case speed matters more than worst-case guarantees",
        ],
        "summary": (
            "Quick sort selects a pivot element and partitions the array so that all elements "
            "smaller than the pivot are to its left and all larger elements are to its right. "
            "It then recursively sorts each partition. Pivot choice (first, last, median-of-three, "
            "random) greatly affects performance; poor pivots lead to O(n²) worst-case behavior. "
            "In practice it is often the fastest comparison sort due to excellent cache locality."
        ),
        "diagram": "quick",
    },
    "radix": {
        "name": "Radix Sort",
        "complexity": [
            ("Worst",   "O(nk)"),
            ("Best",    "O(nk)"),
            ("Average", "O(nk)"),
            ("Space",   "O(n + k)"),
        ],
        "creator": "Concept dates to Herman Hollerith's punched-card tabulating machines (1887). LSD radix sort formalized in early IBM card-sorter documentation (~1920s).",
        "usages": [
            "Sorting large sets of fixed-width integers or strings",
            "Network packet routing tables",
            "Suffix array construction in bioinformatics",
            "GPU-based parallel sorting of integer keys",
        ],
        "summary": (
            "Radix sort is a non-comparative sorting algorithm that processes elements digit by "
            "digit, from the least significant digit (LSD) to the most significant digit (MSD). "
            "At each digit position, elements are distributed into 10 buckets (0-9) using a "
            "stable counting sort, then collected back in order. After processing all digit "
            "positions the array is fully sorted. Its time complexity is O(nk) where k is the "
            "number of digits, making it linear for fixed-width integers."
        ),
        "diagram": "radix",
    },
    "insertion": {
        "name": "Insertion Sort",
        "complexity": [
            ("Worst",   "O(n²)"),
            ("Best",    "O(n)"),
            ("Average", "O(n²)"),
            ("Space",   "O(1)"),
        ],
        "creator": "Unknown origin; one of the oldest known sorting methods. Described formally in Knuth's 'The Art of Computer Programming' Vol. 3 (1973).",
        "usages": [
            "Small arrays (typically n < 20) as a base case in hybrid sorts",
            "Nearly-sorted or streaming data where elements arrive one at a time",
            "Online algorithms that must sort as data arrives",
            "Used as a component in Timsort and Shell sort",
        ],
        "summary": (
            "Insertion sort builds the sorted array one element at a time. It takes the next "
            "unsorted element and scans backward through the sorted portion, shifting elements "
            "right until finding the correct insertion position. This mirrors how a card player "
            "sorts a hand of cards. It is adaptive (O(n) on nearly-sorted input), stable, and "
            "in-place, making it ideal as a finishing step in more complex algorithms."
        ),
        "diagram": "insertion",
    },
    "heap": {
        "name": "Heap Sort",
        "complexity": [
            ("Worst",   "O(n log n)"),
            ("Best",    "O(n log n)"),
            ("Average", "O(n log n)"),
            ("Space",   "O(1)"),
        ],
        "creator": "Invented by J. W. J. Williams in 1964, with improvements to the build-heap phase by Robert Floyd in 1964.",
        "usages": [
            "Systems requiring guaranteed O(n log n) worst-case with O(1) space",
            "Priority queues as the underlying data structure",
            "Real-time systems where worst-case guarantees are essential",
            "Partial sorts (finding the k largest/smallest elements)",
        ],
        "summary": (
            "Heap sort first transforms the array into a max-heap — a complete binary tree "
            "where each parent is larger than its children — using the heapify procedure. "
            "It then repeatedly extracts the maximum element (the root) by swapping it with "
            "the last element, shrinking the heap by one, and sifting the new root down to "
            "restore the heap property. This guarantees O(n log n) in all cases with O(1) "
            "auxiliary space, though it is not stable."
        ),
        "diagram": "heap",
    },
    "shell": {
        "name": "Shell Sort",
        "complexity": [
            ("Worst",   "O(n²) or O(n log² n)"),
            ("Best",    "O(n log n)"),
            ("Average", "depends on gap sequence"),
            ("Space",   "O(1)"),
        ],
        "creator": "Invented by Donald Shell in 1959, published in 'A High-Speed Sorting Procedure' in Communications of the ACM.",
        "usages": [
            "Embedded systems requiring in-place sorting without recursion",
            "Medium-sized arrays where simplicity and speed both matter",
            "uClibc and other resource-constrained C libraries",
        ],
        "summary": (
            "Shell sort is a generalization of insertion sort that allows the exchange of "
            "elements far apart in the array. It starts with a large gap between compared "
            "elements and progressively reduces the gap (often using the sequence n/2, n/4, …, 1). "
            "At each gap size it performs a gap-insertion sort. By the time the gap reaches 1 "
            "the array is nearly sorted, so the final pass is very fast. The choice of gap "
            "sequence significantly affects performance."
        ),
        "diagram": "shell",
    },
    "tim": {
        "name": "Timsort",
        "complexity": [
            ("Worst",   "O(n log n)"),
            ("Best",    "O(n)"),
            ("Average", "O(n log n)"),
            ("Space",   "O(n)"),
        ],
        "creator": "Invented by Tim Peters in 2002 for CPython. Named after its creator.",
        "usages": [
            "Python's built-in sort() and sorted() since Python 2.3",
            "Java's Arrays.sort() for objects since Java 7",
            "Android platform sorting routines",
            "Real-world datasets that contain partially sorted runs",
        ],
        "summary": (
            "Timsort is a hybrid stable sorting algorithm derived from merge sort and insertion "
            "sort. It identifies naturally occurring 'runs' of consecutive sorted (or reverse-sorted) "
            "elements in the input and extends short runs using insertion sort. Runs are then "
            "merged using a merge strategy that adapts to the run structure. Timsort uses a "
            "stack to track pending merges and applies the 'galloping' optimization to skip "
            "large blocks during merging, achieving excellent performance on real-world data."
        ),
        "diagram": "tim",
    },
    "cocktail": {
        "name": "Cocktail Shaker Sort",
        "complexity": [
            ("Worst",   "O(n²)"),
            ("Best",    "O(n)"),
            ("Average", "O(n²)"),
            ("Space",   "O(1)"),
        ],
        "creator": "Unknown origin; a natural bidirectional extension of bubble sort. Also called bidirectional bubble sort or shaker sort.",
        "usages": [
            "Educational variant showing bidirectional traversal",
            "Slight improvement over bubble sort on certain input patterns (turtles)",
            "Small nearly-sorted arrays",
        ],
        "summary": (
            "Cocktail shaker sort is a bidirectional variant of bubble sort. Instead of always "
            "traversing left-to-right, it alternates direction each pass: a forward pass bubbles "
            "the largest unsorted element to the right, then a backward pass bubbles the smallest "
            "unsorted element to the left. This addresses bubble sort's 'turtle' problem where "
            "small elements near the end take many passes to reach their correct positions."
        ),
        "diagram": "cocktail",
    },
    "comb": {
        "name": "Comb Sort",
        "complexity": [
            ("Worst",   "O(n²)"),
            ("Best",    "O(n log n)"),
            ("Average", "O(n²/2^p) for p increments"),
            ("Space",   "O(1)"),
        ],
        "creator": "Invented by Włodzimierz Dobosiewicz in 1980; popularized and named by Stephen Lacey and Richard Box in a 1991 Byte Magazine article.",
        "usages": [
            "Simple improvement over bubble sort with minimal code change",
            "Situations where bubble sort would be chosen but speed matters slightly more",
        ],
        "summary": (
            "Comb sort improves on bubble sort by eliminating 'turtles' — small values near the "
            "end of the list that slow bubble sort down. Instead of always comparing adjacent "
            "elements, comb sort starts with a large gap between compared elements and shrinks it "
            "by a shrink factor (typically 1.3) on each pass until the gap reaches 1, at which "
            "point it behaves like bubble sort. The large initial gap moves turtles quickly toward "
            "their correct positions."
        ),
        "diagram": "comb",
    },
    "gnome": {
        "name": "Gnome Sort",
        "complexity": [
            ("Worst",   "O(n²)"),
            ("Best",    "O(n)"),
            ("Average", "O(n²)"),
            ("Space",   "O(1)"),
        ],
        "creator": "Invented by Hamid Sarbazi-Azad in 2000 as 'Stupid Sort'; renamed Gnome Sort by Dick Grune in 2000 based on how a Dutch garden gnome would sort flower pots.",
        "usages": [
            "Purely educational — demonstrates a very simple yet correct sorting algorithm",
            "Extremely small arrays where code simplicity is paramount",
        ],
        "summary": (
            "Gnome sort works by finding the first place where two adjacent elements are out of "
            "order and swapping them, then stepping backward to verify the swap did not violate "
            "order with the previous element. It continues stepping back until the element is in "
            "its correct position, then advances forward again. It is essentially insertion sort "
            "implemented as a walk forward and backward through the array, with no explicit "
            "inner loop — only a single conditional at each step."
        ),
        "diagram": "gnome",
    },
    "cycle": {
        "name": "Cycle Sort",
        "complexity": [
            ("Worst",   "O(n²)"),
            ("Best",    "O(n²)"),
            ("Average", "O(n²)"),
            ("Space",   "O(1)"),
        ],
        "creator": "Described by Haddon in 1990 in 'Cycle-sort: A Linear Sorting Method' in The Computer Journal.",
        "usages": [
            "Minimizing write operations to storage (flash memory, EEPROM)",
            "Theoretically optimal number of writes: at most n-1 writes total",
            "Situations where write cost greatly exceeds read cost",
        ],
        "summary": (
            "Cycle sort is an in-place, unstable sorting algorithm that is theoretically optimal "
            "in terms of the total number of writes to the original array. It works by "
            "decomposing the permutation of elements into cycles. For each cycle, it rotates "
            "the elements into their correct positions, performing exactly one write per element "
            "per cycle. The total number of writes is minimized to at most n-1, making it "
            "valuable when write operations are significantly more expensive than reads."
        ),
        "diagram": "cycle",
    },
}


# ── Diagram drawing functions ─────────────────────────────────────────────────

def _draw_bubble_diagram(surf, rect):
    """7 bars, centre two highlighted; swap label + arrow above those bars."""
    r = pygame.Rect(rect)
    surf.fill(WIN_GRAY, r)
    n = 7
    heights = [55, 30, 75, 90, 45, 65, 40]
    font = _font(10)
    baseline = r.bottom - 14
    bar_area_h = baseline - r.y - 30   # leave 30px top margin for label
    scale = bar_area_h / max(heights)
    scaled = [int(h * scale) for h in heights]
    bar_w = (r.width - 20) // n
    gap = max(1, (r.width - 20 - n * bar_w) // max(n - 1, 1))
    highlight_indices = {2, 3}
    for i, h in enumerate(scaled):
        bx = r.x + 10 + i * (bar_w + gap)
        color = WIN_NAVY2 if i in highlight_indices else WIN_NAVY
        pygame.draw.rect(surf, color, (bx, baseline - h, bar_w, h))
        pygame.draw.rect(surf, WIN_DARKER, (bx, baseline - h, bar_w, h), 1)
    # double-headed arrow between bars 2 and 3, sitting just above them
    x2 = r.x + 10 + 2 * (bar_w + gap) + bar_w
    x3 = r.x + 10 + 3 * (bar_w + gap)
    mid_x = (x2 + x3) // 2
    ay = baseline - max(scaled[2], scaled[3]) - 18
    pygame.draw.line(surf, WIN_RED, (x2 + 2, ay + 5), (x3 - 2, ay + 5), 2)
    pygame.draw.line(surf, WIN_RED, (x2 + 2, ay + 5), (x2 + 7, ay + 2), 2)
    pygame.draw.line(surf, WIN_RED, (x2 + 2, ay + 5), (x2 + 7, ay + 8), 2)
    pygame.draw.line(surf, WIN_RED, (x3 - 2, ay + 5), (x3 - 7, ay + 2), 2)
    pygame.draw.line(surf, WIN_RED, (x3 - 2, ay + 5), (x3 - 7, ay + 8), 2)
    lbl = font.render("swap", False, WIN_RED)
    surf.blit(lbl, lbl.get_rect(centerx=mid_x, bottom=ay - 2))
    pygame.draw.line(surf, WIN_DARKER, (r.x + 8, baseline), (r.right - 8, baseline), 1)


def _draw_selection_diagram(surf, rect):
    """7 bars, triangle pointer under minimum, dashed swap line, color legend."""
    r = pygame.Rect(rect)
    surf.fill(WIN_GRAY, r)
    n = 7
    heights = [55, 30, 75, 90, 25, 65, 40]
    LEGEND_H = 18
    baseline = r.bottom - 26
    bar_area_h = baseline - r.y - 6
    scale = bar_area_h / max(heights)
    scaled = [int(h * scale) for h in heights]
    bar_w = (r.width - 20) // n
    gap = max(1, (r.width - 20 - n * bar_w) // max(n - 1, 1))
    sorted_end = 1
    min_idx = 4
    font = _font(10)
    SORTED_COL = WIN_DARK
    MIN_COL    = WIN_NAVY2
    SWAP_COL   = WIN_RED
    UNSORTED_COL = WIN_NAVY
    for i, h in enumerate(scaled):
        bx = r.x + 10 + i * (bar_w + gap)
        if i < sorted_end:
            color = SORTED_COL
        elif i == min_idx:
            color = MIN_COL
        elif i == sorted_end:
            color = SWAP_COL
        else:
            color = UNSORTED_COL
        pygame.draw.rect(surf, color, (bx, baseline - h, bar_w, h))
        pygame.draw.rect(surf, WIN_DARKER, (bx, baseline - h, bar_w, h), 1)
    min_bx = r.x + 10 + min_idx * (bar_w + gap) + bar_w // 2
    swap_bx = r.x + 10 + sorted_end * (bar_w + gap) + bar_w // 2
    tri_y = baseline + 2
    pygame.draw.polygon(surf, MIN_COL, [
        (min_bx, tri_y), (min_bx - 5, tri_y + 7), (min_bx + 5, tri_y + 7)
    ])
    pygame.draw.line(surf, WIN_DARKER, (r.x + 8, baseline), (r.right - 8, baseline), 1)
    # legend row: small coloured squares + labels
    legend_y = r.bottom - LEGEND_H
    items = [(SORTED_COL, "sorted"), (SWAP_COL, "swap target"), (MIN_COL, "current min"), (UNSORTED_COL, "unsorted")]
    lx = r.x + 6
    for col, label in items:
        pygame.draw.rect(surf, col, (lx, legend_y + 3, 10, 10))
        pygame.draw.rect(surf, WIN_DARKER, (lx, legend_y + 3, 10, 10), 1)
        lt = font.render(label, False, WIN_TEXT)
        surf.blit(lt, (lx + 13, legend_y + 2))
        lx += 13 + lt.get_width() + 8


def _draw_insertion_diagram(surf, rect):
    """Left half sorted (navy), current element highlighted; arrow shows insertion."""
    r = pygame.Rect(rect)
    surf.fill(WIN_GRAY, r)
    n = 7
    heights = [20, 35, 50, 65, 45, 80, 60]
    LEGEND_H = 18
    font = _font(10)
    baseline = r.bottom - LEGEND_H - 14
    bar_area_h = baseline - r.y - 10
    scale = bar_area_h / max(heights)
    scaled = [int(h * scale) for h in heights]
    bar_w = (r.width - 20) // n
    gap = max(1, (r.width - 20 - n * bar_w) // max(n - 1, 1))
    sorted_count = 4
    insert_idx = 4
    sorted_right = r.x + 10 + sorted_count * (bar_w + gap) - gap // 2
    SORTED_COL = WIN_NAVY
    INSERT_COL = WIN_NAVY2
    UNSORTED_COL = WIN_DARK
    for i, h in enumerate(scaled):
        bx = r.x + 10 + i * (bar_w + gap)
        if i < sorted_count:
            color = SORTED_COL
        elif i == insert_idx:
            color = INSERT_COL
        else:
            color = UNSORTED_COL
        pygame.draw.rect(surf, color, (bx, baseline - h, bar_w, h))
        pygame.draw.rect(surf, WIN_DARKER, (bx, baseline - h, bar_w, h), 1)
    pygame.draw.line(surf, WIN_DARKER, (sorted_right, r.y + 6), (sorted_right, baseline), 2)
    # arrow above inserted bar pointing left
    ins_cx = r.x + 10 + insert_idx * (bar_w + gap) + bar_w // 2
    ay = baseline - scaled[insert_idx] - 12
    pygame.draw.line(surf, WIN_RED, (ins_cx + 2, ay), (ins_cx - bar_w - gap + 2, ay), 2)
    pygame.draw.line(surf, WIN_RED, (ins_cx - bar_w - gap + 2, ay),
                     (ins_cx - bar_w - gap + 8, ay - 4), 2)
    pygame.draw.line(surf, WIN_RED, (ins_cx - bar_w - gap + 2, ay),
                     (ins_cx - bar_w - gap + 8, ay + 4), 2)
    pygame.draw.line(surf, WIN_DARKER, (r.x + 8, baseline), (r.right - 8, baseline), 1)
    # color-swatch legend
    legend_y = r.bottom - LEGEND_H
    items = [(SORTED_COL, "sorted"), (INSERT_COL, "inserting"), (UNSORTED_COL, "unsorted")]
    lx = r.x + 6
    for col, label in items:
        pygame.draw.rect(surf, col, (lx, legend_y + 3, 10, 10))
        pygame.draw.rect(surf, WIN_DARKER, (lx, legend_y + 3, 10, 10), 1)
        lt = font.render(label, False, WIN_TEXT)
        surf.blit(lt, (lx + 13, legend_y + 2))
        lx += 13 + lt.get_width() + 10


def _draw_merge_diagram(surf, rect):
    """Binary tree: unsorted -> halves -> quarters with split/merge arrows."""
    r = pygame.Rect(rect)
    surf.fill(WIN_GRAY, r)
    font = _font(10)
    # Reserve right margin for labels
    LBL_W = 68
    box_w = r.width - LBL_W - 8
    pad = 6
    BOX_H = 20
    GAP_H = 18   # gap between rows (arrows drawn here)
    rows_h = 3 * BOX_H + 2 * GAP_H
    top = r.y + (r.height - rows_h) // 2
    lbl_x = r.x + box_w + 4

    def draw_row_boxes(y, count, color, label_fmt):
        bw = (box_w - 2 * pad - (count - 1) * 3) // count
        for i in range(count):
            bx = r.x + pad + i * (bw + 3)
            rr = pygame.Rect(bx, y, bw, BOX_H)
            draw_sunken(surf, rr, color)
            t = font.render(label_fmt(i), False, WIN_WHITE)
            surf.blit(t, t.get_rect(center=rr.center))
        return y + BOX_H

    # row 0 — full array
    y = top
    y_after0 = draw_row_boxes(y, 1, WIN_NAVY, lambda i: "unsorted array")
    # split arrow + label
    gap_mid = y_after0 + GAP_H // 2
    for bx_c in [r.x + box_w // 4, r.x + 3 * box_w // 4]:
        pygame.draw.line(surf, WIN_DARKER, (bx_c, y_after0 + 2), (bx_c, y_after0 + GAP_H - 2), 1)
        pygame.draw.polygon(surf, WIN_DARKER, [(bx_c, y_after0 + GAP_H - 2),
                                               (bx_c - 4, y_after0 + GAP_H - 8),
                                               (bx_c + 4, y_after0 + GAP_H - 8)])
    split_lbl = font.render("split", False, WIN_DARKER)
    surf.blit(split_lbl, (lbl_x, gap_mid - split_lbl.get_height() // 2))
    # row 1 — two halves
    y = y_after0 + GAP_H
    y_after1 = draw_row_boxes(y, 2, WIN_DARK, lambda i: f"half {i+1}")
    # split arrow again
    gap_mid2 = y_after1 + GAP_H // 2
    for bx_c in [r.x + box_w // 8, r.x + 3 * box_w // 8, r.x + 5 * box_w // 8, r.x + 7 * box_w // 8]:
        pygame.draw.line(surf, WIN_DARKER, (bx_c, y_after1 + 2), (bx_c, y_after1 + GAP_H - 2), 1)
        pygame.draw.polygon(surf, WIN_DARKER, [(bx_c, y_after1 + GAP_H - 2),
                                               (bx_c - 4, y_after1 + GAP_H - 8),
                                               (bx_c + 4, y_after1 + GAP_H - 8)])
    surf.blit(split_lbl, (lbl_x, gap_mid2 - split_lbl.get_height() // 2))
    # row 2 — four quarters
    y = y_after1 + GAP_H
    draw_row_boxes(y, 4, (80, 80, 130), lambda i: str(i + 1))
    merge_lbl = font.render("merge", False, WIN_NAVY)
    surf.blit(merge_lbl, (lbl_x, gap_mid2 - merge_lbl.get_height() // 2 + GAP_H + BOX_H + 4))


def _draw_quick_diagram(surf, rect):
    """7 bars, one pivot bar, left side darker, right side lighter, labels."""
    r = pygame.Rect(rect)
    surf.fill(WIN_GRAY, r)
    n = 7
    pivot_idx = 3
    heights = [40, 25, 55, 70, 85, 60, 45]
    bar_w = (r.width - 20) // n
    gap = max(1, (r.width - 20 - n * bar_w) // max(n - 1, 1))
    baseline = r.bottom - 24
    font = _font(10)
    for i, h in enumerate(heights):
        bx = r.x + 10 + i * (bar_w + gap)
        if i == pivot_idx:
            color = WIN_NAVY2
        elif i < pivot_idx:
            color = (60, 60, 100)
        else:
            color = (140, 160, 200)
        pygame.draw.rect(surf, color, (bx, baseline - h, bar_w, h))
        pygame.draw.rect(surf, WIN_DARKER, (bx, baseline - h, bar_w, h), 1)
    # pivot label
    piv_bx = r.x + 10 + pivot_idx * (bar_w + gap) + bar_w // 2
    plbl = font.render("pivot", False, WIN_NAVY2)
    surf.blit(plbl, plbl.get_rect(centerx=piv_bx, bottom=baseline - heights[pivot_idx] - 2))
    # < pivot and > pivot labels
    ll = font.render("< pivot", False, WIN_LIGHT)
    rl = font.render("> pivot", False, WIN_DARK)
    left_cx = r.x + 10 + (pivot_idx // 2) * (bar_w + gap)
    right_cx = r.x + 10 + (pivot_idx + 2) * (bar_w + gap)
    surf.blit(ll, (r.x + 10, r.bottom - 14))
    surf.blit(rl, (r.x + 10 + (pivot_idx + 1) * (bar_w + gap), r.bottom - 14))
    pygame.draw.line(surf, WIN_DARKER, (r.x + 8, baseline), (r.right - 8, baseline), 1)


def _draw_heap_diagram(surf, rect):
    """Binary tree with 7 nodes labeled as max-heap."""
    r = pygame.Rect(rect)
    surf.fill(WIN_GRAY, r)
    font = _font(10)
    # node values (max-heap)
    values = [90, 70, 75, 40, 60, 50, 65]
    # positions: row 0 center, row 1 two, row 2 four
    cx = r.x + r.width // 2
    node_r = 14
    row_h = (r.height - 20) // 3
    positions = [
        (cx,                   r.y + 16),                          # 0 root
        (cx - r.width // 4,    r.y + 16 + row_h),                  # 1
        (cx + r.width // 4,    r.y + 16 + row_h),                  # 2
        (cx - 3 * r.width // 8, r.y + 16 + 2 * row_h),            # 3
        (cx - r.width // 8,   r.y + 16 + 2 * row_h),              # 4
        (cx + r.width // 8,   r.y + 16 + 2 * row_h),              # 5
        (cx + 3 * r.width // 8, r.y + 16 + 2 * row_h),            # 6
    ]
    # draw edges first
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
    for p, c in edges:
        pygame.draw.line(surf, WIN_DARKER, positions[p], positions[c], 1)
    # draw nodes
    for i, (px, py) in enumerate(positions):
        pygame.draw.circle(surf, WIN_NAVY, (px, py), node_r)
        pygame.draw.circle(surf, WIN_DARKER, (px, py), node_r, 1)
        lbl = font.render(str(values[i]), False, WIN_WHITE)
        surf.blit(lbl, lbl.get_rect(center=(px, py)))
    # label
    title_lbl = font.render("max-heap", False, WIN_DARKER)
    surf.blit(title_lbl, (r.x + 4, r.y + 2))


def _draw_shell_diagram(surf, rect):
    """One representative pair per gap phase; each gap colored and labeled."""
    r = pygame.Rect(rect)
    surf.fill(WIN_GRAY, r)
    n = 7
    heights = [55, 80, 30, 70, 45, 90, 35]
    LEGEND_H = 16
    font = _font(10)
    baseline = r.bottom - LEGEND_H - 14
    bar_area_h = baseline - r.y - 42   # top 42px for three arc levels + labels
    scale = bar_area_h / max(heights)
    scaled = [int(h * scale) for h in heights]
    bar_w = (r.width - 20) // n
    gap_px = max(1, (r.width - 20 - n * bar_w) // max(n - 1, 1))
    bar_cx = [r.x + 10 + i * (bar_w + gap_px) + bar_w // 2 for i in range(n)]

    # One non-overlapping pair per gap phase; larger gap → higher arc
    G3_COL = WIN_RED
    G2_COL = WIN_NAVY2
    G1_COL = (60, 160, 80)
    gap_pairs = [
        (3, 0, 3, G3_COL, "gap = 3", r.y + 6),
        (2, 4, 6, G2_COL, "gap = 2", r.y + 18),
        (1, 1, 2, G1_COL, "gap = 1", r.y + 30),
    ]
    pair_colors = {}
    for _, a, b, col, _, _ in gap_pairs:
        pair_colors[a] = col
        pair_colors[b] = col

    # draw bars
    for i, h in enumerate(scaled):
        bx = r.x + 10 + i * (bar_w + gap_px)
        color = pair_colors.get(i, WIN_NAVY)
        pygame.draw.rect(surf, color, (bx, baseline - h, bar_w, h))
        pygame.draw.rect(surf, WIN_DARKER, (bx, baseline - h, bar_w, h), 1)
    pygame.draw.line(surf, WIN_DARKER, (r.x + 8, baseline), (r.right - 8, baseline), 1)

    # draw one arc per gap + label at arc midpoint
    for _, a, b, col, label, arc_y in gap_pairs:
        x1, x2 = bar_cx[a], bar_cx[b]
        pts = [(x1, baseline - scaled[a] - 4), (x1, arc_y), (x2, arc_y),
               (x2, baseline - scaled[b] - 4)]
        pygame.draw.lines(surf, col, False, pts, 1)
        lbl = font.render(label, False, col)
        surf.blit(lbl, lbl.get_rect(centerx=(x1 + x2) // 2, top=arc_y + 2))

    # legend
    legend_y = r.bottom - LEGEND_H
    lx = r.x + 6
    for col, label in [(G3_COL, "gap = 3"), (G2_COL, "gap = 2"), (G1_COL, "gap = 1")]:
        pygame.draw.rect(surf, col, (lx, legend_y + 3, 10, 10))
        pygame.draw.rect(surf, WIN_DARKER, (lx, legend_y + 3, 10, 10), 1)
        lt = font.render(label, False, WIN_TEXT)
        surf.blit(lt, (lx + 13, legend_y + 2))
        lx += 13 + lt.get_width() + 10


def _draw_tim_diagram(surf, rect):
    """Two sorted runs shown; merge arrow below."""
    r = pygame.Rect(rect)
    surf.fill(WIN_GRAY, r)
    n = 7
    heights = [20, 35, 50, 65, 30, 55, 80]
    LEGEND_H = 18
    ARROW_AREA = 26   # space between baseline and legend for arrow row
    font = _font(10)
    baseline = r.bottom - LEGEND_H - ARROW_AREA
    bar_area_h = baseline - r.y - 20
    scale = bar_area_h / max(heights)
    scaled = [int(h * scale) for h in heights]
    bar_w = (r.width - 20) // n
    gap = max(1, (r.width - 20 - n * bar_w) // max(n - 1, 1))
    run1_end = 4
    RUN1_COL = WIN_NAVY
    RUN2_COL = (80, 80, 160)
    for i, h in enumerate(scaled):
        bx = r.x + 10 + i * (bar_w + gap)
        color = RUN1_COL if i < run1_end else RUN2_COL
        pygame.draw.rect(surf, color, (bx, baseline - h, bar_w, h))
        pygame.draw.rect(surf, WIN_DARKER, (bx, baseline - h, bar_w, h), 1)
    div_x = r.x + 10 + run1_end * (bar_w + gap) - gap // 2 - 1
    pygame.draw.line(surf, WIN_RED, (div_x, r.y + 8), (div_x, baseline + 2), 2)
    pygame.draw.line(surf, WIN_DARKER, (r.x + 8, baseline), (r.right - 8, baseline), 1)
    # merge annotation: "merge:" label inline to the left of the arrow
    arrow_y = baseline + ARROW_AREA // 2
    merge_lbl = font.render("merge:", False, WIN_DARKER)
    lbl_r = merge_lbl.get_rect(midleft=(r.x + 10, arrow_y))
    surf.blit(merge_lbl, lbl_r)
    ax1, ax2 = lbl_r.right + 4, r.right - 10
    pygame.draw.line(surf, WIN_DARKER, (ax1, arrow_y), (ax2, arrow_y), 1)
    pygame.draw.polygon(surf, WIN_DARKER, [(ax2, arrow_y), (ax2 - 6, arrow_y - 3), (ax2 - 6, arrow_y + 3)])
    # legend
    legend_y = r.bottom - LEGEND_H
    lx = r.x + 6
    for col, label in [(RUN1_COL, "run 1"), (RUN2_COL, "run 2")]:
        pygame.draw.rect(surf, col, (lx, legend_y + 3, 10, 10))
        pygame.draw.rect(surf, WIN_DARKER, (lx, legend_y + 3, 10, 10), 1)
        lt = font.render(label, False, WIN_TEXT)
        surf.blit(lt, (lx + 13, legend_y + 2))
        lx += 13 + lt.get_width() + 12


def _draw_cocktail_diagram(surf, rect):
    """7 bars; active element highlighted per pass; direction arrows below."""
    r = pygame.Rect(rect)
    surf.fill(WIN_GRAY, r)
    n = 7
    heights = [60, 30, 80, 45, 70, 25, 55]
    ARROW_AREA = 58   # height reserved below bars for two arrows + labels
    font = _font(10)
    baseline = r.bottom - ARROW_AREA - 8
    bar_area_h = baseline - r.y - 8
    scale = bar_area_h / max(heights)
    scaled = [int(h * scale) for h in heights]
    bar_w = (r.width - 20) // n
    gap = max(1, (r.width - 20 - n * bar_w) // max(n - 1, 1))
    # idx 2 = largest (value 80) being bubbled right; idx 5 = smallest (value 25) moving left
    FWD_IDX, BWD_IDX = 2, 5
    for i, h in enumerate(scaled):
        bx = r.x + 10 + i * (bar_w + gap)
        if i == FWD_IDX:
            color = WIN_NAVY2   # element moving in forward pass
        elif i == BWD_IDX:
            color = WIN_RED     # element moving in backward pass
        else:
            color = WIN_NAVY
        pygame.draw.rect(surf, color, (bx, baseline - h, bar_w, h))
        pygame.draw.rect(surf, WIN_DARKER, (bx, baseline - h, bar_w, h), 1)
    pygame.draw.line(surf, WIN_DARKER, (r.x + 8, baseline), (r.right - 8, baseline), 1)
    ax1 = r.x + 10
    ax2 = r.right - 10
    # forward pass arrow + label (first row below baseline)
    fwd_y = baseline + 22
    pygame.draw.line(surf, WIN_NAVY2, (ax1, fwd_y), (ax2, fwd_y), 2)
    pygame.draw.polygon(surf, WIN_NAVY2, [(ax2, fwd_y), (ax2 - 7, fwd_y - 4), (ax2 - 7, fwd_y + 4)])
    fwd_lbl = font.render("forward pass", False, WIN_NAVY2)
    surf.blit(fwd_lbl, fwd_lbl.get_rect(midleft=(ax1, fwd_y - 9)))
    # backward pass arrow + label (second row)
    bwd_y = baseline + 44
    pygame.draw.line(surf, WIN_RED, (ax2, bwd_y), (ax1, bwd_y), 2)
    pygame.draw.polygon(surf, WIN_RED, [(ax1, bwd_y), (ax1 + 7, bwd_y - 4), (ax1 + 7, bwd_y + 4)])
    bwd_lbl = font.render("backward pass", False, WIN_RED)
    surf.blit(bwd_lbl, bwd_lbl.get_rect(midleft=(ax1, bwd_y - 9)))


def _draw_comb_diagram(surf, rect):
    """One representative pair per gap phase; larger gap = wider arc = higher arc."""
    r = pygame.Rect(rect)
    surf.fill(WIN_GRAY, r)
    n = 7
    heights = [60, 30, 80, 45, 70, 25, 55]
    LEGEND_H = 18
    font = _font(10)
    baseline = r.bottom - LEGEND_H - 14
    bar_area_h = baseline - r.y - 50   # top 50px for three arc levels
    scale = bar_area_h / max(heights)
    scaled = [int(h * scale) for h in heights]
    bar_w = (r.width - 20) // n
    gap_px = max(1, (r.width - 20 - n * bar_w) // max(n - 1, 1))
    bar_cx = [r.x + 10 + i * (bar_w + gap_px) + bar_w // 2 for i in range(n)]

    # One non-overlapping pair per gap; larger gap → higher arc (more separation = bigger jump)
    G4_COL = WIN_RED
    G2_COL = WIN_NAVY2
    G1_COL = WIN_DARK
    # (gap_size, bar_a, bar_b, color, arc_top_y)
    gap_pairs = [
        (4, 0, 4, G4_COL, r.y + 6),    # bars 0 & 4 — widest span
        (2, 3, 5, G2_COL, r.y + 20),   # bars 3 & 5 — medium span
        (1, 1, 2, G1_COL, r.y + 34),   # bars 1 & 2 — narrowest span
    ]
    pair_colors = {}
    for _, a, b, col, _ in gap_pairs:
        pair_colors[a] = col
        pair_colors[b] = col

    # draw bars
    for i, h in enumerate(scaled):
        bx = r.x + 10 + i * (bar_w + gap_px)
        color = pair_colors.get(i, WIN_NAVY)
        pygame.draw.rect(surf, color, (bx, baseline - h, bar_w, h))
        pygame.draw.rect(surf, WIN_DARKER, (bx, baseline - h, bar_w, h), 1)
    pygame.draw.line(surf, WIN_DARKER, (r.x + 8, baseline), (r.right - 8, baseline), 1)

    # draw one arc per gap phase
    for _, a, b, col, arc_y in gap_pairs:
        x1, x2 = bar_cx[a], bar_cx[b]
        pts = [(x1, baseline - scaled[a] - 4), (x1, arc_y), (x2, arc_y),
               (x2, baseline - scaled[b] - 4)]
        pygame.draw.lines(surf, col, False, pts, 1)

    # color-swatch legend
    legend_y = r.bottom - LEGEND_H
    lx = r.x + 6
    for col, label in [(G4_COL, "gap 4"), (G2_COL, "gap 2"), (G1_COL, "gap 1")]:
        pygame.draw.rect(surf, col, (lx, legend_y + 3, 10, 10))
        pygame.draw.rect(surf, WIN_DARKER, (lx, legend_y + 3, 10, 10), 1)
        lt = font.render(label, False, WIN_TEXT)
        surf.blit(lt, (lx + 13, legend_y + 2))
        lx += 13 + lt.get_width() + 12


def _draw_gnome_diagram(surf, rect):
    """7 bars: forward-walk arrow above in-order region; step-back arrow below out-of-order pair."""
    r = pygame.Rect(rect)
    surf.fill(WIN_GRAY, r)
    n = 7
    heights    = [20, 35, 50, 80, 40, 65, 55]
    gnome_idx  = 4   # gnome is here (40) — out of order with element behind it (80)
    cmp_idx    = 3   # element being compared (80)
    font       = _font(10)
    FWDARROW_H = 20   # space at top reserved for the forward-walk arrow
    BKWARROW_H = 28   # space at bottom for the step-back arrow
    LEGEND_H   = 16
    baseline   = r.bottom - BKWARROW_H - LEGEND_H - 4
    bar_top    = r.y + FWDARROW_H + 4
    bar_area_h = baseline - bar_top
    scale      = bar_area_h / max(heights)
    scaled     = [int(h * scale) for h in heights]
    bar_w      = (r.width - 20) // n
    gap        = max(1, (r.width - 20 - n * bar_w) // max(n - 1, 1))

    PASSED_COL = WIN_NAVY
    CMP_COL    = WIN_NAVY2          # light blue — element being compared
    GNOME_COL  = (190, 70, 0)       # orange — gnome's position (out of order)
    AHEAD_COL  = WIN_DARK

    def bar_cx(i):
        return r.x + 10 + i * (bar_w + gap) + bar_w // 2

    for i, h in enumerate(scaled):
        bx = r.x + 10 + i * (bar_w + gap)
        if i < cmp_idx:
            color = PASSED_COL
        elif i == cmp_idx:
            color = CMP_COL
        elif i == gnome_idx:
            color = GNOME_COL
        else:
            color = AHEAD_COL
        pygame.draw.rect(surf, color, (bx, baseline - h, bar_w, h))
        pygame.draw.rect(surf, WIN_DARKER, (bx, baseline - h, bar_w, h), 1)
    pygame.draw.line(surf, WIN_DARKER, (r.x + 8, baseline), (r.right - 8, baseline), 1)

    # forward-walk arrow near top of bar area 0 → cmp_idx (all stepped forward because in order)
    fwd_y  = bar_top + 6    # sits just inside the bar area, overlapping the short bars is fine
    fwd_x1 = bar_cx(0)
    fwd_x2 = bar_cx(cmp_idx)
    pygame.draw.line(surf, WIN_NAVY, (fwd_x1, fwd_y), (fwd_x2, fwd_y), 2)
    pygame.draw.polygon(surf, WIN_NAVY, [(fwd_x2, fwd_y), (fwd_x2 - 7, fwd_y - 4), (fwd_x2 - 7, fwd_y + 4)])
    fwd_lbl = font.render("in order: step forward", False, WIN_NAVY)
    surf.blit(fwd_lbl, fwd_lbl.get_rect(
        centerx=(fwd_x1 + fwd_x2) // 2, top=fwd_y + 4))

    # step-back arrow below bars cmp_idx ← gnome_idx (out of order: swap + step back)
    bk_y   = baseline + 8
    bk_x1  = bar_cx(gnome_idx)
    bk_x2  = bar_cx(cmp_idx)
    pygame.draw.line(surf, WIN_RED, (bk_x1, bk_y), (bk_x2, bk_y), 2)
    pygame.draw.polygon(surf, WIN_RED, [(bk_x2, bk_y), (bk_x2 + 7, bk_y - 4), (bk_x2 + 7, bk_y + 4)])
    bk_lbl = font.render("out of order: swap + step back", False, WIN_RED)
    surf.blit(bk_lbl, bk_lbl.get_rect(
        centerx=(bk_x1 + bk_x2) // 2, top=bk_y + 8))

    # legend
    legend_y = r.bottom - LEGEND_H + 2
    for col, label, lx in [(CMP_COL,   "compare",  r.x + 6),
                            (GNOME_COL, "gnome",    r.x + 100),
                            (AHEAD_COL, "ahead",    r.x + 178)]:
        pygame.draw.rect(surf, col, (lx, legend_y, 10, 10))
        pygame.draw.rect(surf, WIN_DARKER, (lx, legend_y, 10, 10), 1)
        lt = font.render(label, False, WIN_TEXT)
        surf.blit(lt, (lx + 13, legend_y - 1))


def _draw_cycle_diagram(surf, rect):
    """Array [3,1,2,5,4] decomposed into 2 cycles; diagonal arrows connect each
    element to its destination box in sorted position order."""
    r = pygame.Rect(rect)
    surf.fill(WIN_GRAY, r)
    font = _font(10)
    sm   = _font(9)

    C1 = WIN_NAVY           # cycle 1 colour
    C2 = (130, 60, 0)       # cycle 2 colour (dark orange)
    BOX_W, BOX_H = 32, 20
    ARR_GAP  = 8   # gap between initial-array boxes
    CYC_GAP  = 8   # gap between boxes within a cycle row
    ARROW_H  = 6   # gap between top and bottom cycle rows

    # ── initial array row ─────────────────────────────────────────────────────
    array      = [3, 1, 2, 5, 4]
    box_colors = [C1, C1, C1, C2, C2]
    n = len(array)
    arr_w = n * BOX_W + (n - 1) * ARR_GAP
    arr_x = r.x + (r.width - arr_w) // 2
    arr_y = r.y + 4

    in_lbl = sm.render("input:", False, WIN_DARKER)
    surf.blit(in_lbl, (r.x + 4, arr_y + (BOX_H - in_lbl.get_height()) // 2))

    for i, (val, col) in enumerate(zip(array, box_colors)):
        bx = arr_x + i * (BOX_W + ARR_GAP)
        br = pygame.Rect(bx, arr_y, BOX_W, BOX_H)
        draw_sunken(surf, br, col)
        vt = font.render(str(val), False, WIN_WHITE)
        surf.blit(vt, vt.get_rect(center=br.center))
        it = sm.render(str(i), False, WIN_DARKER)
        surf.blit(it, it.get_rect(centerx=br.centerx, top=br.bottom + 3))

    div_y = arr_y + BOX_H + 18
    pygame.draw.line(surf, WIN_DARK, (r.x + 6, div_y), (r.right - 6, div_y), 1)

    # ── two cycle panels side by side ─────────────────────────────────────────
    panel_top = div_y + 7
    mid_x     = r.x + r.width // 2

    def draw_cycle(px, pw, elements, dest_pos, color, heading):
        h_surf = font.render(heading, False, color)
        surf.blit(h_surf, (px, panel_top))

        n_el    = len(elements)
        min_pos = min(dest_pos)
        row_w   = n_el * BOX_W + (n_el - 1) * CYC_GAP
        bx0     = px + (pw - row_w) // 2
        top_y   = panel_top + h_surf.get_height() + 5
        bot_y   = top_y + BOX_H + ARROW_H

        # build bottom row: slot_vals[dest - min_pos] = value
        slot_vals = [None] * n_el
        for j, (val, dst) in enumerate(zip(elements, dest_pos)):
            slot_vals[dst - min_pos] = val

        # top row — elements in write order
        for j, val in enumerate(elements):
            bx = bx0 + j * (BOX_W + CYC_GAP)
            br = pygame.Rect(bx, top_y, BOX_W, BOX_H)
            draw_sunken(surf, br, color)
            vt = font.render(str(val), False, WIN_WHITE)
            surf.blit(vt, vt.get_rect(center=br.center))

        # bottom row — elements in sorted position order, with position index labels
        for slot, val in enumerate(slot_vals):
            bx = bx0 + slot * (BOX_W + CYC_GAP)
            br = pygame.Rect(bx, bot_y, BOX_W, BOX_H)
            draw_sunken(surf, br, color)
            vt = font.render(str(val), False, WIN_WHITE)
            surf.blit(vt, vt.get_rect(center=br.center))
            pt = sm.render(str(min_pos + slot), False, WIN_DARKER)
            surf.blit(pt, pt.get_rect(centerx=br.centerx, top=br.bottom + 3))

    # Cycle 1: item 3 (at pos 0) -> pos 2; displaces 2 -> pos 1; displaces 1 -> pos 0
    draw_cycle(r.x + 2,   mid_x - r.x - 4,
               [3, 2, 1], [2, 1, 0], C1, "Cycle 1:")
    # Cycle 2: item 5 (at pos 3) -> pos 4; displaces 4 -> pos 3
    draw_cycle(mid_x + 2, r.right - mid_x - 2,
               [5, 4],    [4, 3],    C2, "Cycle 2:")


def _draw_radix_diagram(surf, rect):
    """3 rows of buckets 0-9 with elements showing LSD sort passes."""
    r = pygame.Rect(rect)
    surf.fill(WIN_GRAY, r)
    font = _font(9)
    n_buckets = 10
    bw = max(1, (r.width - 20) // n_buckets)
    bh = 18
    pad = 10
    labels = [str(i) for i in range(n_buckets)]
    # three passes (ones, tens, hundreds)
    pass_labels = ["pass 1: ones", "pass 2: tens", "pass 3: hundreds"]
    # sample occupancy per bucket per pass (for visual dots)
    occupancy = [
        [1, 0, 1, 1, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 1, 1, 0, 1, 0, 0, 1],
        [0, 0, 1, 0, 0, 1, 1, 0, 1, 0],
    ]
    for row, (occ, plbl) in enumerate(zip(occupancy, pass_labels)):
        ry = r.y + pad + row * (bh + 14)
        # pass label
        pl = font.render(plbl, False, WIN_DARKER)
        surf.blit(pl, (r.x + pad, ry - 10))
        for b in range(n_buckets):
            bx = r.x + pad + b * (bw + 1)
            bucket_rect = pygame.Rect(bx, ry, bw, bh)
            draw_sunken(surf, bucket_rect, WIN_WHITE if occ[b] == 0 else WIN_NAVY)
            bl = font.render(labels[b], False, WIN_DARKER if occ[b] == 0 else WIN_WHITE)
            surf.blit(bl, bl.get_rect(center=bucket_rect.center))
    # bottom label
    lbl = font.render("LSD: ones → tens → hundreds", False, WIN_DARKER)
    surf.blit(lbl, lbl.get_rect(centerx=r.centerx, bottom=r.bottom - 2))


_DIAGRAM_FUNCS = {
    "bubble":    _draw_bubble_diagram,
    "selection": _draw_selection_diagram,
    "insertion": _draw_insertion_diagram,
    "merge":     _draw_merge_diagram,
    "quick":     _draw_quick_diagram,
    "heap":      _draw_heap_diagram,
    "shell":     _draw_shell_diagram,
    "tim":       _draw_tim_diagram,
    "cocktail":  _draw_cocktail_diagram,
    "comb":      _draw_comb_diagram,
    "gnome":     _draw_gnome_diagram,
    "cycle":     _draw_cycle_diagram,
    "radix":     _draw_radix_diagram,
}


# ── Text helpers ──────────────────────────────────────────────────────────────

def _wrap_text(text, font, max_width):
    """Return list of strings each fitting within max_width pixels."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _build_content_surf(algo_key, font, bold_font, w):
    """Build and return a Surface of width w containing all sections for algo_key."""
    info = ALGO_INFO[algo_key]
    PAD_TOP    = 12
    SEC_GAP    = 14
    INSET_PAD  = 6
    TEXT_LEFT  = INSET_PAD + 4
    LINE_H     = font.get_linesize()
    BOLD_H     = bold_font.get_linesize()
    DIAG_H     = 150

    sections = []

    def measure_inset_height(lines_count, extra=0):
        return INSET_PAD * 2 + lines_count * LINE_H + extra

    # ── measure total height first, then render ───────────────────────────────
    # Time Complexity
    tc_lines = len(info["complexity"])
    tc_h = measure_inset_height(tc_lines)
    # Founder / Origin
    founder_wrapped = _wrap_text(info["creator"], font, w - 2 * INSET_PAD - 8)
    founder_h = measure_inset_height(len(founder_wrapped))
    # Main Usages
    usage_wrapped = []
    for usage in info["usages"]:
        wrapped = _wrap_text("• " + usage, font, w - 2 * INSET_PAD - 8)
        usage_wrapped.extend(wrapped)
    usage_h = measure_inset_height(len(usage_wrapped))
    # How It Works
    summary_wrapped = _wrap_text(info["summary"], font, w - 2 * INSET_PAD - 8)
    summary_h = measure_inset_height(len(summary_wrapped))
    # Visual Aid
    diag_h = INSET_PAD * 2 + DIAG_H

    section_data = [
        ("Time Complexity", tc_h),
        ("Founder / Origin", founder_h),
        ("Main Usages", usage_h),
        ("How It Works", summary_h),
        ("Diagram", diag_h),
    ]

    total_h = PAD_TOP
    for _, sh in section_data:
        total_h += BOLD_H + 2 + sh + SEC_GAP
    total_h += PAD_TOP

    surf = pygame.Surface((w, total_h))
    surf.fill(WIN_GRAY)

    y = PAD_TOP

    def draw_section_header(label, sy):
        lbl = bold_font.render(label, False, WIN_NAVY)
        surf.blit(lbl, (INSET_PAD, sy))
        return sy + BOLD_H + 2

    def draw_inset(sy, height):
        inset_rect = pygame.Rect(INSET_PAD, sy, w - 2 * INSET_PAD, height)
        draw_sunken(surf, inset_rect, WIN_WHITE)
        return inset_rect

    # ── Time Complexity ───────────────────────────────────────────────────────
    y = draw_section_header("Time Complexity", y)
    inset = draw_inset(y, tc_h)
    label_col_w = 70
    for i, (lbl, val) in enumerate(info["complexity"]):
        ty = inset.y + INSET_PAD + i * LINE_H
        lt = font.render(lbl + ":", False, WIN_TEXT)
        vt = font.render(val, False, WIN_NAVY)
        surf.blit(lt, (inset.x + TEXT_LEFT, ty))
        surf.blit(vt, (inset.x + TEXT_LEFT + label_col_w, ty))
    y += tc_h + SEC_GAP

    # ── Founder / Origin ─────────────────────────────────────────────────────
    y = draw_section_header("Founder / Origin", y)
    inset = draw_inset(y, founder_h)
    for i, line in enumerate(founder_wrapped):
        lt = font.render(line, False, WIN_TEXT)
        surf.blit(lt, (inset.x + TEXT_LEFT, inset.y + INSET_PAD + i * LINE_H))
    y += founder_h + SEC_GAP

    # ── Main Usages ───────────────────────────────────────────────────────────
    y = draw_section_header("Main Usages", y)
    inset = draw_inset(y, usage_h)
    for i, line in enumerate(usage_wrapped):
        lt = font.render(line, False, WIN_TEXT)
        surf.blit(lt, (inset.x + TEXT_LEFT, inset.y + INSET_PAD + i * LINE_H))
    y += usage_h + SEC_GAP

    # ── How It Works ──────────────────────────────────────────────────────────
    y = draw_section_header("How It Works", y)
    inset = draw_inset(y, summary_h)
    for i, line in enumerate(summary_wrapped):
        lt = font.render(line, False, WIN_TEXT)
        surf.blit(lt, (inset.x + TEXT_LEFT, inset.y + INSET_PAD + i * LINE_H))
    y += summary_h + SEC_GAP

    # ── Diagram ───────────────────────────────────────────────────────────────
    y = draw_section_header("Diagram", y)
    inset = draw_inset(y, diag_h)
    diag_rect = pygame.Rect(
        inset.x + INSET_PAD,
        inset.y + INSET_PAD,
        inset.width - 2 * INSET_PAD,
        DIAG_H,
    )
    diagram_key = info.get("diagram", algo_key)
    if diagram_key in _DIAGRAM_FUNCS:
        diag_surf = pygame.Surface((diag_rect.width, diag_rect.height))
        diag_surf.fill(WIN_GRAY)
        _DIAGRAM_FUNCS[diagram_key](diag_surf, pygame.Rect(0, 0, diag_rect.width, diag_rect.height))
        surf.blit(diag_surf, (diag_rect.x, diag_rect.y))
    y += diag_h

    return surf


# ── InfoModal class ───────────────────────────────────────────────────────────

# Alphabetical order matching the dropdown
ALGO_ORDER = [
    "bubble", "cocktail", "comb", "cycle", "gnome",
    "heap", "insertion", "merge", "quick", "radix",
    "selection", "shell", "tim",
]


class InfoModal:
    W       = 640
    TITLE_H = 22
    _NAV_H  = 36   # prev/next nav bar height
    _BTN_H  = 26
    _BTN_AREA = _BTN_H + 20   # close button row: 10px above + button + 10px below

    def __init__(self, btn_font, comp_font):
        self.btn_font  = btn_font
        self.comp_font = comp_font
        self.is_open   = False
        self._algo_key = None
        self._content_surf = None

        # bold font for section headers
        self._bold_font = _font(comp_font.size("A")[1] - 2, bold=True)

        # largest bold font whose rendered height fits in the nav bar with 6px margin each side
        _nav_margin = 6
        _max_text_h = self._NAV_H - 2 * _nav_margin
        _nav_sz = 8
        while True:
            _test = _font(_nav_sz + 1, bold=True)
            if _test.size("A")[1] > _max_text_h:
                break
            _nav_sz += 1
        self._nav_font = _font(_nav_sz, bold=True)

        # compute H: measure content for every algorithm, take the max
        content_w = self.W - 8   # 4px border each side
        max_content_h = 0
        for key in ALGO_INFO:
            s = _build_content_surf(key, self.comp_font, self._bold_font, content_w)
            max_content_h = max(max_content_h, s.get_height())
        self.H = self.TITLE_H + 6 + self._NAV_H + max_content_h + self._BTN_AREA

        mx = (WIN_W - self.W) // 2
        my = max(10, (WIN_H - self.H) // 2)
        self.rect = pygame.Rect(mx, my, self.W, self.H)

        # pre-render title bar gradient
        _gw = self.W - 4
        self._title_grad = pygame.Surface((_gw, self.TITLE_H))
        for i in range(_gw):
            t = i / max(_gw - 1, 1)
            c = (
                int(WIN_NAVY[0] + t * (WIN_NAVY2[0] - WIN_NAVY[0])),
                int(WIN_NAVY[1] + t * (WIN_NAVY2[1] - WIN_NAVY[1])),
                int(WIN_NAVY[2] + t * (WIN_NAVY2[2] - WIN_NAVY[2])),
            )
            pygame.draw.line(self._title_grad, c, (i, 0), (i, self.TITLE_H - 1))

        # dim overlay
        self._overlay = pygame.Surface((WIN_W, WIN_H))
        self._overlay.set_alpha(80)
        self._overlay.fill((0, 0, 0))

        # X button (title bar)
        self._x_btn = pygame.Rect(
            self.rect.right - 4 - 20,
            self.rect.y + 3 + (self.TITLE_H - 16) // 2,
            20, 16,
        )

        # nav bar rect (below title bar)
        _nav_y = self.rect.y + 2 + self.TITLE_H + 2
        self._nav_rect = pygame.Rect(self.rect.x + 4, _nav_y, self.W - 8, self._NAV_H)

        # prev / next buttons inside nav bar
        _nb_w, _nb_h = 80, 24
        _nb_cy = _nav_y + self._NAV_H // 2
        self._prev_btn = pygame.Rect(
            self._nav_rect.x + 8,
            _nb_cy - _nb_h // 2,
            _nb_w, _nb_h,
        )
        self._next_btn = pygame.Rect(
            self._nav_rect.right - 8 - _nb_w,
            _nb_cy - _nb_h // 2,
            _nb_w, _nb_h,
        )

        # content area (below nav bar)
        self._content_rect = pygame.Rect(
            self.rect.x + 4,
            _nav_y + self._NAV_H + 2,
            self.W - 8,
            max_content_h,
        )

        # close button (bottom right, 10px from edges)
        self._close_btn = pygame.Rect(
            self.rect.right - 10 - 80,
            self.rect.bottom - 10 - self._BTN_H,
            80, self._BTN_H,
        )

    # ── lifecycle ─────────────────────────────────────────────────────────────
    def open(self, algo_key):
        self._algo_key = algo_key
        self._content_surf = _build_content_surf(
            algo_key, self.comp_font, self._bold_font, self._content_rect.width
        )
        self.is_open = True

    def close(self):
        self.is_open = False

    # ── draw ──────────────────────────────────────────────────────────────────
    def draw(self, screen, title_font):
        screen.blit(self._overlay, (0, 0))
        draw_raised(screen, self.rect)

        # title bar
        screen.blit(self._title_grad, (self.rect.x + 2, self.rect.y + 2))
        title_txt = title_font.render("Algorithm Info", False, WIN_WHITE)
        screen.blit(title_txt, title_txt.get_rect(
            midleft=(self.rect.x + 10, self.rect.y + 2 + self.TITLE_H // 2)
        ))
        draw_raised(screen, self._x_btn)
        xt = self.btn_font.render("X", False, WIN_TEXT)
        screen.blit(xt, xt.get_rect(center=self._x_btn.center))

        # nav bar
        algo_name = ALGO_INFO.get(self._algo_key, {}).get("name", self._algo_key or "")
        draw_sunken(screen, self._nav_rect)
        draw_raised(screen, self._prev_btn)
        pt = self.btn_font.render("< Prev", False, WIN_TEXT)
        screen.blit(pt, pt.get_rect(center=self._prev_btn.center))
        draw_raised(screen, self._next_btn)
        nt = self.btn_font.render("Next >", False, WIN_TEXT)
        screen.blit(nt, nt.get_rect(center=self._next_btn.center))
        nav_lbl = self._nav_font.render(algo_name, False, WIN_TEXT)
        screen.blit(nav_lbl, nav_lbl.get_rect(center=self._nav_rect.center))

        # content area
        if self._content_surf is not None:
            screen.blit(self._content_surf, self._content_rect.topleft)

        # close button
        draw_raised(screen, self._close_btn)
        ct = self.btn_font.render("Close", False, WIN_TEXT)
        screen.blit(ct, ct.get_rect(center=self._close_btn.center))

    # ── events ────────────────────────────────────────────────────────────────
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self._x_btn.collidepoint(pos) or self._close_btn.collidepoint(pos):
                return "close"
            if self._prev_btn.collidepoint(pos):
                return "prev"
            if self._next_btn.collidepoint(pos):
                return "next"
            if not self.rect.collidepoint(pos):
                return "close"
        return None
