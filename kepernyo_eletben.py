"""
Képernyő életben tartó — v2
Két mechanizmus egyszerre:
  1. SetThreadExecutionState — jelzi a Windowsnak, ne kapcsolja le a kijelzőt
  2. SendInput — valódi egér input eseményt generál (screensaver reseteléshez)
Indítás: python kepernyo_eletben.py
Leállítás: Ctrl+C vagy zárd be az ablakot
"""

import sys
import time
import ctypes
import ctypes.wintypes

# --- Beállítások ---
INTERVAL_SEC = 60       # Hány másodpercenként aktiválódjon
PIXEL_DELTA  = 1        # Mennyi pixelt mozdítson (oda, majd vissza)
# -------------------

# Windows konstansok
ES_CONTINUOUS        = 0x80000000
ES_SYSTEM_REQUIRED   = 0x00000001
ES_DISPLAY_REQUIRED  = 0x00000002
INPUT_MOUSE          = 0
MOUSEEVENTF_MOVE     = 0x0001

# SendInput struktúrák
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx",          ctypes.c_long),
        ("dy",          ctypes.c_long),
        ("mouseData",   ctypes.c_ulong),
        ("dwFlags",     ctypes.c_ulong),
        ("time",        ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT)]
    _anonymous_ = ("_input",)
    _fields_ = [("type", ctypes.c_ulong), ("_input", _INPUT)]


def keep_display_on():
    """Jelzi a Windowsnak, hogy tartsa ébren a kijelzőt."""
    ctypes.windll.kernel32.SetThreadExecutionState(
        ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
    )

def send_mouse_move(dx, dy):
    """Valódi egér input eseményt generál."""
    inp = INPUT(type=INPUT_MOUSE,
                _INPUT=INPUT._INPUT(mi=MOUSEINPUT(
                    dx=dx, dy=dy,
                    mouseData=0,
                    dwFlags=MOUSEEVENTF_MOVE,
                    time=0,
                    dwExtraInfo=None
                )))
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

def jiggle():
    send_mouse_move(PIXEL_DELTA, 0)
    time.sleep(0.05)
    send_mouse_move(-PIXEL_DELTA, 0)

def restore_on_exit():
    """Kilépéskor visszaállítja a normál alvási viselkedést."""
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)

def main():
    keep_display_on()
    print("=" * 45)
    print("  Képernyő életben tartó v2 — AKTÍV")
    print(f"  Intervallum : {INTERVAL_SEC} mp")
    print(f"  Mozgás      : ±{PIXEL_DELTA} pixel (SendInput)")
    print("  Kijelző alvás: letiltva (SetThreadExecutionState)")
    print("  Leállítás   : Ctrl+C")
    print("=" * 45)

    tick = 0
    try:
        while True:
            jiggle()
            tick += 1
            ts = time.strftime("%H:%M:%S")
            print(f"[{ts}] Jiggle #{tick}")
            time.sleep(INTERVAL_SEC)
    except KeyboardInterrupt:
        restore_on_exit()
        print("\nLeállítva — kijelző alvás visszaállítva.")
        sys.exit(0)

if __name__ == "__main__":
    main()
