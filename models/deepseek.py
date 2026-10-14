import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

from models.base import BaseModelProvider


load_dotenv()


class DeepSeekProvider(BaseModelProvider):

    def __init__(self):
        api_key = os.getenv("DEEPSEEK_API_KEY")

        if not api_key:
            raise ValueError(
                "DEEPSEEK_API_KEY was not found in the environment."
            )

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com",
        )

        self.model = "deepseek-flash"

    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        response_schema: type[Any] | None = None,
    ) -> Any:

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        # Normal text response
        if response_schema is None:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )

            return response.choices[0].message.content

        # Structured response
        schema = response_schema.model_json_schema()

        messages.append(
            {
                "role": "user",
                "content": (
                    "Return ONLY valid JSON matching this JSON schema:\n"
                    f"{json.dumps(schema, indent=2)}"
                ),
            }
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content

        return response_schema.model_validate_json(content)

from schemas.research_spec import ResearchSpec
    
if __name__ == "__main__":
    model = DeepSeekProvider()

    response = model.generate(
        prompt="""
        I want to research how reinforcement learning can help
        a robotic arm learn to grasp previously unseen objects.

        I want to perform the experiments in simulation.
        """,
        system_prompt="""
        You are a research requirements analyst.

        Analyze the researcher's idea and convert it into
        a structured research specification.

        Do not invent information.
        Anything important that is missing should be placed
        in the unknowns field.
        """,
        response_schema=ResearchSpec,
    )

    print(response)