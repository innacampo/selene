import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import json
import os

class SeleneBrain:
    def __init__(self, model_id="google/gemma-2-2b-it"):
        self.model_id = model_id
        self.tokenizer = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_model(self):
        """Loads the model with 4-bit quantization if GPU is available, else loads on CPU."""
        print(f"Loading model {self.model_id} on {self.device}...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        
        if self.device == "cuda":
            # 4-bit Quantization Config
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                quantization_config=bnb_config,
                device_map="auto"
            )
        else:
            # Fallback for CPU
            print("CUDA not detected. Loading model on CPU (this may be slow).")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                torch_dtype=torch.float32,
                device_map="cpu"
            )
        
        print("Model loaded successfully.")

    def process_symptom(self, text):
        """Converts user text into structured JSON using the LLM."""
        if not self.model or not self.tokenizer:
            return {"error": "Model not loaded. Please call load_model() first."}

        system_prompt = "You are SELENE, a menopause research partner. Convert the user's text into strict JSON: {symptom, severity, duration, clinical_category}."
        
        # Structure the prompt for Gemma (Instruct format)
        messages = [
            {"role": "user", "content": f"{system_prompt}\n\nUser input: {text}"}
        ]
        
        # Apply chat template if available, otherwise simple string
        try:
            prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        except Exception:
            prompt = f"{system_prompt}\n\nUser: {text}\n\nJSON Output:"

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs, 
                max_new_tokens=256,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Post-process to extract JSON
        try:
            # Look for the last JSON-like block in the response
            json_start = response.rfind('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                return {"error": "Could not parse JSON from model response", "raw_response": response}
        except Exception as e:
            return {"error": f"JSON parsing failed: {str(e)}", "raw_response": response}

    def save_to_journal(self, entry):
        """Appends the structured entry to the local JSON store."""
        journal_path = os.path.join(os.path.dirname(__file__), "..", "data", "journal.json")
        try:
            if os.path.exists(journal_path):
                with open(journal_path, "r") as f:
                    journal = json.load(f)
            else:
                journal = []
            
            journal.append(entry)
            
            with open(journal_path, "w") as f:
                json.dump(journal, f, indent=4)
            return True
        except Exception as e:
            print(f"Failed to save to journal: {e}")
            return False
