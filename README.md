# Képernyő életben tartó

Egyszerű Python script, ami megakadályozza a képernyővédő bekapcsolását azáltal, hogy percenként 1 pixelt mozgatja az egeret oda-vissza. Hasznos távoli asztali kapcsolatoknál, ahol kevés az interakció.

## Követelmények

- Windows
- Python 3.x (telepítés nélkül fut, csak beépített Windows API-t használ)

## Indítás

```bash
python kepernyo_eletben.py
```

## Leállítás

`Ctrl+C` a konzolablakban, vagy zárd be az ablakot.

## Beállítások

A fájl tetején két sor hangolható:

```python
INTERVAL_SEC = 60   # Hány másodpercenként mozduljon az egér
PIXEL_DELTA  = 1    # Hány pixelt mozdítson (oda, majd vissza)
```
