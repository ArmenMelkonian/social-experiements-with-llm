from games import MultiRoundGame, SimultaneousGame
from agents.character_agents import agents


class PublicGoodsGame(MultiRoundGame, SimultaneousGame):
    pass


if __name__ == "__main__":
    game = PublicGoodsGame(agents,
                           game_name="public_goods_game",
                           rounds=3,
                           players_n=4,
                           player_output="g")
    game.simulate()
    game.save_results()
