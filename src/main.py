from agents.character_agents import agents
from games.game_simulator import PrisonersDilemma
from games.one_shot_game import OneShotGame


def main():
    game = OneShotGame(agents=agents, game="prisoner_dilemma")
    game.play_game(rounds=5)

if __name__ == "__main__":
    main()
