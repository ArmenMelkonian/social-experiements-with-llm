from typing import Dict, List

from games import BaseGame
from agents import GameAgent


class MultiRoundGame(BaseGame):

    def play_game(self):
        """Play the game for the specified number of rounds, collecting results."""
        for idx, pair in enumerate(self.pairs, start=1):
            pair_history = []
            self.current_round = 0
            for _ in range(self.total_rounds):
                round_result = self.play_round(*pair, idx=idx, history=pair_history)
                pair_history.append({f"Round {self.current_round}": round_result})
            self.history.append(pair_history)

    def _format_history(self):
        # Utility to format history for template (e.g., last moves or scores)
        return [ (h["agents"][0]["action"], h["agents"][1]["action"]) for h in self.history ]
