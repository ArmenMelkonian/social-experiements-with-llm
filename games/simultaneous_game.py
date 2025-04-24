from games import BaseGame


class SimultaneousGame(BaseGame):
    def play_round(self) -> dict:
        self.current_round += 1
        # Prepare prompts for this round for both agents
        agent_names = list(self.agents.keys())
        agent1, agent2 = self.agents[agent_names[0]], self.agents[agent_names[1]]
        self.set_player_instructions(agent1, agent2)
        # Get actions from both agents (simultaneous decisions)
        input_prompt = {"content": "Your turn to move."}  # a generic placeholder message
        output1 = agent1.run(input_prompt)
        output2 = agent2.run(input_prompt)
        # Assume outputX.action gives the chosen action as per AgentOutput schema
        action1 = output1["action"]
        action2 = output2['action']
        # Record the results of this round
        round_result = {
            "round": self.current_round,
            "agents": [
                {"name": agent1.name, "action": action1},
                {"name": agent2.name, "action": action2}
            ]
        }
        self.history.append(round_result)
        print(f"Round {self.current_round}: {agent1.name} → {action1}, {agent2.name} → {action2}")
        return round_result