from atomic_agents.agents.base_agent import BaseAgent, BaseAgentConfig
from atomic_agents.lib.components.system_prompt_generator import SystemPromptGenerator
from instructor import Instructor
from pydantic import BaseModel, Field
import httpx


class AgentInput(BaseModel):
    game_state: dict = Field(..., description="Current state of the game")
    history: list = Field(..., description="History of moves")

class AgentOutput(BaseModel):
    action: str = Field(..., description="Chosen action by the agent")

# Shared HTTP client
http_client = httpx.Client(base_url="http://localhost:11434")

# Create function compatible with Instructor
def ollama_create(messages, **kwargs):
    prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
    response = http_client.post(
        "/api/generate",
        json={
            "model": kwargs.get("model", "mistral"),
            "prompt": prompt,
            "stream": False
        }
    )
    return {
        "choices": [
            {"message": {"content": response.json()["response"]}}
        ]
    }

class GameAgent(BaseAgent):
    def __init__(self, name: str, background_prompt: str, model_name: str = "mistral"):
        instructor_model = Instructor(
            client=http_client,
            create=ollama_create,
            model=model_name
        )

        system_prompt_generator = SystemPromptGenerator(
            background=[background_prompt],
            steps=[],
            output_instructions=[]
        )

        config = BaseAgentConfig(
            name=name,
            system_prompt_generator=system_prompt_generator,
            input_schema=AgentInput,
            output_schema=AgentOutput,
            client=instructor_model,  # ✅ pass as `client`
            model=model_name           # ✅ pass model name string here
        )
        super().__init__(config)