from games.base_game import BaseGame


class PrisonersDilemma(BaseGame):
    def play_round(self):
        actions = {}
        for name, agent in self.agents.items():
            input_data = {
                "game_state": self.state,
                "history": self.history
            }
            output = agent.run(input_data)
            actions[name] = output.action
        self.history.append(actions)
        # Update game state based on actions
        # Implement payoff logic here
