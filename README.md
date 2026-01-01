# Rumor Mill Model

## Overview
An agent-based model simulating how a rumor spreads through a population based on spatial proximity. Individuals who know the rumor share it with their neighbors, and the simulation tracks both the spread and redundant transmissions.

## How It Works

The model places people on a 2D grid where each cell contains one person. At each time step:
1. Every person who knows the rumor randomly selects one neighbor
2. They tell that neighbor the rumor
3. The model tracks how many times each person has heard the rumor

## Model Parameters

- **know_rumor_ratio**: Initial percentage of agents who know the rumor (0.0 - 1.0)
- **eight_neightborhood**: Whether to use Moore (8-neighbor) or Von Neumann (4-neighbor) grid
- **width**: Grid width (default: 10)
- **height**: Grid height (default: 10)

## Neighborhood Types

**Moore Neighborhood** (8 neighbors):
```
[X][X][X]
[X][ ][X]
[X][X][X]
```
- Faster spread
- Diagonal transmission
- Reaches saturation quicker

**Von Neumann Neighborhood** (4 neighbors):
```
   [X]
[X][ ][X]
   [X]
```
- Diamond-shaped spread pattern
- Slower diffusion
- More directional spread

## Metrics Tracked

- **Percentage Knowing Rumor**: Percentage of population that knows the rumor
- **Times Heard Rumor**: Average number of times each person has heard the rumor
- **Ratio Knowing Rumor**: Ratio of population that knows the rumor (0.0 - 1.0)

## Expected Behavior

**Early Stage**: Linear growth radiating from initial spreaders, few repeated tellings

**Middle Stage**: Accelerating spread as more people know the rumor, increasing redundancy

**Late Stage**: Slowing growth as most people already know, high repeated tellings

## Running the Model

### Installation
```bash
pip install mesa
```

### Run
```bash
solara run app.py
```

### Access
Open browser to: `http://localhost:8765`

## Visualization

- **Red agents**: Know the rumor
- **Blue agents**: Don't know the rumor
- **Charts**: Track spread metrics over time

## References

Adapted from NetLogo Rumor Mill model:
https://www.netlogoweb.org/launch#https://www.netlogoweb.org/assets/modelslib/Sample%20Models/Social%20Science/Rumor%20Mill.nlogox
