from games.base_game import BaseGame


class OneShotGame(BaseGame):

    def play_game(self):
        """Override to ignore rounds parameter and run exactly one round."""
        for idx, pair in enumerate(self.pairs, start=1):
            self.current_round = 0
            result = self.play_round(*pair, idx=idx)
            self.history.append([{f"Round {self.current_round}": result}])
