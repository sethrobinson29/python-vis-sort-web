# python-vis-sort-web

A sorting algorithm visualizer built with Python and Pygame, compiled to WebAssembly via [Pygbag](https://pygame-web.github.io/) and hosted on GitHub Pages.

> Best viewed on desktop Chrome.

**[Live demo](https://sethrobinson29.github.io/python-vis-sort-web/)**

## Algorithms

- Bubble Sort
- Selection Sort
- Merge Sort
- Quick Sort
- Radix Sort

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
