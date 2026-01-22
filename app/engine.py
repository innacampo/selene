import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import os

class MedGemmaEngine:
    def __init__(self, model_path="google/medgemma-1.5-4b-it"):
        self.model_path = model_path
        self.tokenizer = None
        self.model = None

    def load_model(self, token=None):
        """Loads the model and tokenizer."""
        print(f"Loading model from {self.model_path}...")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, token=token)
            
            # Simple loading with auto device map
            # Assuming user might have GPU, but fallback is handled by library usually
            # added 4-bit loading for memory efficiency if bitsandbytes is available
            try:
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16
                )
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_path,
                    quantization_config=quantization_config,
                    device_map="auto",
                    trust_remote_code=True,
                    token=token
                )
            except Exception as e:
                print(f"Failed to load with quantization (likely no GPU): {e}")
                print("Falling back to CPU/standard load...")
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_path,
                    device_map="cpu", # Force CPU if quantization failed implying no GPU
                    torch_dtype=torch.float32,
                    trust_remote_code=True,
                    token=token
                )

            return True, "Model loaded successfully!"
        except Exception as e:
            return False, f"Error loading model: {str(e)}"

    def generate_response(self, messages, max_new_tokens=512):
        """
        Generates a response given a list of messages.
        messages: list of dicts [{'role': 'user', 'content': '...'}, ...]
        """
        if not self.model or not self.tokenizer:
            return "Error: Model not loaded."

        # Apply chat template
        input_ids = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(self.model.device)

        terminators = [
            self.tokenizer.eos_token_id,
            self.tokenizer.convert_tokens_to_ids("<end_of_turn>")
        ]

        outputs = self.model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
        )

        response = outputs[0][input_ids.shape[-1]:]
        return self.tokenizer.decode(response, skip_special_tokens=True)
