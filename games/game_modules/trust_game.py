from games import OneShotGame, SequentialGame
from agents.character_agents import agents


class TrustGame(OneShotGame, SequentialGame):
    pass


if __name__ == "__main__":
    game = TrustGame(agents,
                     game_name="trust_game",
                     agent1_templ_name="investor",
                     agent2_templ_name="trustee",
                     agent1_player_output="Y",
                     agent2_player_output="Z")
    game.simulate(pairs=100)
    game.save_results()
