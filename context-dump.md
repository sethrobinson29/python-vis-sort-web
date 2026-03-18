# Context Dump

## Files changed this session
| File | Status | Notes |
|------|--------|-------|
| `main.py` | Created | Full Pygame UI — Button, Slider, async game loop, sort task management |
| `sorter.py` | Created | Pygame port of original — async sorts, draw throttling, removed broken proxMapSort stubs |
| `template.tmpl` | Created | Custom Pygbag loading screen — dark theme, styled infobox, UME block removed |
| `requirements.txt` | Created | `pygame-ce`, `pygbag` |
| `.github/workflows/deploy.yml` | Created | GitHub Pages deploy via Actions |
| `.gitignore` | Created | Excludes `build/`, `__pycache__/` |
| `README.md` | Modified | Updated for Pygame/web, local run instructions, live demo link |
| `app.py` | Copied | Original Tkinter version, read-only reference |

## Key functions

### `main.py`
- `Button.draw(surf)` / `Button.is_clicked(pos)` — simple rect button
- `Slider.handle_event(event)` / `Slider._update_value(mouse_x)` — drag slider, snaps to step 5
- `cancel_task(task_ref)` — cancels running sort task, awaits CancelledError
- `draw_ui(screen, sorter, sort_surf, buttons, slider, ...)` — full frame render
- `async def main()` — pygame init, event loop, `asyncio.run(main())`

### `sorter.py`
- `Sorter.__init__(surface, width, height)` — accepts a `pygame.Surface`
- `Sorter.drawNums()` — fills surface `(0,0,52)`, draws bars with color from gradient list
- `Sorter.makeNewVals(length)` — shuffled range, resets comps
- All sorts: `async def bubbleSort/selectionSort/mergeSortWrap/quickSortWrap/radixSort`
- `merge()` is sync (no draw calls, no recursion)
- `partition()` is async (has draw calls)

## Assumptions made
- `comps` counter is not live-updated in the UI during a sort — it reflects the count at the last `drawNums()` call, which is sufficient for the current UI (label reads `sorter.comps` each frame)
- Slider regenerates array on `MOUSEBUTTONUP` after drag, not on every mouse move (avoids spamming makeNewVals)
- `pygame` 2.4.0 is installed locally; `pygame-ce` is in requirements and used in CI — compatible, `pygame-ce` replaces `pygame` if installed

## Pygbag version
0.9.3 — template cached at `build/web-cache/27613e24ba16d44f2a5c88150c6d64e5.tmpl`, used as the base for `template.tmpl`
