# Book of Tench

A terminal-based roguelite RPG with sound, written in Python.

---

## About This Repo

This project acts as a structured game sandbox focused on gameplay systems, architecture, and modular design.
It is an ongoing collaboration between brothers Brodie and Brock Sennish.

The focus is on **design, structure, and iteration** more than completing a finished product.

---

## What’s Inside

Book of Tench includes a working terminal-based roguelite loop built around modular systems, including:

* Turn-based combat flow
* Enemy spawning and encounters
* Event-driven reactions and listeners
* State-driven player and enemy models
* Persistence, audio, and curses-based UI utilities

Systems are separated so gameplay flow, data, and side-effects remain easy to follow.

---

## Project Structure (High Level)

```
bookoftench/
│
├── component/      # Flow owners that route game phases and coordinate systems
├── data/           # Static definitions (enemies, items, configuration data)
├── model/          # Core state objects and domain models
├── service/        # Logic layers that perform actions or mutate state
│
├── audio.py        # Sound handling
├── curses_util.py  # Terminal UI helpers
├── event_base.py   # Event definitions
├── event_logger.py # Event logging utilities
├── game.py         # Core game orchestration
├── globals.py      # Shared constants/state references
├── listeners.py    # Event listeners and reactions
├── persistence.py  # Save/load logic
├── settings.py     # Configuration values
├── ui.py           # Display/UI helpers
└── util.py         # General utilities

main.py             # Application entry point
```

---

## Run

```bash
python3 main.py
```

No external services or setup required.
