from games import OneShotGame, SimultaneousGame
from agents.character_agents import agents
from src.config import CFG


class PrisonersDilemmaGame(OneShotGame, SimultaneousGame):
    # No additional methods needed if logic is covered by parents
    pass


if __name__ == "__main__":
    game = PrisonersDilemmaGame({"Alice": agents["skeptical_individualist"],
                                 "Bob": agents["passive_observer"]},
                                 game_name="prisoner_dilemma")
    game.play_game()
    result_data = {
        "game": game.game_name,
        "agents": [name for name in game.agents.keys()],  # e.g. ["Alice", "Bob"]
        "rounds": game.history  # list of round result dicts
    }

    import json

    with open(CFG.results_dir / f"{game.game_name}_Alice_vs_Bob.json", "w") as f:
        json.dump(result_data, f, indent=4)
