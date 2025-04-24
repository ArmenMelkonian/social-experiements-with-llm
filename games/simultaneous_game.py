from collections import defaultdict

from games import BaseGame


class SimultaneousGame(BaseGame):

    def play_round(self):
        self.current_round += 1
        for idx, pair in enumerate(self.pairs, start=1):
            self.play_round_batch(*pair, idx=idx)

    def play_round_batch(self, *agent_names, idx) -> dict:
        name_counts = defaultdict(int)
        agents = {}
        for name in agent_names:
            name_counts[name] += 1
            key = f"{name}{name_counts[name]}" if name_counts[name] > 1 else name
            agents[key] = self.agents[name]

        self.set_player_instructions(*agents.values())

        input_prompt = {"content": "Your turn to move."}

        outputs = {agent_name: agent.run(input_prompt) for agent_name, agent in agents.items()}
        actions = {agent_name: output.get(self.player_output) for agent_name, output in outputs.items()}

        round_result = {
            "round": self.current_round,
            "agents": [{"name": name, self.player_output: action} for name, action in actions.items()]
        }
        self.history.append(round_result)
        print(f"Round {self.current_round} (Pair {idx}/{len(self.pairs)}): {', '.join(f'{agent_name} → {action}' for agent_name, action in actions.items())}")
        return round_result