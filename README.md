# python-vis-sort-web

A sorting algorithm visualizer built with Python and Pygame, compiled to WebAssembly via [Pygbag](https://pygame-web.github.io/) and hosted on GitHub Pages.

Styled with a **Windows 95/98 theme** — silver 3D widgets, navy title bar gradient, teal diamond-grid desktop background, and non-antialiased fonts for that authentic pixelated look. The entire UI floats as a raised Win95 window on the teal crosshatch desktop.

> Best viewed on desktop Chrome.

**[Live demo](https://sethrobinson29.github.io/python-vis-sort-web/)**

## Algorithms

| Algorithm | Notes |
|---|---|
| Bubble Sort | Early-exit when already sorted |
| Cocktail Sort | Bidirectional bubble with shrinking window |
| Comb Sort | Gap ÷ 1.3 each pass |
| Cycle Sort | Minimises writes; direct placement |
| Gnome Sort | Single-pointer; steps forward and back |
| Heap Sort | Max-heap; O(n log n) guaranteed |
| Insertion Sort | Shift-based; efficient on nearly-sorted data |
| Merge Sort | Stable divide-and-conquer; O(n log n) |
| Quick Sort | In-place partition with median pivot |
| Radix Sort | LSD non-comparative; O(nk) |
| Selection Sort | Minimal swaps; always O(n²) comparisons |
| Shell Sort | Gap = n÷2, halved each pass |
| Tim Sort | Hybrid insertion+merge (MIN_RUN=32) |

Click the **?** button next to the algorithm dropdown to open an info sheet with time complexities, origin, use cases, a summary, and a diagram for the selected algorithm. Use **< Prev** / **Next >** to browse all algorithms without closing the modal.

## Controls

| Control | Description |
|---|---|
| **Start** | Run the selected algorithm |
| **Stop** | Cancel a running sort |
| **New Array** | Generate a new shuffled array |
| **Descending** | Toggle sort direction |
| **Algorithm** dropdown | Choose which algorithm to run (also resets the array) |
| **Array size** slider | 100 – 500 elements |
| **Volume** slider | Tone volume (0 – 100); adjustable while sorting |
| **M** key | Toggle sound on/off |
| **Palette** buttons | Switch between Default, Phosphor (green CRT), or Custom color palettes |

Controls are disabled and greyed out while a sort is running (except Stop and Volume).

## Custom Palette

Click **Custom...** to open a Win95-style tabbed dialog with 5 save slots. Each slot lets you build a palette of 1–10 colors using RGB sliders. Changes preview live on the array while the dialog is open. Click **OK** to apply and save, or **Cancel** / **×** to discard.

Palettes are saved to `localStorage` in the browser (expire after 30 days) and to `palettes.json` when running natively.

## Running locally

```bash
pip install pygame-ce pygbag

# Desktop
python main.py

# Browser (WASM) — open http://localhost:8000
python -m pygbag --template template.tmpl main.py
```

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

Tests cover all 13 sorting algorithms, widgets (Button, Dropdown), color palettes, and the info modal.

## Credits

Radix and counting sort originally from https://www.geeksforgeeks.org/radix-sort/
