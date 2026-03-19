# python-vis-sort-web

A sorting algorithm visualizer built with Python and Pygame, compiled to WebAssembly via [Pygbag](https://pygame-web.github.io/) and hosted on GitHub Pages.

Styled with a **Windows 95/98 theme** — silver 3D widgets, navy title bar gradient, teal diamond-grid desktop background, and non-antialiased fonts for that authentic pixelated look.

> Best viewed on desktop Chrome.

**[Live demo](https://sethrobinson29.github.io/python-vis-sort-web/)**

## Algorithms

- Bubble Sort
- Selection Sort
- Merge Sort
- Quick Sort
- Radix Sort

## Controls

| Control | Description |
|---|---|
| **Start** | Run the selected algorithm |
| **Stop** | Cancel a running sort |
| **New Array** | Generate a new shuffled array |
| **Descending** | Toggle sort direction |
| **Algorithm** dropdown | Choose which algorithm to run |
| **Array size** slider | 100 – 500 elements |
| **Volume** slider | Tone volume (0 – 100) |
| **M** key | Toggle sound on/off |

## Running locally

```bash
pip install pygame-ce pygbag

# Desktop
python main.py

# Browser (WASM) — open http://localhost:8000
python -m pygbag --template template.tmpl main.py
```

## Credits

Radix and counting sort originally from https://www.geeksforgeeks.org/radix-sort/
