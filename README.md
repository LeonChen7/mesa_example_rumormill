# Rumor Mill Model

A simple agent-based simulation showing how rumors spread through a population, implemented with the Mesa framework.

## About

This is an introductory Mesa example that demonstrates:
- Creating agents with simple behaviors
- Using grid-based space (Von Neumann and Moore neighborhoods)
- Collecting and visualizing data
- Building an interactive web interface with SolaraViz

The model is adapted from the NetLogo Rumor Mill model by Uri Wilensky (1999).

## How It Works

Agents are placed on a grid. Some agents start knowing a rumor (red), others don't (blue). Each step:
- Agents who know the rumor tell one random neighbor
- The rumor spreads with a configurable probability
- The simulation tracks how the rumor propagates through the population

## Installation

```bash
pip install mesa
```

## Running the Model

Launch the interactive visualization:

```bash
solara run app.py
```

or

```bash
mesa runserver app.py
```

This opens a web interface where you can:
- Adjust parameters with sliders
- Watch the rumor spread in real-time
- View plots of spread metrics

## Parameters

- **know_rumor_ratio** (0.0-1.0): Initial percentage of agents who know the rumor
- **rumor_spread_chance** (0.0-1.0): Probability of successful rumor transmission
- **eight_neighborhood** (True/False): Use 8 neighbors (Moore) vs 4 neighbors (Von Neumann)
- **width/height**: Grid dimensions

## Code Structure

**agent.py** - Defines the Person agent
- `knows_rumor`: Whether agent knows the rumor
- `times_heard`: How many times agent heard it
- `step()`: Tell a random neighbor if you know the rumor

**model.py** - Defines the RumorMillModel
- Creates grid and agents
- Runs the simulation steps
- Collects data (percentage knowing rumor, average times heard, percentage of new people hearing the rumor)

**app.py** - Visualization interface
- Grid display with color-coded agents
- Interactive parameter controls
- Real-time charts

## Running Programmatically

```python
from model import RumorMillModel

model = RumorMillModel(
    width=10,
    height=10,
    know_rumor_ratio=0.3,
    rumor_spread_chance=0.5,
    eight_neightborhood=False
)

for i in range(100):
    model.step()

data = model.datacollector.get_model_vars_dataframe()
print(data)
```

## Credits

- Original NetLogo model: Uri Wilensky (1999), Northwestern University
- Mesa framework: https://github.com/projectmesa/mesa
