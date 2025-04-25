from typing import Dict

from agents import GameAgent
from games.base_game import BaseGame

class SequentialGame(BaseGame):

    def __init__(self, agents: Dict[str, GameAgent], game_name: str, *,
                 agent1_templ_name: str, agent2_templ_name: str,
                 agent1_player_output: str, agent2_player_output: str, rounds: int = 1):
        super().__init__(agents, game_name, players_n=2, rounds=rounds)
        self.agent1_templ_name = agent1_templ_name
        self.agent2_templ_name = agent2_templ_name
        self.agent1_player_output = agent1_player_output
        self.agent2_player_output = agent2_player_output


    def play_round(self, agent1_name, agent2_name, idx: int = None) -> dict:
        self.current_round += 1
        agent_1 = self.agents[agent1_name]
        agent_2 = self.agents[agent2_name]
        self.set_single_player_instructions(agent_1, self.agent1_templ_name)
        input_prompt_1 = {"content": "Your turn to move."}
        result1 = self.get_output(agent_1, input_prompt_1, self.agent1_player_output)
        action1 = result1.get(self.agent1_player_output)
        kwargs = {self.agent1_player_output: action1}
        self.set_single_player_instructions(agent_2, self.agent2_templ_name, **kwargs)
        input_prompt_2 = {"content": f"{agent_1.name} chose {action1}. Your move."}
        result2 = self.get_output(agent_2, input_prompt_2, self.agent2_player_output)
        action2 = result2.get(self.agent2_player_output)
        # Record the round outcome
        result = {
            "agents": [
                {"name": agent_1.name, self.agent1_player_output: action1},
                {"name": agent_2.name, self.agent2_player_output: action2}
            ]
        }
        print(f"Round {self.current_round} (Pair {idx} / {len(self.pairs)}): {agent_1.name} → {action1}, "
              f"then {agent_2.name} → {action2}")

        return result
