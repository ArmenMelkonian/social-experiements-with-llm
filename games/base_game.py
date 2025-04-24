import copy
from abc import ABC, abstractmethod
from agents.base_agent import GameAgent
from src.config import CFG
from src.utils import read_prompt_template


class BaseGame(ABC):
    def __init__(self, agents: dict [str, GameAgent], game: str):
        self.agents = agents
        self.game = game
        self.state = {}
        self.history = []
        self.add_game_description()
        self.pair_agents = self.generate_agent_pairs()

    def generate_agent_pairs(self):
        return [([name1, agent1], [name2, agent2]) for name1, agent1 in self.agents.items() for name2, agent2 in self.agents.items()]

    def add_game_description(self):
        for _, agent in self.agents.items():
            templates_dir = CFG.games_templates_dir / self.game
            game_prompt = read_prompt_template(templates_dir, "game_description").render()
            agent.system_prompt_generator.background.append(game_prompt)

    def set_player_instructions(self, agent_1: GameAgent, agent_2: GameAgent):
        templates_dir = CFG.games_templates_dir / self.game
        instruction_prompt = read_prompt_template(templates_dir, "player_instruction").render()
        agent_1.system_prompt_generator.steps = [instruction_prompt]
        agent_2.system_prompt_generator.steps = [instruction_prompt]
        return agent_1, agent_2


    @abstractmethod
    def play_round(self):
        pass

    def play_game(self, rounds: int):
        for _ in range(rounds):
            self.play_round()
