# Desktop Pet

A small desktop companion that lives on top of your screen while you
work — registers an account, lets you pick one of three Arknights-themed
characters (Beeswax / Lappland / Magallan), and gives them animations,
drag-and-drop, chat, and a screen-capture button.

Built for fun, in Python + PyQt5. Kept public as a portfolio entry
because the same project taught me Qt event handling, frameless
windows, and Windows-API quirks I keep coming back to.

<p align="center">
  <img src="Deskpet_Beeswax/deskpet/right/idle/0.png"  width="180" alt="Beeswax">
  <img src="Deskpet_Lappland/deskpet/right/idle/0.png" width="180" alt="Lappland">
  <img src="Deskpet_Magallan/magallan/right/idle/0.png" width="180" alt="Magallan">
</p>
<p align="center">
  <i>Three Arknights-themed companions — Beeswax · Lappland · Magallan.
  Each renders as a transparent, always-on-top, frameless window so the
  character appears to live directly on your desktop. Every character
  has a full set of <code>idle / move / sit / sleep / poke / drop / skill / attack</code>
  animation states in both left- and right-facing variants.</i>
</p>

## Stack

Python 3 · PyQt5 · pywin32 (for the always-on-top / transparency
window flags). Windows only.

## Run

```bash
pip install -r requirements.txt
python main.py
```

A login window opens — register an account first, then pick a pet
from the storage screen.

## Project structure

```
.
├── main.py              # Login / register / storage / exit windows
├── log.py               # Login UI (generated from Qt Designer)
├── regi.py              # Register UI
├── stor.py              # Pet-storage selection UI
├── ex.py                # Exit-confirmation UI
├── Deskpet_Beeswax/     # Pet character 1 — Beeswax
├── Deskpet_Lappland/    # Pet character 2 — Lappland
├── Deskpet_Magallan/    # Pet character 3 — Magallan
└── images/              # Shared UI assets
```

Each `Deskpet_*` folder contains its own animation frames and a
character-specific `MainWindows` class that exposes the pet on screen.
