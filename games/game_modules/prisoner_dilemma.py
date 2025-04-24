from games import OneShotGame, SimultaneousGame
from agents.character_agents import agents


class PrisonersDilemmaGame(OneShotGame, SimultaneousGame):
    pass


if __name__ == "__main__":
    game = PrisonersDilemmaGame(agents,
                                game_name="prisoner_dilemma",
                                players_n=2,
                                player_output="action")
    game.simulate()
    game.save_results()
