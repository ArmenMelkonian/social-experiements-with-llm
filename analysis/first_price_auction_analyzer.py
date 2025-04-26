import pandas as pd
import matplotlib.pyplot as plt

from analysis.base_analyzer import BaseAnalyzer
from src.config import CFG


class AuctionSummary(BaseAnalyzer):
    def _tidy(self):
        rows = []
        for grp_ix, auction in enumerate(self.raw["rounds"], start=1):
            for _round in auction:
                (round_name, agents), = _round.items()
                round_num = int(round_name.split()[1])

                bids = agents["agents"]
                winner = max(bids, key=lambda x: x["bid"])
                rows.append({"auction": grp_ix,
                             "round": round_num,
                             "winner": winner["name"],
                             "winning_bid": winner["bid"],
                             "mean_bid": pd.Series([b["bid"] for b in bids]).mean()})
        return pd.DataFrame(rows)

    def special_stats(self):
        print(self.df[["winning_bid", "mean_bid"]].describe(), end="\n\n")
        # overbidding relative to mean
        diff = self.df["winning_bid"] - self.df["mean_bid"]
        print(f"Avg winner minus mean bid: {diff.mean():.2f}")

    def make_plots(self):
        """Plot mean winning bid *and* mean bid per round on one figure."""
        by_round = self.df.groupby("round")

        ax = by_round["winning_bid"].mean().plot(
            marker="o", label="Mean winning bid"
        )

        # add overall mean-bid curve
        by_round["mean_bid"].mean().plot(
            marker="s", linestyle="--", label="Mean bid", ax=ax
        )

        plt.ylabel("Bid (currency units)")
        plt.xlabel("Round")
        plt.title("First-Price Auction – bid dynamics")
        plt.legend()
        plt.tight_layout()
        plt.savefig(CFG.figures_dir / "auction_winners.png")
        plt.close()


if __name__ == "__main__":
    analyzer = AuctionSummary(CFG.results_dir / "first_bid_auction_simulation.json")
    analyzer.run_all(skip_basic=True)
