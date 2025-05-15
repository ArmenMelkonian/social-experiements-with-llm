import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.config import CFG
from analysis.base_analyzer import BaseAnalyzer

class PDSummary(BaseAnalyzer):
    def _tidy(self) -> pd.DataFrame:
        rows = []
        for pair_idx, game in enumerate(self.raw["rounds"], start=1):
            rd   = game[0]["Round 1"]["agents"]          # one-shot ⇒ only “Round 1”
            player1, player2 = rd
            rows.append(
                {"pair": pair_idx, "player 1": player1["action"], "player 2": player2["action"]}
            )
        return pd.DataFrame(rows)

    # ---------- stats ----------
    def special_stats(self):
        coop_mask = (self.df["player 1"] == "C") & (self.df["player 2"] == "C")
        print(f"Cooperation rate: {coop_mask.mean():.2%}")

        # build simple 2 × 2 outcome matrix
        first  = self.df["player 1"]
        second = self.df["player 2"]
        matrix = pd.crosstab(first, second)                      # rows = Player 1, cols = Player 2
        print("\nOutcome counts (rows=P1, cols=P2):\n", matrix)

        # stash for plotting
        self._cross = matrix

    def make_plots(self):
        sns.heatmap(self._cross, annot=True, fmt="d", cmap="Blues", cbar=False)
        # plt.title("Prisoner’s Dilemma outcome matrix")
        # plt.xlabel("Player 2")
        # plt.ylabel("Player 1")
        plt.title("Բանտարկյալների դիլեմայի մատրիցա")
        plt.xlabel("Խաղացող 2")
        plt.ylabel("Խաղացող 1")
        plt.savefig(CFG.figures_dir / "pd_matrix_armenian.png")
        plt.close()


if __name__ == "__main__":
    analyzer = PDSummary(CFG.results_dir / "prisoner_dilemma_simulation.json")
    analyzer.special_stats()
    analyzer.make_plots()
