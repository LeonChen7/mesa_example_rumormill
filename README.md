# Rumor Mill Model - Mesa Implementation

## Overview
This project implements an agent-based model (ABM) of rumor spreading using the Mesa framework. The model simulates how information (a rumor) propagates through a population based on spatial proximity, where individuals share the rumor with their neighbors over time.

## Model Description

### Concept
The rumor spreads through a grid-based population where each cell contains one person. At each time step, every person who knows the rumor randomly selects one of their neighbors and tells them the rumor. The simulation tracks both the spread of information and redundant transmissions (repeated tellings).

### Key Mechanisms
1. **Spatial Structure**: Agents are placed on a 2D grid representing spatial proximity
2. **Rumor Transmission**: Agents who know the rumor tell one random neighbor per step
3. **Repeated Tellings**: The model tracks when someone hears the rumor multiple times
4. **Neighborhood Types**: Configurable neighbor definitions (4-adjacent or 8-adjacent)

## Implementation Architecture

### File Structure
```
mesa_example_rumormill/
├── agent.py          # Person agent class
├── model.py          # RumorModel class
├── app.py            # Solara visualization interface
└── README.md         # This file
```

### Component Design

#### 1. Agent Class (`agent.py`)

**Class**: `Person`

**Attributes**:
- `unique_id`: Agent identifier
- `model`: Reference to the model
- `knows_rumor`: Boolean indicating if agent knows the rumor
- `times_heard`: Integer counting how many times agent has heard the rumor
- `pos`: Grid position (x, y)

**Methods**:
- `__init__()`: Initialize agent with default state (doesn't know rumor)
- `step()`: Execute one time step of behavior
  - If knows rumor:
    1. Get neighbors based on model's neighborhood type
    2. If neighbors exist, randomly select one
    3. Tell that neighbor the rumor
    4. Update neighbor's state and times_heard counter

**Logic Flow**:
```python
if self.knows_rumor:
    neighbors = get_neighbors()
    if neighbors:
        target = random.choice(neighbors)
        if target.knows_rumor:
            # Repeated telling - increment counter
        else:
            # New transmission - set knows_rumor = True
        target.times_heard += 1
```

#### 2. Model Class (`model.py`)

**Class**: `RumorModel`

**Parameters**:
- `width`: Grid width (default: 10)
- `height`: Grid height (default: 10)
- `initial_rumor_spreaders`: Number of agents who start knowing the rumor (default: 1)
- `moore_neighborhood`: Boolean - True for 8-neighbors, False for 4-neighbors (default: True)

**Components**:
- `grid`: `SingleGrid` - Ensures one agent per cell
- `schedule`: `RandomActivation` - Agents act in random order each step
- `datacollector`: `DataCollector` - Tracks metrics over time

**Initialization Process**:
1. Create grid and schedule
2. Create agents (width × height total)
3. Place agents on grid (one per cell)
4. Randomly select `initial_rumor_spreaders` agents
5. Set selected agents' `knows_rumor = True` and `times_heard = 1`
6. Set up data collection

**Data Collection Metrics**:

*Model-level reporters*:
- `Knows_Rumor`: Count of agents where `knows_rumor == True`
- `Total_Heard`: Sum of all `times_heard` across agents
- `Repeated_Tellings`: `Total_Heard - Knows_Rumor` (tellings to people who already knew)
- `Percent_Informed`: `(Knows_Rumor / total_agents) * 100`

*Agent-level reporters*:
- `knows_rumor`: Individual agent state
- `times_heard`: Individual agent counter

**Step Method**:
```python
def step():
    self.schedule.step()  # All agents execute their step()
    self.datacollector.collect(self)  # Record metrics
```

#### 3. Visualization (`app.py`)

**Framework**: Mesa's Solara-based visualization

**Grid Visualization**:
- **Portrayal Function**: `person_portrayal(agent)`
  - If `knows_rumor == True`: Red circle
  - If `knows_rumor == False`: Gray circle
  - Size: Proportional to grid size
  - Optional: Display `times_heard` as text overlay

**Components**:
- `SpaceDrawer`: Renders the 2D grid with agent portrayals
- `PlotMatplotlib`: Line charts showing spread over time
  - Chart 1: Number of people who know rumor vs. time
  - Chart 2: Repeated tellings vs. time
  - Chart 3: Percentage informed vs. time

**Model Parameters UI**:
```python
model_params = {
    "width": {
        "type": "SliderInt",
        "value": 10,
        "min": 5,
        "max": 50,
        "step": 1
    },
    "height": {
        "type": "SliderInt",
        "value": 10,
        "min": 5,
        "max": 50,
        "step": 1
    },
    "initial_rumor_spreaders": {
        "type": "SliderInt",
        "value": 1,
        "min": 1,
        "max": 10,
        "step": 1
    },
    "moore_neighborhood": {
        "type": "Checkbox",
        "value": True,
        "label": "Moore Neighborhood (8 neighbors)"
    }
}
```

**Page Layout**:
```python
SolaraViz(
    model_class=RumorModel,
    model_params=model_params,
    components=[grid_display, charts],
    name="Rumor Mill Model"
)
```

## Implementation Details

### Neighborhood Definition

**Moore Neighborhood** (`moore=True`):
```
[ ][ ][ ]
[ ][X][ ]  → X has 8 neighbors
[ ][ ][ ]
```

**Von Neumann Neighborhood** (`moore=False`):
```
   [ ]
[ ][X][ ]  → X has 4 neighbors
   [ ]
```

Implementation uses Mesa's `grid.get_neighbors()`:
```python
neighbors = self.model.grid.get_neighbors(
    self.pos,
    moore=self.model.moore_neighborhood,
    include_center=False
)
```

### Edge Handling
The grid is non-toroidal by default (edges are boundaries):
```python
grid = SingleGrid(width, height, torus=False)
```

Corner agents have fewer neighbors (2 for Von Neumann, 3 for Moore).

### Random Selection
Uses Python's `random.choice()` for:
- Initial rumor spreaders: `random.sample(agents, k=initial_rumor_spreaders)`
- Target neighbor selection: `random.choice(neighbors)`

### Activation Order
`RandomActivation` scheduler ensures:
- Each agent acts once per step
- Order is randomized each step
- Prevents systematic biases from fixed ordering

## Expected Behavior

### Spread Patterns

**With Moore Neighborhood (8 neighbors)**:
- Faster radial spread
- More diagonal transmission
- Higher repeated telling rate
- Reaches saturation quicker

**With Von Neumann Neighborhood (4 neighbors)**:
- Diamond-shaped spread pattern
- Slower overall diffusion
- Lower repeated telling rate
- More directional spread

### Metrics Evolution

**Early Stage** (first few steps):
- Linear growth in informed population
- Low repeated tellings
- Spread radiates from initial spreader(s)

**Middle Stage**:
- Accelerating growth as more spreaders exist
- Increasing repeated tellings at infection front
- Patches of informed vs. uninformed agents

**Late Stage** (approaching saturation):
- Slowing growth as fewer uninformed remain
- Rapidly increasing repeated tellings
- Eventually 100% informed, all tellings are repeats

### Saturation Time
Expected to reach full saturation in approximately:
- Moore: `~(max_distance_from_spreader)` steps
- Von Neumann: `~(manhattan_distance)` steps

Where distance is measured from initial spreader(s).

## Running the Model

### Installation
```bash
pip install mesa
```

### Execution
```bash
# Run visualization server
solara run app.py

# Or using Mesa command
mesa runserver
```

### Access
Open browser to: `http://localhost:8765`

## Experiments to Try

### 1. Initial Spreaders
Compare 1 vs. multiple initial spreaders:
- How does saturation time change?
- Do multiple spreaders in corners vs. center differ?

### 2. Neighborhood Type
Moore vs. Von Neumann:
- Speed of spread
- Pattern of diffusion
- Repeated tellings ratio

### 3. Grid Size
Small (10×10) vs. large (50×50):
- Does spread rate scale linearly?
- Edge effects on small grids

### 4. Grid Density
Modify to allow empty cells:
- How do gaps affect spread?
- Create "barriers" to transmission

## Extensions (Future Enhancements)

### 1. Forgetting Mechanism
Agents forget rumor after N steps of not hearing it:
- Add `steps_since_last_heard` counter
- Revert `knows_rumor` to False if threshold exceeded

### 2. Skepticism
Agents require multiple exposures before believing:
- Add `belief_threshold` parameter
- Only set `knows_rumor = True` when `times_heard >= threshold`

### 3. Network Structure
Replace grid with social network:
- Use NetworkGrid instead of SingleGrid
- Define friend connections (small-world, scale-free)
- Transmission follows edges, not spatial proximity

### 4. Heterogeneous Agents
Different agent types:
- "Influencers" who tell multiple neighbors per step
- "Skeptics" who don't spread even when they know
- "Fact-checkers" who can stop believing

### 5. Rumor Mutation
Rumor changes as it spreads:
- Track rumor "version" or "accuracy"
- Transmission has chance to mutate message
- Visualize how distortion accumulates

### 6. Communication Probability
Not every telling succeeds:
- Add `transmission_probability` parameter (0.0 - 1.0)
- Transmission only occurs with probability p
- Models attention/trust factors

## Technical Notes

### Mesa Version
Built for Mesa 3.0+ (Solara-based visualization)

### Performance
- Grid size impact: O(width × height) agents
- Each step: O(n) where n = number of agents
- Recommended max: 50×50 = 2,500 agents for smooth visualization

### Data Storage
DataCollector stores full time series:
- Model-level: Small (4 metrics × steps)
- Agent-level: Large (2 metrics × agents × steps)
- For large/long runs, consider disabling agent-level collection

## References

- Mesa Documentation: https://mesa.readthedocs.io/
- Agent-Based Models: Wilensky, U. (1997). NetLogo Rumor Mill model
- Diffusion Theory: Rogers, E. M. (2003). Diffusion of Innovations

## License

This is an educational example model for learning Mesa framework.
