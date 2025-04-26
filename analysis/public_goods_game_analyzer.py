import pandas as pd
import matplotlib.pyplot as plt

from analysis.base_analyzer import BaseAnalyzer
from src.config import CFG


class PGSummary(BaseAnalyzer):
    def _tidy(self):
        rows=[]
        for grp_ix, rounds in enumerate(self.raw["rounds"], start=1):
            for _round in rounds:
                (round_name, agents), = _round.items()
                round_num = int(round_name.split()[1])
                for player in agents["agents"]:
                    rows.append({"group": grp_ix,
                                 "round": round_num,
                                 "player": player["name"],
                                 "g": player["g"]})
        return pd.DataFrame(rows)

    def special_stats(self):
        contribution = self.df["g"]
        overall = contribution.mean()
        print(f"Mean contribution overall: {overall:.2f} (out of 100), "
              f"inter-quartile range (25-75) = ({contribution.quantile(0.25)}-{contribution.quantile(0.75)})", end="\n\n")
        by_round = self.df.groupby("round")["g"].mean()
        print("Mean per round:\n", by_round, end="\n\n")

        self.free_rider_stats()

    def free_rider_stats(self):
        free_riders = self.df[self.df["g"] == 0]
        round_fr_counts = free_riders.groupby("round").size()
        pct_round_fr = round_fr_counts / self.df.groupby("round").size()

        # (2) players who contributed 0 in *every* round they played
        player_rounds = self.df.groupby("player")["round"].nunique()
        player_zero_rounds = free_riders.groupby("player")["round"].nunique()
        persistent_fr = [
            p for p, r_tot in player_rounds.items()
            if player_zero_rounds.get(p, 0) == r_tot
        ]

        print(f"Total free-rider moves (g = 0): {len(free_riders)} "
              f"of {len(self.df)} observations → "
              f"{len(free_riders) / len(self.df):.2%} of all moves.")

        print("\nFree-rider share by round:")
        print((pct_round_fr * 100).round(1).astype(str) + " %")

        print(f"\nPlayers who *never* contributed in any round they played "
              f"(persistent free-riders): {len(persistent_fr)}")
        if persistent_fr:
            print("  ", ", ".join(sorted(persistent_fr)))

    def make_plots(self):
        by_round = self.df.groupby("round")["g"].mean()
        by_round.plot(marker="o")
        plt.ylabel("Average contribution"); plt.xlabel("Round")
        plt.title("Public Goods – contribution decay")
        plt.savefig(CFG.figures_dir / "pg_time_series.png"); plt.close()


if __name__ == "__main__":
    analyzer = PGSummary(CFG.results_dir / "public_goods_game_simulation.json")
    analyzer.run_all(skip_basic=True)
