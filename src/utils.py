from pathlib import Path
from typing import Union

import jinja2


def read_prompt_template(path: Union[Path, str], name: str) -> jinja2.Template:
    with open(path / f"{name}.j2") as f:
        return jinja2.Template(f.read())
