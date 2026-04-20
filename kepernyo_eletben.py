"""
Képernyő életben tartó — egér jiggler
Minden 60 másodpercben 1 pixelt mozgatja az egeret oda-vissza.
Indítás: python kepernyo_eletben.py
Leállítás: Ctrl+C vagy zárd be az ablakot
"""

import sys
import time
import ctypes
import ctypes.wintypes

# --- Beállítások ---
INTERVAL_SEC = 60       # Hány másodpercenként mozduljon az egér
PIXEL_DELTA  = 1        # Mennyi pixelt mozdítson (oda, majd vissza)
# -------------------

def get_cursor_pos():
    pt = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def move_cursor(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)

def jiggle():
    x, y = get_cursor_pos()
    move_cursor(x + PIXEL_DELTA, y)
    time.sleep(0.05)
    move_cursor(x, y)

def main():
    print("=" * 45)
    print("  Képernyő életben tartó — AKTÍV")
    print(f"  Intervallum : {INTERVAL_SEC} mp")
    print(f"  Mozgás      : ±{PIXEL_DELTA} pixel")
    print("  Leállítás   : Ctrl+C")
    print("=" * 45)

    tick = 0
    try:
        while True:
            jiggle()
            tick += 1
            ts = time.strftime("%H:%M:%S")
            print(f"[{ts}] Jiggle #{tick} — egér pozíció megtartva")
            time.sleep(INTERVAL_SEC)
    except KeyboardInterrupt:
        print("\nLeállítva.")
        sys.exit(0)

if __name__ == "__main__":
    main()
