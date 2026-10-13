import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

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

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        return response.choices[0].message.content
    
if __name__ == "__main__":
    model = DeepSeekProvider()

    response = model.generate(
        prompt="What is reinforcement learning? Answer in one sentence.",
        system_prompt="You are a concise AI research assistant.",
    )

    print(response)