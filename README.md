# Boids Flocking Behaviour (Numerical Methods Project)

## Overview
This project simulates biological flocking behaviour using the Boids model. It demonstrates how simple local rules can produce emergent group motion over time.

## Model (Boids Rules)
Each boid has:
- Position: (x, y)
- Velocity: (vx, vy)

At each time-step, each boid looks at nearby neighbours and computes steering forces:
- Separation: steer away if too close (avoid collisions).
- Alignment: steer toward neighbours’ average heading.
- Cohesion: steer toward neighbours’ average position (flock center).

Key parameters used in the simulation (see `main.py`):
- VISION_RADIUS
- SEPARATION_RADIUS
- W_COH, W_ALI, W_SEP
- MAX_SPEED, MAX_FORCE

## Numerical Method
The simulation is advanced in discrete time using Euler integration:
- v = v + a * dt
- x = x + v * dt

Where `dt` is the time step per frame (seconds), controlled by the PyGame clock.

## Visualisation / Controls
The simulation renders boids in real-time using PyGame.
Controls:
- R: Reset simulation
- (Add any others you implemented, e.g., D: toggle debug circles)

## Setup
### Requirements
- Python 3.10+ recommended
- Dependencies in `requirements.txt`

### Install
Create and activate a virtual environment, then install dependencies:

Windows (PowerShell):
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

### Install (Git Bash on Windows)
```bash
# From the repo root
py -m venv .venv

# Activate the venv (Git Bash)
source .venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt

