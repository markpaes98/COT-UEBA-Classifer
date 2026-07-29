import os
import json
from dotenv import load_dotenv
from tqdm import tqdm

from src.classifier import UEBAClassifier
from src.evaluator import Evaluator

def load_data(filepath: str) -> list[dict]:
    with open(filepath, 'r') as f:
        return [json.loads(line) for line in f]

def main():
    #env and API key
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")
    
    if not api_key or api_key.startswith("sk-your-api-key"):
        print("Error: Please set a valid OPENAI_API_KEY in your .env file.")
        return

    print(f"Initializing UEBA Classifier using {model_name}...")
    classifier = UEBAClassifier(api_key=api_key, model=model_name)
    
    #load the sample dataset
    data_path = "data/sample_logs.jsonl"
    try:
        events = load_data(data_path)
        print(f"Loaded {len(events)} events from {data_path}.\n")
    except FileNotFoundError:
        print(f"Error: Could not find data file at {data_path}.")
        print("Ensure you are running this script from the project root.")
        return

    #run the Chain of Thought classification pipeline
    results = []
    print("Starting classification pipeline...")
    
    # tqdm provides a clean progress bar in the terminal
    for event in tqdm(events, desc="Processing Events", unit="event"):
        try:
            #enforce CoT schema under the hood
            cot_result = classifier.classify_event(event)
            
            results.append({
                "event_id": event.get("event_id"),
                "action": event.get("action"),
                "true_label": event.get("true_label"),
                "predicted_label": cot_result.risk_level.value, # Extract string from Enum
                "synthesis": cot_result.step_3_synthesis        # Capture reasoning for evaluation
            })
            
        except Exception as e:
            print(f"\nFailed to classify event {event.get('event_id')}: {e}")

    # performance eval
    if results:
        evaluator = Evaluator(results)
        evaluator.generate_report()
    else:
        print("No results generated. Check your API connection and data formatting.")

if __name__ == "__main__":
    main()
