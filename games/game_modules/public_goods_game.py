from agents import GameAgent
from games import MultiRoundGame, SimultaneousGame
from agents.character_agents import agents
from src.config import CFG
from src.utils import read_prompt_template


class PublicGoodsGame(MultiRoundGame, SimultaneousGame):
    pass
    # def set_player_instructions(self, agent_1: GameAgent, agent_2: GameAgent):
    #     templates_dir = CFG.games_templates_dir / self.game_name
    #     instruction_prompt = read_prompt_template(templates_dir, "player").render()
    #     agent_1.system_prompt_generator.steps = [instruction_prompt]
    #     agent_2.system_prompt_generator.steps = [instruction_prompt]
    #     return agent_1, agent_2


if __name__ == "__main__":
    game = PublicGoodsGame(agents,
                           game_name="public_goods_game",
                           rounds=3,
                           players_n=4,
                           player_output="g")
    game.simulate()
    result_data = {
        "game": game.game_name,
        "agents": [name for name in game.agents.keys()],
        "rounds": game.history
    }

    import json

    with open(CFG.results_dir / f"{game.game_name}.json", "w") as f:
        json.dump(result_data, f, indent=4)
