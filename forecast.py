import ast
import re
import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

@st.cache_resource
def load_ai_model():
    """Loads the model once and caches it to prevent Streamlit from crashing or lagging."""
    print("Loading AI model for forecasting...")
    base_model_id = "Qwen/Qwen1.5-0.5B"
    tokenizer = AutoTokenizer.from_pretrained(base_model_id)
    base_model = AutoModelForCausalLM.from_pretrained(base_model_id)
    model = PeftModel.from_pretrained(base_model, "./fine_tuned_flood_model/fine_tuned_flood_model")
    return tokenizer, model

def forecast_next_3_hours(rainfall_values):
    """
    Predicts the next 3 hours using the fine-tuned AI model.
    Includes an emergency override for extreme spikes.
    """
    if len(rainfall_values) == 0:
        return [0.0, 0.0, 0.0]

    # 1. Grab the most recent 3 hours of data
    history = rainfall_values[-3:]
    while len(history) < 3:
        history.insert(0, 0.0)  # Pad with zeros if less than 3 hours exist

    # 2. 🚨 EMERGENCY OVERRIDE
    if max(history) > 75.0:
        print("🚨 EMERGENCY OVERRIDE: Extreme rainfall detected (>75mm)!")
        return [85.0, 95.0, 70.0]  # Force a severe flash flood alert

    # 3. AI MODEL PREDICTION
    tokenizer, model = load_ai_model()
    
    prompt = f"Given the past 3 hours of rainfall (mm): {history}. Predict the next 3 hours."
    formatted_prompt = f"<s>[INST] {prompt} [/INST]"
    
    inputs = tokenizer(formatted_prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs, 
        max_new_tokens=40,
        pad_token_id=tokenizer.eos_token_id
    )
    
    prediction_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    final_answer = prediction_text.split("[/INST]")[-1].strip()
    
    # 4. PARSE TEXT TO PYTHON LIST
    try:
        # Extract the array from the AI's text (e.g. "[15.0, 10.2, 5.1]")
        match = re.search(r'\[.*?\]', final_answer)
        if match:
            predicted_values = ast.literal_eval(match.group())
            if len(predicted_values) >= 3:
                return [float(x) for x in predicted_values[:3]]
    except Exception as e:
        print(f"⚠️ AI parsing failed: {e}. Falling back to safe trend.")

    # 5. FAIL-SAFE FALLBACK (Prevents crashes if the AI hallucinates text during presentation)
    latest = history[-1]
    return [max(0.0, latest * 0.8), max(0.0, latest * 0.5), max(0.0, latest * 0.2)]

if __name__ == "__main__":
    test_values = [40.0, 60.0, 80.0]  # Should trigger the 75mm emergency override
    forecasts = forecast_next_3_hours(test_values)
    print("Next 3 hour rainfall forecast:")
    for hour, value in enumerate(forecasts, start=1):
        print(f"Hour {hour}: {round(value, 2)} mm")