"""Headless smoke test for cargame.py (SDL dummy drivers).

Drives: menu -> play -> accelerate/steer until crash -> B (back to menu)
        -> garage (Money screen) -> back -> QUIT. Exits 0 on success.
"""
import os, sys, threading, time, traceback

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame  # noqa: E402

t0 = time.time()
def log(msg):
    print(f"[{time.time()-t0:6.2f}s] {msg}", flush=True)

failures = []
music_loaded = []
music_played = []

_orig_load = pygame.mixer.music.load
def _spy_load(path, *a, **k):
    music_loaded.append(str(path))
    log(f"  [music.load] {path}")
    return _orig_load(path, *a, **k)
pygame.mixer.music.load = _spy_load

_orig_play = pygame.mixer.music.play
def _spy_play(*a, **k):
    music_played.append(1)
    return _orig_play(*a, **k)
pygame.mixer.music.play = _spy_play

# Dummy video driver keeps SDL mouse state at (0,0); the game hit-tests
# buttons via pygame.mouse.get_pos(), so provide a controllable fake.
_fake_mouse = [0, 0]
_last_seen = None
def _fake_get_pos():
    global _last_seen
    p = tuple(_fake_mouse)
    if p != _last_seen:
        log(f"  [get_pos -> {p}]")
        _last_seen = p
    return p
pygame.mouse.get_pos = _fake_get_pos

# diagnostic: log which events the game loop actually consumes
_orig_event_get = pygame.event.get
def _spy_event_get(*a, **k):
    evs = _orig_event_get(*a, **k)
    for e in evs:
        if e.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.QUIT):
            extra = f" key={e.key}" if hasattr(e, "key") else ""
            extra += f" pos={getattr(e, 'pos', None)} btn={getattr(e, 'button', None)}"
            log(f"  [event consumed] {pygame.event.event_name(e.type)}{extra}")
    return evs
pygame.event.get = _spy_event_get

death_info = {}
def game_thread():
    try:
        import cargame  # runs intro() loop and blocks here
        log("GAME THREAD ENDED NORMALLY (unexpected)")
    except BaseException as ex:
        death_info["exc"] = ex
        death_info["tb"] = traceback.format_exc()
        log(f"GAME THREAD DIED: {type(ex).__name__}: {ex}")

th = threading.Thread(target=game_thread, daemon=True)
msgs = []
def wait_until(pred, timeout, what):
    end = time.time() + timeout
    while time.time() < end:
        if pred():
            log(f"OK: {what}")
            return True
        if not th.is_alive() and "exc" in death_info:
            failures.append(f"{what}: game thread died early:\n{death_info['tb']}")
            return False
        time.sleep(0.05)
    failures.append(f"TIMEOUT waiting for: {what}")
    return False

def _find_diff_pixel(img_a, img_b):
    wa, ha = img_a.get_size(); wb, hb = img_b.get_size()
    w, h = min(wa, wb), min(ha, hb)
    for y in range(0, h, 5):
        for x in range(0, w, 5):
            if img_a.get_at((x, y)) != img_b.get_at((x, y)):
                return (x, y)
    return (w // 2, h // 2)

# pixel probes to deterministically tell which screen is up
# (images loaded lazily: pygame.image.load needs video initialized)
_screen_imgs = {}
def screen_state():
    if "menu" not in _screen_imgs:
        base = os.path.dirname(os.path.abspath(__file__))
        m, g = None, None
        try:
            m = pygame.image.load(os.path.join(base, "menu.png"))
            g = pygame.image.load(os.path.join(base, "garage.png"))
        except Exception:
            pass
        px_coord = (5, 5)
        if m is not None and g is not None:
            px_coord = _find_diff_pixel(m, g)
        _screen_imgs.update(menu=m, garage=g, coord=px_coord)
    try:
        px = cg.gameDisplay.get_at(_screen_imgs["coord"])
    except Exception:
        return "other"
    if _screen_imgs["menu"] is not None and px == _screen_imgs["menu"].get_at(_screen_imgs["coord"]):
        return "menu"
    if _screen_imgs["garage"] is not None and px == _screen_imgs["garage"].get_at(_screen_imgs["coord"]):
        return "store"
    return "other"

th.start()
time.sleep(1.5)

cg = sys.modules["cargame"]
_orig_msg = cg.message
def _spy_msg(text, *a, **k):
    msgs.append(str(text))
    return _orig_msg(text, *a, **k)
cg.message = _spy_msg

log(f"alive after start: {th.is_alive()}")
crash_calls = []
_orig_crash = cg.crash
def _spy_crash(*a, **k):
    crash_calls.append(1)
    return _orig_crash(*a, **k)
cg.crash = _spy_crash

def click(x, y, label):
    _fake_mouse[0], _fake_mouse[1] = x, y
    time.sleep(0.05)  # cross a frame boundary: loop hit-tests pos before draining events each frame
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(x, y)))
    log(f"CLICK {label} at ({x},{y}) (alive={th.is_alive()})")

def key(k, label):
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=k))
    log(f"KEY {label} (alive={th.is_alive()})")

# 1) menu is up -> click PLAY; expect game loop to start loading run.mp3
click(396, 444, "PLAY")
wait_until(lambda: any("run.mp3" in m for m in music_loaded), 5, "game loop started (run.mp3)")

# 2) drive until crash -> cc.mp3 loaded on crash screen
key(pygame.K_UP, "UP (accelerate)")
time.sleep(1.0)
key(pygame.K_RIGHT, "RIGHT (steer to wall)")
wait_until(lambda: any("cc.mp3" in m for m in music_loaded), 8, "crash screen reached (cc.mp3)")
# wait out the 1s "You Crashed" pause until the interactive game-over loop is draining events
wait_until(lambda: any(m.startswith("B to play again") for m in msgs), 8, "game-over screen interactive")

# 3) B -> back to menu; verify deterministically via pixel probe
key(pygame.K_b, "B (back to menu)")
wait_until(lambda: screen_state() == "menu", 6, "back at main menu after B")

# 4) garage: exercises the old long() crash + Money message
click(397, 526, "GARAGE")
ok1 = wait_until(lambda: any(m.startswith("Money:") for m in msgs), 5, "garage 'Money:' shown (store loop)")
if ok1:
    wait_until(lambda: screen_state() == "store", 3, "pixel probe confirms store screen")

# 5) back to menu (verified), then quit cleanly via window-close event
click(80, 64, "BACK")
wait_until(lambda: screen_state() == "menu", 5, "back at main menu after BACK")
pygame.event.post(pygame.event.Event(pygame.QUIT))
end = time.time() + 6
while th.is_alive() and time.time() < end:
    time.sleep(0.1)

log(f"final alive={th.is_alive()}")
if th.is_alive():
    failures.append("game thread still running after QUIT event (did not exit cleanly)")
elif "exc" in death_info and not isinstance(death_info["exc"], SystemExit):
    failures.append("unexpected exception:\n" + death_info["tb"])

print(f"\ncrash() calls (game loop frames): {len(crash_calls)}")
print(f"music loaded: {music_loaded}")
print(f"sample messages: {msgs[:3]} ... total {len(msgs)}")
if failures:
    for f in failures:
        print("FAIL:", f, flush=True)
print("RESULT:", "FAIL" if failures else "PASS")
sys.exit(1 if failures else 0)
