from games.base_game import BaseGame


class OneShotGame(BaseGame):
    def play_game(self, rounds: int = 1) -> dict:
        """Override to ignore rounds parameter and run exactly one round."""
        result = self.play_round()
        # Optionally, write out result immediately or do any cleanup.
        return result