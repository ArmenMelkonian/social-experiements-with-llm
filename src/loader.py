import os

def load_templates(directory: str):
    templates = {}
    for filename in os.listdir(directory):
        if filename.endswith(".j2"):
            with open(os.path.join(directory, filename), 'r') as file:
                templates[filename[:-3]] = file.read()
    return templates
