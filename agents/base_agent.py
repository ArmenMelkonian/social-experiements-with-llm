from atomic_agents.agents.base_agent import BaseAgent, BaseAgentConfig
from atomic_agents.lib.components.system_prompt_generator import SystemPromptGenerator
from instructor import Instructor
from pydantic import BaseModel, Field
import httpx


class AgentInput(BaseModel):
    query: str = Field(..., description="Query for the move")

class AgentOutput(BaseModel):
    action: str = Field(..., description="Chosen action by the agent")

# Shared HTTP client
http_client = httpx.Client(base_url="http://localhost:11434")

# Create function compatible with Instructor
def ollama_create(messages, **kwargs):
    """
    Translate Instructor/ChatML messages → Ollama /api/generate payload
    """
    prompt = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
    model_name = kwargs.get("model", "llama3")        # default model
    params = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }
    # kwargs such as temperature, top_p, etc. get forwarded if supplied
    for key in ("temperature", "top_p", "top_k", "repeat_penalty"):
        if key in kwargs:
            params[key] = kwargs[key]

    resp = http_client.post(
        "/api/generate",
        json={
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "format": "json"  # ✅ accepted in current releases
        }
    )                         # raise if bad HTTP

    content = resp.json()["response"].strip()
    return eval(content)

# ---------- 3) GameAgent class -----------------------------------
class GameAgent(BaseAgent):
    """
    Wraps an Instructor model hooked to Ollama and exposes .run().
    """
    def __init__(self, name: str, background_prompt: str, model_name: str = "llama3.2"):
        self.name = name
        instructor_model = Instructor(
            client=http_client,          # uses the shared httpx.Client
            create=ollama_create,        # our helper above
            model=model_name
        )

        system_prompt_generator = SystemPromptGenerator(
            background=[background_prompt],  # persona text
            steps=[],                        # filled each turn by game logic
            output_instructions=[]           # optional: schema hints
        )

        cfg = BaseAgentConfig(
            name=name,
            system_prompt_generator=system_prompt_generator,
            input_schema=AgentInput,
            output_schema=AgentOutput,
            client=instructor_model,         # <-- Instructor instance
            model=model_name                 # model id (string) for logging
        )
        super().__init__(cfg)