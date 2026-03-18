# Overview — python-vis-sort-web

A sorting algorithm visualizer ported from Tkinter to **Pygame + Pygbag** so it can run in the browser via WebAssembly. Deployed to GitHub Pages automatically on push to `main`.

## What it does
Visualizes 5 sorting algorithms on a bar chart. Each bar's color cycles through a green→pink gradient every 100 values. Controls: sort buttons, a "New Array" button, a "Reverse" button, and a slider (100–500 bars, step 5).

## Algorithms
- Bubble Sort
- Selection Sort
- Merge Sort (recursive)
- Quick Sort (recursive, Lomuto partition)
- Radix Sort (via counting sort by digit)

## File structure
```
main.py          # Pygame entry point — UI, async game loop, Button/Slider classes
sorter.py        # Sorter class — bar drawing, all sort methods (async def)
app.py           # Original Tkinter version (read-only reference, not used)
template.tmpl    # Custom Pygbag HTML loading screen template
requirements.txt # pygame-ce, pygbag
.github/workflows/deploy.yml  # Build + deploy to GitHub Pages on push
.gitignore       # Excludes build/ and __pycache__/
```

## Color palette
| Name    | Hex       | RGB            | Used for              |
|---------|-----------|----------------|-----------------------|
| BG      | `#000034` | (0, 0, 52)     | Sort canvas, body bg  |
| PANEL   | `#2e294e` | (46, 41, 78)   | Buttons, borders      |
| PURPLE  | `#be97c6` | (190, 151, 198)| Text, bar colors      |
| TEAL    | `#297373` | (41, 115, 115) | Window background     |

## Key design points
- All sort methods are `async def`; they `await asyncio.sleep(0)` periodically to yield to the browser event loop
- Draw throttling: `draw_every = max(1, numBars // 100)` — redraws every N comparisons to keep slow sorts (bubble/selection at 500 bars) from being unusably slow
- Sort task management: one `asyncio.Task` at a time in `task_ref = [None]`; new sort cancels the previous one
- `pygame.font.Font(None, size)` used exclusively (no SysFont — unavailable in WASM)
- No `sys.exit()` or `time.sleep()` (Pygbag compatibility)
