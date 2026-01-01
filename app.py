from mesa.visualization import SolaraViz, make_plot_component, SpaceRenderer
from mesa.visualization.components import AgentPortrayalStyle
from model import RumorMillModel


def agent_portrayal(agent):
    # agent portrayal based on knows_rumor attribute
    return AgentPortrayalStyle(color="red" if agent.knows_rumor else "blue", size=50)

model_parames = {
    "know_rumor_ratio": {
        "type": "SliderFloat",
        "value": 0.3,
        "label": "Initial Percentage Knowing Rumor",
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

rumor_model = RumorMillModel(width=10, height=10, know_rumor_ratio=0.3, eight_neightborhood=False)

renderer = SpaceRenderer(model=rumor_model, backend="matplotlib").render(
    agent_portrayal=agent_portrayal
)

rumor_spread_plot = make_plot_component(
    "Percentage_Knowing_Rumor", page=1
)
successive_diff_plot = make_plot_component(
    "Times_Heard_Rumor", page=1
)
ratio_knowing_rumor_plot = make_plot_component(
    "Ratio_Knowing_Rumor", page=1
)

page = SolaraViz(
    rumor_model,
    renderer,
    components=[rumor_spread_plot, successive_diff_plot, ratio_knowing_rumor_plot],
    model_params=model_parames,
    name="Rumor Mill Model",
)