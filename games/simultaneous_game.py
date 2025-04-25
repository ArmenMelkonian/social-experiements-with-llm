from collections import defaultdict

import httpx
from loguru import logger

from games import BaseGame


class SimultaneousGame(BaseGame):

    def play_round(self, *agent_names, idx: int = None, history: list = None) -> dict:
        self.current_round += 1
        if history is None:
            history = []
        name_counts = defaultdict(int)
        agents = {}
        for name in agent_names:
            name_counts[name] += 1
            key = f"{name}{name_counts[name]}" if name_counts[name] > 1 else name
            agents[key] = self.agents[name]

        self.set_player_instructions(*agents.values(), history=history)

        input_prompt = {"content": "Your turn to move."}
        outputs = {}
        for agent_name, agent in agents.items():
            try:
                output = self.get_output(agents[agent_name], input_prompt)
            except Exception as e:
                logger.error(f"Couldn't play move for agent: {agent_name}, got {e}")
                output = {}
            outputs[agent_name] = output

        actions = {}
        for agent_name, output in outputs.items():

            action = output.get(self.player_output)
            if action is None:
                base_name = self.remove_trailing_number(agent_name)# handle bad output
                action = output.get(base_name)

            actions[agent_name] = action

        batch_result = {
            "agents": [{"name": name, self.player_output: action} for name, action in actions.items()]
        }
        print(f"Round {self.current_round} (Pair {idx}/{len(self.pairs)}): {', '.join(f'{agent_name} → {action}' for agent_name, action in actions.items())}")
        return batch_result
