"""
Visualization interface for the Rumor Mill model using Mesa's SolaraViz.
"""
from mesa.visualization import SolaraViz, make_plot_component, SpaceRenderer
from mesa.visualization.components import AgentPortrayalStyle
from model import RumorMillModel


def agent_portrayal(agent):
    """
    Define how agents are displayed in the grid visualization.
    Red = knows rumor, Blue = doesn't know rumor
    """
    return AgentPortrayalStyle(color="red" if agent.knows_rumor else "blue", size=50)


# Model parameters that can be adjusted via UI sliders and checkboxes
model_parames = {
    "know_rumor_ratio": {
        "type": "SliderFloat",
        "value": 0.3,
        "label": "Initial Percentage Knowing Rumor",
        "min": 0.0,
        "max": 1.0,
        "step": 0.01,
    },
    "rumor_spread_chance": {
        "type": "SliderFloat",
        "value": 0.5,
        "label": "Rumor Spread Chance",
        "min": 0.0,
        "max": 1.0,
        "step": 0.01,
    },
    "eight_neightborhood": {
        "type": "Checkbox",
        "value": False,
        "label": "Use Eight Neighborhood",
    },
    "width": 10,
    "height": 10,
}

# Create initial model instance
rumor_model = RumorMillModel(width=10, height=10, know_rumor_ratio=0.3, rumor_spread_chance=0.5, eight_neightborhood=False)

# Create grid renderer to visualize agents on the grid
renderer = SpaceRenderer(model=rumor_model, backend="matplotlib").render(
    agent_portrayal=agent_portrayal
)

# Create plot components to track metrics over time
rumor_spread_plot = make_plot_component(
    "Percentage_Knowing_Rumor", page=1  # Track percentage who know rumor
)
successive_diff_plot = make_plot_component(
    "Times_Heard_Rumor", page=1  # Track average times heard
)
ratio_knowing_rumor_plot = make_plot_component(
    "Ratio_Knowing_Rumor", page=1  # Track ratio knowing rumor
)

# Create the visualization page with all components
page = SolaraViz(
    rumor_model,
    renderer,
    components=[rumor_spread_plot, successive_diff_plot, ratio_knowing_rumor_plot],
    model_params=model_parames,
    name="Rumor Mill Model",
)