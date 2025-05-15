import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from analysis.base_analyzer import BaseAnalyzer
from src.config import CFG


class UltimatumSummary(BaseAnalyzer):

    def _tidy(self) -> pd.DataFrame:
        rows = []
        for game_ix, game in enumerate(self.raw["rounds"], start=1):
            agents = game[0]["Round 1"]["agents"]
            proposer, responder = agents  # always two
            rows.append(
                {
                    "pair": game_ix,
                    "offer": proposer["offer"],
                    "accepted": 1 if responder["action"] == "A" else 0,
                }
            )
        return pd.DataFrame(rows)

    def special_stats(self):
        print("Offer stats", self.df["offer"].describe(), sep="\n-----------\n", end="\n\n")          # full numeric summary

        acc_rate = self.df["accepted"].mean()
        low_acc = self.df[self.df["offer"] < 2]["accepted"].mean()

        print(f"Overall acceptance rate : {acc_rate:6.2%}")
        print(f"Offers <2   acceptance  : {low_acc:6.2%}")


    def make_plots(self):
        plt.figure(figsize=(7, 4))
        self.df = self.df.rename({"accepted": "Ընտրություն"}, axis=1)

        sns.histplot(
            data=self.df,
            x="offer",
            hue=self.df["Ընտրություն"].map({1: "Ընդունված", 0: "Մերժված"}),
            multiple="stack",
            bins=10,
            palette={"Ընդունված": "steelblue", "Մերժված": "indianred"},
            edgecolor="white",
        )

        plt.xlabel("Առաջարկ (միավորներ)")
        plt.ylabel("Քանակ")
        plt.title("Ուլտիմատումի խաղի առաջարկներ: ընդունված vs մերժված")
        plt.tight_layout()

        plt.savefig(CFG.figures_dir / "ultimatum_offers_armenian.png", dpi=300)
        plt.close()


if __name__ == "__main__":
    analyzer = UltimatumSummary(CFG.results_dir / "ultimatum_game_simulation.json")
    analyzer.run_all()
