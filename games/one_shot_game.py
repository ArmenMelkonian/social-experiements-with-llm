from games.base_game import BaseGame
from games.simultaneous_game import SimultaneousGameManager


class OneShotGame(BaseGame):
    def play_round(self):
        for (_, agent_1), (_, agent_2) in self.pair_agents:
            manager = SimultaneousGameManager(agent_1, agent_2)
            self.set_player_instructions(agent_1, agent_2)
            result = manager.run_one_round(initial_state={"game": "prisoners_dilemma"})
        # actions = {}
        # for name, agent in self.agents.items():
        #     input_data = {
        #         "game_state": self.state,
        #         "history": self.history
        #     }
        #     output = agent.run(input_data)
        #     actions[name] = output.action
        # self.history.append(actions)
        ...
        # Update game state based on actions
        # Implement payoff logic here
