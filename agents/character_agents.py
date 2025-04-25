import os

from agents.base_agent import GameAgent
from src.config import CFG
from src.utils import read_prompt_template


def load_character_prompts(directory: str):
    prompts = {}
    for filename in os.listdir(directory):
        if filename.endswith(".j2"):
            character = filename.rsplit(".", maxsplit=1)[0]
            prompts[character] = read_prompt_template(directory, character).render()
    return prompts

character_prompts = load_character_prompts(CFG.character_templates_dir)

agents = {}
for name, prompt in character_prompts.items():
    agents[name] = GameAgent(name=name, background_prompt=prompt)
