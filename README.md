# Chain of Thought (CoT) Entity Behavioral Analaysis Classifier

Using Large Language Models for Chain of Thought classification. This pipeline evaluates User-Entity Behavior Analysis (UEBA) logs to classify insider risk levels while explicitly reasoning through security indicators, business context, and privacy considerations before making a final determination.

## Architecture

This project enforces structured outputs using Pydantic. Instead of asking the LLM to simply output "High Risk" or "Low Risk", the prompt and output schema force the model to populate a `ReasoningSteps` object first.

**The CoT Pipeline:**
1. **Analyze Activity:** What is the technical action?
2. **Contextualize:** What is the user's role and historical baseline?
3. **Weigh Tensions:** Are there legitimate business reasons or privacy norms that explain the behavior?
4. **Classify:** Output the final risk label (`LOW`, `MEDIUM`, `HIGH`).

## Setup Instructions

1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your OpenAI API key.

## Usage

To run the classification pipeline on the sample data:
```bash
python main.py
