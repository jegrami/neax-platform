import pandas as pd
from score_lga_input import minmax_0_100


def test_demand_score_is_bounded_0_100():
    df = pd.DataFrame(
        {
            "population_density": [180, 250, 320],
            "health_facilities": [7, 12, 15],
        }
    )

    pop_norm = minmax_0_100(df["population_density"])
    health_norm = minmax_0_100(df["health_facilities"])
    demand_score = (0.7 * pop_norm) + (0.3 * health_norm)

    assert (demand_score >= 0).all()
    assert (demand_score <= 100).all()


