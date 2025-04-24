import json
from abc import ABC, abstractmethod
from typing import Dict, List
from itertools import product

from loguru import logger

from agents.base_agent import GameAgent
from src.config import CFG
from src.utils import read_prompt_template


class BaseGame(ABC):
    def __init__(self, agents: Dict[str, GameAgent], game_name: str, player_output: str, players_n: int = 2):
        self.agents = agents
        self.game_name = game_name
        self.player_output = player_output
        self.players_n = players_n
        self.history = []
        self.state = {}
        self._load_game_templates()
        self.pairs = None
        self.current_round = 0

    def _load_game_templates(self):
        templates_dir = CFG.games_templates_dir / self.game_name
        description = read_prompt_template(templates_dir, "game_description").render()
        for agent in self.agents.values():
            agent.system_prompt_generator.background.append(description)
        self._player_instruction_tmpl = read_prompt_template(templates_dir, "player")

    # def set_player_instructions(self, agent1: GameAgent, agent2: GameAgent):
    #     instruction_text = self._player_instruction_tmpl.render(round=self.current_round,
    #                                                             total_rounds=self.total_rounds,
    #                                                             history=self._format_history())
    #     agent1.system_prompt_generator.steps = [instruction_text]
    #     agent2.system_prompt_generator.steps = [instruction_text]

    def simulate(self, rounds=1):
        logger.info(f"Starting the simulation, game: {self.game_name.replace('_', ' ')}")
        self.generate_agent_pairs()
        logger.info(f"Agent pairs are created with {self.players_n} players")
        self.play_game()

    def generate_agent_pairs(self):
        self.pairs =  list(product(self.agents, repeat=self.players_n))

    def add_game_description(self):
        for _, agent in self.agents.items():
            templates_dir = CFG.games_templates_dir / self.game_name
            game_prompt = read_prompt_template(templates_dir, "game_description").render()
            agent.system_prompt_generator.background.append(game_prompt)

    def set_player_instructions(self, *agents: List[GameAgent]):
        templates_dir = CFG.games_templates_dir / self.game_name
        instruction_prompt = read_prompt_template(templates_dir, "player").render()
        for agent in agents:
            agent.system_prompt_generator.steps = [instruction_prompt]

    @abstractmethod
    def play_round(self):
        raise NotImplementedError

    def play_game(self):
        raise NotImplementedError

    @property
    def results(self):
        if not self.history:
            logger.warning(f"The game {self.game_name} is not simulated.")
        return {
            "game": self.game_name,
            "agents": [name for name in self.agents],
            "rounds": self.history
        }

    def save_results(self, save_path: str = None):
        if save_path is None:
            save_path = CFG.results_dir / f"{self.game_name}_simulation.json"
        results = self.results
        with open(save_path, "w") as f:
            json.dump(results, f, indent=4)
        logger.success(f"Simulation results of {self.game_name.replace('_', ' ')} are saved successfully.")
