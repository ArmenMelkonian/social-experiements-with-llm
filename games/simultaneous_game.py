from agents.base_agent import GameAgent
from typing import Dict, List


class SimultaneousGameManager:
    def __init__(self, agent_a: GameAgent, agent_b: GameAgent):
        self.agent_a = agent_a
        self.agent_b = agent_b
        self.history: List[Dict] = []

    def run_one_round(self, initial_state: dict):
        input_data = {
            "content": "do your move"
        }

        # 🔁 Simultaneous moves
        output_a = self.agent_a.run(input_data)
        output_b = self.agent_b.run(input_data)

        result = {
            "round": 1,
            "agent_a": {
                "name": self.agent_a.config.name,
                "action": output_a.action
            },
            "agent_b": {
                "name": self.agent_b.config.name,
                "action": output_b.action
            }
        }

        self.history.append(result)

        print(f"Round 1")
        print(f"  {self.agent_a.config.name} → {output_a.action}")
        print(f"  {self.agent_b.config.name} → {output_b.action}")

        return result
