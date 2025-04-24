from abc import ABC, abstractmethod
from typing import Dict

from agents.base_agent import GameAgent
from src.config import CFG
from src.utils import read_prompt_template


class BaseGame(ABC):
    def __init__(self, agents: Dict[str, GameAgent], game_name: str):
        self.agents = agents
        self.game_name = game_name
        self.history = []
        self.state = {}
        self._load_game_templates()
        self.current_round = 0

    def _load_game_templates(self):
        # Compose path to the game’s template directory
        templates_dir = CFG.games_templates_dir / self.game_name
        # Load and render game description template (no dynamic data needed here)
        description = read_prompt_template(templates_dir, "game_description").render()
        # Append game description to each agent's system (background) prompts
        for agent in self.agents.values():
            agent.system_prompt_generator.background.append(description)
        # Load player instruction template for use each round
        self._player_instruction_tmpl = read_prompt_template(templates_dir, "player")

    def set_player_instructions(self, agent1: GameAgent, agent2: GameAgent):
        instruction_text = self._player_instruction_tmpl.render(round=self.current_round,
                                                                total_rounds=self.total_rounds,
                                                                history=self._format_history())
        # Set the same instruction for both agents (since symmetric roles)
        agent1.system_prompt_generator.steps = [instruction_text]
        agent2.system_prompt_generator.steps = [instruction_text]

    def generate_agent_pairs(self):
        return [([name1, agent1], [name2, agent2]) for name1, agent1 in self.agents.items() for name2, agent2 in self.agents.items()]

    def add_game_description(self):
        for _, agent in self.agents.items():
            templates_dir = CFG.games_templates_dir / self.game_name
            game_prompt = read_prompt_template(templates_dir, "game_description").render()
            agent.system_prompt_generator.background.append(game_prompt)

    def set_player_instructions(self, agent_1: GameAgent, agent_2: GameAgent):
        templates_dir = CFG.games_templates_dir / self.game_name
        instruction_prompt = read_prompt_template(templates_dir, "player").render()
        agent_1.system_prompt_generator.steps = [instruction_prompt]
        agent_2.system_prompt_generator.steps = [instruction_prompt]
        return agent_1, agent_2


    @abstractmethod
    def play_round(self):
        raise NotImplementedError

    def play_game(self, rounds: int):
        raise NotImplementedError
