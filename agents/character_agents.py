import os

from agents.base_agent import GameAgent
from src.config import CFG


def load_character_prompts(directory: str):
    prompts = {}
    for filename in os.listdir(directory):
        if filename.endswith(".j2"):
            with open(os.path.join(directory, filename), 'r') as file:
                prompts[filename[:-3]] = file.read()
    return prompts

character_prompts = load_character_prompts(CFG.character_templates_dir)

agents = {}
for name, prompt in character_prompts.items():
    agents[name] = GameAgent(name=name, background_prompt=prompt)

...
