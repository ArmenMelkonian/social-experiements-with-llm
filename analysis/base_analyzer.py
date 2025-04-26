"""
Shared helpers for reading JSON result files, producing tidy DataFrames,
computing generic summary stats and saving figures.

Usage:
    from analysis.prisoner_dilemma_analyzer import PDSummary
    summary = PDSummary("results/prisoner_dilemma_simulation.json")
    summary.run_all()        # prints stats + writes plots to /figures
"""
import json
from  pathlib import Path
from abc import ABC, abstractmethod
from typing import Any, Dict

import pandas as pd

from src.config import CFG


CFG.figures_dir.mkdir(exist_ok=True)   # auto-create once


class BaseAnalyzer(ABC):
    """Abstract base class – subclass must implement `_tidy()` & `special_stats()`."""

    def __init__(self, json_path: str | Path):
        self.json_path = Path(json_path)
        self.raw: Dict[str, Any] = self._load()
        self.df: pd.DataFrame = self._tidy()   # game-specific melt

    def run_all(self, skip_basic=False) -> None:
        print(f"\n=== {self.game_name} ({len(self.df)} observations) ===")
        if not skip_basic:
            self.basic_stats()
        self.special_stats()
        self.make_plots()

    @property
    def game_name(self) -> str:
        return self.raw.get("game", self.json_path.stem)

    def _load(self) -> Dict[str, Any]:
        with open(self.json_path) as f:
            return json.load(f)

    @abstractmethod
    def _tidy(self) -> pd.DataFrame:
        """Return a flat DataFrame with at minimum columns:
           round, group_id (pair index), player, variable(s)."""
        raise NotImplementedError

    def basic_stats(self) -> None:
        print(self.df.describe(include='all').T, end="\n\n")

    @abstractmethod
    def special_stats(self) -> None: ...

    @abstractmethod
    def make_plots(self) -> None: ...
