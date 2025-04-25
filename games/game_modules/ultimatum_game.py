from games import OneShotGame, SequentialGame
from agents.character_agents import agents


class UltimatumGame(OneShotGame, SequentialGame):
    pass


if __name__ == "__main__":
    game = UltimatumGame(agents,
                         game_name="ultimatum_game",
                         agent1_templ_name="proposer",
                         agent2_templ_name="responder",
                         agent1_player_output="offer",
                         agent2_player_output="action")
    game.simulate(pairs=100)
    game.save_results()
