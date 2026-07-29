import pandas as pd
from sklearn.metrics import accuracy_score, classification_report

class Evaluator:
    def __init__(self, results_data: list[dict]):
        #expected keys in each dict: 'true_label', 'predicted_label', 'event_id', 'action', 'synthesis'
        self.df = pd.DataFrame(results_data)
        
    def generate_report(self):
        y_true = self.df['true_label']
        y_pred = self.df['predicted_label']
        
        accuracy = accuracy_score(y_true, y_pred)
        report = classification_report(
            y_true, 
            y_pred, 
            labels=["LOW", "MEDIUM", "HIGH"], 
            zero_division=0
        )
        
        print("\n" + "="*40)
        print(" PIPELINE EVALUATION REPORT ")
        print("="*40)
        print(f"Overall Accuracy: {accuracy * 100:.2f}%\n")
        print("Detailed Metrics:")
        print(report)
        
        # Isolate and print misclassifications to debug the LLM's reasoning
        errors = self.df[self.df['true_label'] != self.df['predicted_label']]
        if not errors.empty:
            print("-" * 40)
            print(f" MISCLASSIFICATIONS ({len(errors)}) ")
            print("-" * 40)
            for _, row in errors.iterrows():
                print(f"Event ID:  {row.get('event_id', 'N/A')}")
                print(f"Action:    {row.get('action', '')}")
                print(f"Expected:  {row['true_label']} | Predicted: {row['predicted_label']}")
                print(f"CoT Synth: {row.get('synthesis', '')}\n")
        else:
            print("-" * 40)
            print(" Perfect Classification! No errors detected. ")
            print("-" * 40)
