from google import genai
from google.genai import types
from src.llms.base import BaseLLMProvider
from config.settings import settings

class GeminiProvider(BaseLLMProvider):

    def __init__(self, api_key=settings.GEMINI_API_KEY, model="gemini-2.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(
        self,
        prompt: str,
        system_prompt: str,
    ) -> str:

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.2,
            ),
        )

        return response.text