# Architectural & Implementation Decisions

## Pygame-CE + Pygbag over alternatives
Tkinter cannot run in a browser. Pygame + Pygbag compiles to WASM and is the only path that keeps the project in Python. Alternatives considered: Pyodide alone (no Pygame), Brython (different paradigm), rewrite in JS (not the goal).

## Separate repo (`python-vis-sort-web`)
The original Tkinter repo (`python-vis-sort`) is kept untouched as a reference. `app.py` is copied into the web repo as read-only reference — not imported or run.

## `async def` for all sort methods
Pygbag requires the main loop to be async. Sort methods must yield (`await asyncio.sleep(0)`) after each draw call so the browser event loop can process frames. Without this, the browser tab freezes for the duration of the sort.

## Draw throttling (`draw_every = numBars // 100`)
Bubble and selection sort at 500 bars = ~125k comparisons. Drawing every comparison would be extremely slow. Throttling to ~100 redraws keeps animation smooth and responsive without sacrificing the visual effect. Value chosen empirically.

## Single task ref + cancellation pattern
```python
task_ref = [None]
# on new sort:
await cancel_task(task_ref)
task_ref[0] = asyncio.create_task(sorter.bubbleSort())
```
A list is used (not a plain variable) so `cancel_task` can mutate it. Cancelling awaits the task to ensure clean shutdown before starting the next sort.

## `pygame.Surface` passed into `Sorter`
Sorter draws onto a passed-in surface rather than creating its own. This lets `main.py` blit the sort surface at a specific position on the screen, keeping drawing and layout logic separate.

## `pygame.font.Font(None, size)` only
`SysFont` is unavailable in WASM (no system fonts in the browser sandbox). `Font(None, size)` uses pygame's built-in font which is always available.

## Pygbag custom template (`template.tmpl`)
The default pygbag template has a grey/white loading screen. A local `template.tmpl` is passed via `--template` to both the local pygbag command and the CI build. Changes from the default:
- Body background matches app color scheme (`#000034`)
- `#infobox` styled as a centered card with the app title
- UME (User Media Engagement) waiting block removed — app starts automatically (safe because there's no audio)
- `ui_callback` uses `innerHTML` to keep title visible while showing install status
- `platform.document.body.style.background` changed from `#7f7f7f` to `#000034`

## proxMapSort removed
The original `sorter.py` had `proxMapSort`, `calculateHash`, and `mapInsertionSort` as unfinished stubs with broken code (indexing into empty lists). These were dropped in the port.

## GitHub Actions deploy
Pages source set to "GitHub Actions" in repo settings. The workflow installs `pygame-ce` and `pygbag`, builds with `python -m pygbag --build --template template.tmpl main.py`, then uploads `build/web` as the Pages artifact.
