import sys
import os
import json
from unittest.mock import MagicMock

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from engine import SeleneBrain

def test_symptom_processing():
    print("Testing SeleneBrain.process_symptom with mock model...")
    
    brain = SeleneBrain()
    
    # Mock the model and tokenizer to avoid heavy downloads during test
    brain.model = MagicMock()
    brain.tokenizer = MagicMock()
    
    # Mock response from tokenizer and model
    mock_json = '{"symptom": "dizziness and hot flashes", "severity": "moderate", "duration": "recent", "clinical_category": "vasomotor/neuro"}'
    
    # Mock decode output
    brain.tokenizer.decode.return_value = f"Some thinking... {mock_json}"
    brain.tokenizer.apply_chat_template.return_value = "Mocked Prompt"
    # Mock tokenizer return value to handle .to() call
    mock_inputs = MagicMock()
    mock_inputs.to.return_value = mock_inputs
    brain.tokenizer.return_value = mock_inputs
    
    # Run process_symptom
    result = brain.process_symptom("I feel dizzy and hot")
    
    print(f"Mock Result: {result}")
    
    # Assertions
    assert "symptom" in result
    assert result["symptom"] == "dizziness and hot flashes"
    assert "clinical_category" in result
    
    print("Test PASSED!")

if __name__ == "__main__":
    try:
        test_symptom_processing()
    except Exception as e:
        print(f"Test FAILED: {e}")
        sys.exit(1)
