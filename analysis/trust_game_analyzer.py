import pandas as pd, matplotlib.pyplot as plt

from analysis.base_analyzer import BaseAnalyzer
from src.config import CFG


class TrustSummary(BaseAnalyzer):
    def _tidy(self):
        rows=[]
        for g_ix, game in enumerate(self.raw["rounds"], start=1):
            agents = game[0]["Round 1"]["agents"]
            sender, receiver = agents
            rows.append({
                "pair": g_ix,
                "Y": sender.get("Y", 0),  # investment
                "Z": receiver.get("Z", 0),  # return
            })
        return pd.DataFrame(rows)

    def special_stats(self):
        invest = self.df["Y"]
        returned = self.df["Z"]
        print(f"Mean investment: {invest.mean():.2f}  median={invest.median():.0f}, quantiles(25-75)=({invest.quantile(0.25)}-{invest.quantile(0.75)})")
        print(f"Mean return:     {returned.mean():.2f}  median={returned.median():.0f}")
        ratio = (returned / invest.replace(0, pd.NA)).dropna()
        print(f"Return / Invest ratio (mean): {ratio.mean():.2f}")

    def make_plots(self):
        self.df.plot.scatter("Y", "Z")
        plt.xlabel("Investment Y")
        plt.ylabel("Return Z")
        plt.title("Trust Game – Returns vs. Investments")
        plt.savefig(CFG.figures_dir / "trust_scatter.png")
        plt.close()


if __name__ == "__main__":
    analyzer = TrustSummary(CFG.results_dir / "trust_game_simulation.json")
    analyzer.run_all()
