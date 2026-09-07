import json
import random

def generate_llm_dataset(filename="weather_dataset.jsonl", samples=2000):
    with open(filename, 'w') as f:
        for _ in range(samples):
            
            # Scenario 1: 70% dry baseline weather
            if random.random() < 0.7:
                history = [0.0, 0.0, 0.0]
                future = [0.0, 0.0, 0.0]
                
            # Scenario 2: 30% building storm weather
            else:
                h1 = round(random.uniform(0, 20), 1)
                h2 = round(h1 + random.uniform(-5, 10), 1)
                h3 = round(max(0, h2 + random.uniform(-10, 15)), 1)
                history = [h1, max(0, h2), h3]
                
                f1 = round(max(0, h3 * 0.8), 1)
                f2 = round(max(0, f1 * 0.5), 1)
                f3 = round(max(0, f2 * 0.2), 1)
                future = [f1, f2, f3]

            prompt = f"Given the past 3 hours of rainfall (mm): {history}. Predict the next 3 hours."
            response = str(future)
            
            formatted_text = f"<s>[INST] {prompt} [/INST] {response} </s>"
            
            record = {"text": formatted_text}
            f.write(json.dumps(record) + '\n')

    print(f"✅ Generated {samples} fine-tuning pairs in {filename}")

if __name__ == "__main__":
    generate_llm_dataset()