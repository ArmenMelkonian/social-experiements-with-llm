from pathlib import Path

class CFG:
    parent_dir = Path(__file__).parents[1]
    data_dir = parent_dir / "data"
    games_templates_dir = data_dir / "games"
    character_templates_dir = data_dir / "characters"
    results_dir = parent_dir / "results"

