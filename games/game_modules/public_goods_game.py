from games import MultiRoundGame, SimultaneousGame
from agents.character_agents import agents


class PublicGoodsGame(MultiRoundGame, SimultaneousGame):
    pass


if __name__ == "__main__":
    game = PublicGoodsGame(agents,
                           game_name="public_goods_game",
                           players_n=5,
                           rounds=4,
                           player_output="g")
    game.simulate(pairs=100)
    game.save_results()
