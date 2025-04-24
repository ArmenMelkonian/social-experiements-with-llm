from typing import Dict, List

from games import BaseGame
from agents import GameAgent


class MultiRoundGame(BaseGame):

    def __init__(self, agents: Dict[str, GameAgent], game_name: str, rounds: int, player_output: str, players_n: int = 2):
        super().__init__(agents, game_name, player_output, players_n)
        self.rounds = rounds
        self.current_round = 0

    def play_game(self) -> List[dict]:
        """Play the game for the specified number of rounds, collecting results."""
        results = []
        for _ in range(self.rounds):
            result = self.play_round()
            results.append(result)
        # After all rounds, possibly process final outcomes
        return results

    def _format_history(self):
        # Utility to format history for template (e.g., last moves or scores)
        return [ (h["agents"][0]["action"], h["agents"][1]["action"]) for h in self.history ]
