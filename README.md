# Book of Tench

Terminal-based roguelite RPG built in Python.

## Core Systems

- Turn-based combat
- Deep and diverse economy  
- Event-driven reactions using a listener pattern  
- State-driven player and enemy domain models  
- Modular component → service → model layering  
- Persistence (save/load) system  
- Audio integration and curses-based terminal UI  

Gameplay flow, state mutation, and side-effects are separated to maintain architectural control as the project grows.

## Architectural Structure (High Level)

```text
bookoftench/
│
├── component/      # Flow owners coordinating phases
├── service/        # Logic layers mutating state
├── model/          # Core domain/state objects
├── data/           # Static definitions
│
├── listeners.py    # Event-driven reactions
├── persistence.py  # Save/load handling
├── audio.py        # Sound system
├── curses_util.py  # Terminal UI helpers
└── main.py         # Entry point
```

## Architectural Intent

The project emphasizes:

- Explicit ownership boundaries
- Flow vs mutation vs reaction separation
- Event-driven extensibility
- Long-term maintainability over short-term convenience

## Run

```bash
python3 main.py
```

No external services required.
