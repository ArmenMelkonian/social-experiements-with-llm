from games.base_game import BaseGame

class SequentialGame(BaseGame):

    # TODO: add new method play_round_batch and rename later
    def play_round(self) -> dict:
        self.current_round += 1
        agent_names = list(self.agents.keys())
        first_agent = self.agents[agent_names[0]]
        second_agent = self.agents[agent_names[1]]
        # Render prompt for first agent (no prior move info needed)
        instruction1 = self._player_instruction_tmpl.render(round=self.current_round,
                                                            total_rounds=self.total_rounds,
                                                            history=self._format_history(),
                                                            last_move=None)
        first_agent.config.system_prompt_generator.steps = [instruction1]
        # First agent acts
        result1 = first_agent.run({"content": "Your move."})
        action1 = result1.action
        # Now render prompt for second agent, including first agent's move
        instruction2 = self._player_instruction_tmpl.render(round=self.current_round,
                                                            total_rounds=self.total_rounds,
                                                            history=self._format_history(),
                                                            last_move=action1)
        second_agent.config.system_prompt_generator.steps = [instruction2]
        result2 = second_agent.run({"content": f"{first_agent.config.name} chose {action1}. Your move."})
        action2 = result2.action
        # Record the round outcome
        round_result = {
            "round": self.current_round,
            "first_player": {"name": first_agent.config.name, "action": action1},
            "second_player": {"name": second_agent.config.name, "action": action2}
        }
        self.history.append(round_result)
        print(f"Round {self.current_round}: {first_agent.config.name} → {action1}, then {second_agent.config.name} → {action2}")
        return round_result