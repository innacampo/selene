# SELENE - Menopause Research Partner

SELENE is under construction and will be released soon. 

SELENE is a privacy-first AI companion designed to help women track and understand their health during midlife. It uses a local LLM to process and structure symptom logs without sending sensitive data to the cloud.

## Key Features

- **Privacy-First**: All AI processing happens locally on your device.
- **Natural Language Logging**: Speak or type how you feel; SELENE structures the data.
- **Structured Journal**: Automatically converts entries into JSON for better tracking.


## Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **AI Engine**: [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
- **Model**: [Gemma-2-2b-it](https://huggingface.co/google/gemma-2-2b-it) (4-bit quantized via `bitsandbytes`)
- **Deep Learning**: [PyTorch](https://pytorch.org/)

## Getting Started

### Prerequisites

- Python 3.9+
- (Optional) CUDA-enabled GPU for faster performance.

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd selene
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the Streamlit app:
```bash
streamlit run app/main.py
```

## How to Use

1. **Load the Engine**: In the sidebar, click the **"Load Engine"** button. This will initialize the Gemma model (may take a minute on CPU).
2. **Log Symptoms**: Type your symptom check-in in the main text area (e.g., *"I've had hot flashes and trouble sleeping for two nights"*).
3. **Log to Journal**: Click **"Log to Journal"**. SELENE will structure the entry and save it to `data/journal.json`.
4. **View History**: Toggle the **"Show Journal History"** checkbox to see your previous entries.

## 📁 Project Structure

- `app/main.py`: Streamlit frontend and UI logic.
- `app/engine.py`: `SeleneBrain` class handling model loading and inference.
- `data/journal.json`: Local storage for your structured health logs.
- `requirements.txt`: Python package dependencies.
