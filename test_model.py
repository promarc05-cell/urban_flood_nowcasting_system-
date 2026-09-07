from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

print("Loading model and LoRA weights...")

base_model_id = "Qwen/Qwen1.5-0.5B"
tokenizer = AutoTokenizer.from_pretrained(base_model_id)
base_model = AutoModelForCausalLM.from_pretrained(base_model_id)
model = PeftModel.from_pretrained(base_model, "./fine_tuned_flood_model/fine_tuned_flood_model")

print("\n✅ Model ready! Type 'quit' to exit.")
print("-" * 50)

# Start an interactive loop
while True:
    user_input = input("\nEnter past 3 hours of rainfall (e.g., 5.0, 10.2, 15.5): ")
    
    if user_input.lower() in ['quit', 'exit', 'q']:
        print("Testing complete.")
        break
        
    try:
        # 1. Convert input into a list of numbers
        history = [float(x.strip()) for x in user_input.split(',')]
        
        # 🚨 2. SAFETY OVERRIDE CHECK (Add it right here!)
        if max(history) > 75.0:
            print("🚨 EMERGENCY OVERRIDE: Extreme rainfall detected! Ignoring AI smoothing—issuing Flash Flood Red Alert!")
        
        # 3. Format the prompt and generate normal AI prediction
        prompt = f"Given the past 3 hours of rainfall (mm): {history}. Predict the next 3 hours."
        formatted_prompt = f"<s>[INST] {prompt} [/INST]"
        
        inputs = tokenizer(formatted_prompt, return_tensors="pt")
        outputs = model.generate(
            **inputs, 
            max_new_tokens=40,
            pad_token_id=tokenizer.eos_token_id
        )
        
        prediction = tokenizer.decode(outputs[0], skip_special_tokens=True)
        final_answer = prediction.split("[/INST]")[-1].strip()
        
        print(f"🤖 AI Prediction: {final_answer}")
        
    except ValueError:
        print("⚠️ Invalid input. Please enter numbers separated by commas.")