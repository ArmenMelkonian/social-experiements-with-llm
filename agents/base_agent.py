from loguru import logger

from atomic_agents.agents.base_agent import BaseAgent, BaseAgentConfig
from atomic_agents.lib.components.system_prompt_generator import SystemPromptGenerator
from instructor import Instructor
from pydantic import BaseModel, Field
import httpx


class AgentInput(BaseModel):
    query: str = Field(..., description="Query for the move")

class AgentOutput(BaseModel):
    action: str = Field(..., description="Chosen action by the agent")

http_client = httpx.Client(base_url="http://localhost:11434")


def ollama_create(messages, **kwargs):
    """
    Translate Instructor/ChatML messages → Ollama /api/generate payload
    """
    prompt = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
    model_name = kwargs.get("model", "llama3")        # default model
    params = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.1  # a little randomness
    }

    for key in ("temperature", "top_p", "top_k", "repeat_penalty"):
        if key in kwargs:
            params[key] = kwargs[key]

    resp = http_client.post(
        "/api/generate",
        json={
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
    )

    content = resp.json()["response"].strip().replace("null", "")
    try:
        return eval(content)
    except Exception as e:
        logger.error(f"Couldn't parse LLM response, got {e = }, {content = }")
        return {}

class GameAgent(BaseAgent):
    """
    Wraps an Instructor model hooked to Ollama and exposes .run().
    """
    def __init__(self, name: str, background_prompt: str, model_name: str = "llama3"):
        self.name = name
        instructor_model = Instructor(
            client=http_client,
            create=ollama_create,
            model=model_name
        )

        system_prompt_generator = SystemPromptGenerator(
            background=[background_prompt],  # persona text
            steps=[],                        # filled each turn by game logic
            output_instructions=[]
        )

        cfg = BaseAgentConfig(
            name=name,
            system_prompt_generator=system_prompt_generator,
            input_schema=AgentInput,
            output_schema=AgentOutput,
            client=instructor_model,
            model=model_name
        )
        super().__init__(cfg)
