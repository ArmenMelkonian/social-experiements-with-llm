from games import MultiRoundGame, SimultaneousGame
from agents.character_agents import agents


class FirstBidAuction(MultiRoundGame, SimultaneousGame):
    pass


if __name__ == "__main__":
    game = FirstBidAuction(agents,
                           game_name="first_bid_auction",
                           players_n=5,
                           rounds=3,
                           player_output="bid")
    game.simulate(pairs=100)
    game.save_results()
