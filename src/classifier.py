import json
from enum import Enum
from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI
from src.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class CoTAnalysisResult(BaseModel):
    #Pydantic model that enforces the Chain of Thought structure.

    step_1_security_analysis: str = Field(
        description="Analysis of the raw technical risks or policy violations."
    )
    step_2_context_and_privacy: str = Field(
        description="Evaluation of business justification and privacy norms."
    )
    step_3_synthesis: str = Field(
        description="Final weighing of security vs. context."
    )
    risk_level: RiskLevel = Field(
        description="The final computed risk label."
    )

class UEBAClassifier:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def classify_event(self, event_data: dict) -> CoTAnalysisResult:
        #user prompt with the specific event data
        user_content = USER_PROMPT_TEMPLATE.format(
            event_id=event_data.get("event_id", "UNKNOWN"),
            user_role=event_data.get("user_role", "UNKNOWN"),
            action=event_data.get("action", "UNKNOWN"),
            time=event_data.get("time", "UNKNOWN"),
            context=event_data.get("context", "None")
        )

        try:
            # Call the LLM using JSON mode
            response = self.client.chat.completions.create(
                model=self.model,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.2 # Low temperature for more deterministic reasoning
            )
            
            raw_output = response.choices[0].message.content
            
            # Parse and validate the JSON string into our Pydantic model
            parsed_data = json.loads(raw_output)
            return CoTAnalysisResult(**parsed_data)
            
        except json.JSONDecodeError:
            raise ValueError("The LLM failed to return valid JSON.")
        except ValidationError as e:
            raise ValueError(f"The LLM output did not match the expected schema: {e}")
        except Exception as e:
            raise RuntimeError(f"An error occurred during API execution: {e}")
