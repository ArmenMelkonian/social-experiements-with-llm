import json
import re
from abc import ABC, abstractmethod
import random
from typing import Dict, List
from itertools import product

from loguru import logger

from agents.base_agent import GameAgent
from src.config import CFG
from src.utils import read_prompt_template


class BaseGame(ABC):
    def __init__(self, agents: Dict[str, GameAgent], game_name: str, *, players_n: int = 2, rounds: int = 1):
        self.agents = agents
        self.game_name = game_name
        self.players_n = players_n
        self.total_rounds = rounds
        self.history = []
        self.state = {}
        self.add_game_description()
        self.pairs = None
        self.current_round = 0

    def simulate(self, pairs: int = None):
        logger.info(f"Starting the simulation, game: {self.game_name.replace('_', ' ')}")
        self.generate_agent_pairs(pairs)
        logger.info(f"Agent pairs are created with {self.players_n} players")
        self.play_game()

    def generate_agent_pairs(self, pairs):
        all_pairs = list(product(self.agents, repeat=self.players_n))
        total_combinations = len(all_pairs)

        if pairs is None or pairs <= 0 or pairs > total_combinations:
            logger.warning(f"Invalid or too large pair count ({pairs}), using all {total_combinations} combinations.")
            self.pairs = all_pairs
        else:
            self.pairs = random.sample(all_pairs, pairs)


    def add_game_description(self):
        for _, agent in self.agents.items():
            templates_dir = CFG.games_templates_dir / self.game_name
            game_prompt = read_prompt_template(templates_dir, "game_description").render(
                total_rounds=self.total_rounds
            )
            agent.system_prompt_generator.background.append(game_prompt)

    def set_players_instructions(self, *agents: List[GameAgent], history: list = None):
        if history is None:
            history = []
        templates_dir = CFG.games_templates_dir / self.game_name

        for agent in agents:
            instruction_prompt = read_prompt_template(templates_dir, "player").render(
                player_name=agent.name, round=self.current_round,
                total_rounds=self.total_rounds, history=history)
            agent.system_prompt_generator.steps = [instruction_prompt]
            if hasattr(agent, "messages"):
                agent.messages = []
            agent.memory.history = []

    def set_single_player_instructions(self, agent: GameAgent, template_name: str, **kwargs):
        templates_dir = CFG.games_templates_dir / self.game_name
        instruction_prompt = read_prompt_template(templates_dir, template_name).render(**kwargs)
        agent.system_prompt_generator.steps = [instruction_prompt]
        if hasattr(agent, "messages"):
            agent.messages = []
        agent.memory.history = []

    @staticmethod
    def remove_trailing_number(text):
        return re.sub(r'\d+$', '', text)

    @staticmethod
    def get_output(agent, input_prompt, player_output: str, retries=10):
        for i in range(retries):
            try:
                output = agent.run(input_prompt)
                if isinstance(output, dict) and player_output in output:
                    return output
            except Exception as e:
                logger.error(f"Failed to get a move for agent: {agent.name}, got {e}, trying {i+1}/{retries}")
        logger.error(f"Failed to get a move for agent: {agent.name} after {retries} attempts")
        return {}


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
