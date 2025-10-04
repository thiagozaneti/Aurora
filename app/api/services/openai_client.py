from openai import OpenAI
from .openai_prompt import SCHEMA,SYSTEM_PROMPT
from typing import Dict
import os
import json
from dotenv import load_dotenv


load_dotenv()

class TextAnalyzer:
  def __init__(self,
                 model: str = "gpt-4.1",
                 temperature: float = 0.3):

        self.client = OpenAI(api_key= os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.temperature = temperature
        self.system_prompt = SYSTEM_PROMPT

        
  def analyze(self, user_text:str) -> Dict[str, any]:
      response = self.client.chat.completions.create(
        model=self.model,
        seed=7,
        temperature=self.temperature,
        response_format={"type": "json_schema", "json_schema": SCHEMA},
        messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_text
                    }
                ])
      analysis_content = response.choices[0].message.content
      return json.loads(analysis_content)
    
