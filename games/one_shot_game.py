from games.base_game import BaseGame


class OneShotGame(BaseGame):

    def play_game(self) -> dict:
        """Override to ignore rounds parameter and run exactly one round."""
        result = self.play_round()
        return result